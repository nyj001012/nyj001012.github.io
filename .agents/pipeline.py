import os
import re
import base64
import json
import mimetypes
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

# Custom Tools Import
from tools.file_io import FileIOTool
from tools.git_client import GitClientTool

AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(AGENTS_DIR)
PROMPTS_DIR = os.path.join(AGENTS_DIR, "prompts")
DRAFT_DIR = os.path.join(AGENTS_DIR, "draft")
GENERATED_DIR = os.path.join(AGENTS_DIR, "generated")
LOG_DIR = os.path.join(AGENTS_DIR, "log")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")
ASSETS_IMAGES_DIR = os.path.join(REPO_ROOT, "assets", "images", "page")
ALLOWED_CATEGORIES = {
    "42_seoul",
    "algorithm",
    "books",
    "csharp",
    "etc",
    "html",
    "lecture",
    "license",
    "python",
    "spring",
    "springboot",
    "web",
}

logger = logging.getLogger("blog_pipeline")
client = None


def load_local_env(env_path):
    """Load simple KEY=VALUE pairs without overriding the process environment."""
    if not os.path.isfile(env_path):
        return False

    with open(env_path, "r", encoding="utf-8-sig") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.removeprefix("export ").strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            if key:
                os.environ.setdefault(key, value)
    return True


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    log_filename = f"pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.log"
    log_path = os.path.join(LOG_DIR, log_filename)

    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(threadName)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return log_path

def load_prompt(prompt_path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def call_agent(
    agent_name,
    system_prompt,
    user_content,
    model="gpt-4o",
    response_format=None,
):
    logger.info("Agent '%s' request started (model=%s).", agent_name, model)
    request = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
    }
    if response_format is not None:
        request["response_format"] = response_format
    response = client.chat.completions.create(
        **request
    )
    result = response.choices[0].message.content.strip()
    logger.info("Agent '%s' request completed (output_chars=%d).", agent_name, len(result))
    return result


def build_asset_input(images, refined_body):
    content = [
        {
            "type": "text",
            "text": (
                f"Images found, in order: {images}\n\n"
                f"Body context:\n{refined_body}"
            ),
        }
    ]
    for index, image_path in enumerate(images, start=1):
        mime_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("ascii")
        content.append(
            {
                "type": "text",
                "text": f"IMAGE_{index}: {os.path.basename(image_path)}",
            }
        )
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{encoded_image}",
                    "detail": "low",
                },
            }
        )
    return content


def normalize_frontmatter_output(content):
    """Extract and validate the Meta Generator's YAML frontmatter block."""
    normalized = content.strip()
    fence_start = re.search(r"```(?:yaml|yml)\s*\r?\n", normalized, re.IGNORECASE)
    if fence_start:
        fence_end = normalized.rfind("\n```")
        if fence_end > fence_start.end():
            normalized = normalized[fence_start.end():fence_end].strip()

    delimiters = list(re.finditer(r"(?m)^---[ \t]*$", normalized))
    if len(delimiters) < 2:
        raise ValueError("Meta Generator output does not contain complete frontmatter.")
    normalized = normalized[delimiters[0].start():delimiters[1].end()]

    required_fields = {
        "title",
        "slug",
        "excerpt",
        "category",
        "author_profile",
        "sidebar",
        "tag",
        "toc",
        "toc_sticky",
        "last_modified_at",
    }
    present_fields = set(
        re.findall(r"(?m)^([a-z_]+):(?:[ \t]*.*)?$", normalized)
    )
    missing_fields = sorted(required_fields - present_fields)
    if missing_fields:
        raise ValueError(
            f"Meta Generator output is missing required fields: {missing_fields}"
        )
    if extract_frontmatter_value(normalized, "title", "untitled") == "untitled":
        raise ValueError("Meta Generator output has an empty title.")
    slug = extract_frontmatter_value(normalized, "slug", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(
            "Meta Generator slug must use descriptive English words in "
            f"lowercase ASCII kebab-case: {slug!r}"
        )
    if extract_primary_category(normalized) == "uncategorized":
        raise ValueError("Meta Generator output has an invalid category list.")
    return normalized.rstrip() + "\n"


def parse_asset_manifest(content, images):
    """Validate the JSON filename manifest returned by the Asset Manager."""
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("Asset Manager output is not valid JSON.") from error

    assets = payload.get("assets")
    if not isinstance(assets, list):
        raise ValueError("Asset Manager output must contain an 'assets' array.")

    expected_sources = {
        os.path.basename(path).casefold(): os.path.basename(path)
        for path in images
    }
    expected_extensions = {
        os.path.basename(path).casefold(): os.path.splitext(path)[1].lower()
        for path in images
    }
    manifest = []
    seen_sources = set()
    seen_filenames = set()
    filename_pattern = re.compile(
        r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:png|jpe?g|gif|webp)$"
    )

    for item in assets:
        if not isinstance(item, dict):
            raise ValueError("Each Asset Manager item must be an object.")
        source = item.get("source")
        filename = item.get("filename")
        if not isinstance(source, str) or not isinstance(filename, str):
            raise ValueError("Each asset requires string 'source' and 'filename' fields.")

        source_key = os.path.basename(source).casefold()
        filename_key = filename.casefold()
        if source_key not in expected_sources:
            raise ValueError(f"Asset Manager returned an unknown source: {source}")
        if source_key in seen_sources:
            raise ValueError(f"Asset Manager duplicated source: {source}")
        if filename_key in seen_filenames:
            raise ValueError(f"Asset Manager duplicated filename: {filename}")
        if os.path.basename(filename) != filename or not filename_pattern.fullmatch(filename):
            raise ValueError(
                "Asset Manager filename must use descriptive English words in "
                f"lowercase ASCII kebab-case: {filename}"
            )
        if os.path.splitext(filename)[1].lower() != expected_extensions[source_key]:
            raise ValueError(
                f"Asset Manager must preserve the source extension: {filename}"
            )

        seen_sources.add(source_key)
        seen_filenames.add(filename_key)
        manifest.append(
            {
                "source": expected_sources[source_key],
                "filename": filename,
            }
        )

    missing_sources = sorted(set(expected_sources) - seen_sources)
    if missing_sources:
        missing_names = [expected_sources[source] for source in missing_sources]
        raise ValueError(f"Asset Manager omitted source images: {missing_names}")
    return manifest


def build_final_document(frontmatter_block, body):
    body = body.strip()
    if not body:
        raise ValueError("Content Editor output body is empty.")
    if re.match(r"^---[ \t]*(?:\r?\n|$)", body):
        raise ValueError("Content Editor output must not contain YAML frontmatter.")
    fence_count = len(re.findall(r"(?m)^```", body))
    if fence_count % 2:
        raise ValueError(
            f"Content Editor output has unbalanced code fences: {fence_count}"
        )
    document = f"{frontmatter_block.rstrip()}\n\n{body}\n"
    normalize_frontmatter_output(document)
    return document


def extract_frontmatter_value(frontmatter_block, key, default):
    match = re.search(
        rf"(?m)^{re.escape(key)}:[ \t]*([^\r\n]+?)[ \t]*$",
        frontmatter_block,
    )
    if not match:
        return default
    return match.group(1).strip().strip("\"'") or default


def extract_primary_category(frontmatter_block):
    match = re.search(
        r"(?m)^category:[ \t]*\r?\n[ \t]*-[ \t]*([^\r\n]+?)[ \t]*$",
        frontmatter_block,
    )
    if not match:
        return "uncategorized"
    return match.group(1).strip().strip("\"'") or "uncategorized"


def normalize_frontmatter_category(frontmatter_block):
    category = extract_primary_category(frontmatter_block)
    if category in ALLOWED_CATEGORIES:
        return frontmatter_block

    logger.warning(
        "Unsupported category '%s'; falling back to 'etc'.",
        category,
    )
    return re.sub(
        r"(?m)(^category:[ \t]*\r?\n[ \t]*-[ \t]*)[^\r\n]+?[ \t]*$",
        r"\g<1>etc",
        frontmatter_block,
        count=1,
    )

def main():
    global client

    log_path = setup_logging()
    logger.info("Pipeline started (log=%s).", log_path)

    try:
        env_path = os.path.join(AGENTS_DIR, ".env")
        if load_local_env(env_path):
            logger.info("Local environment loaded from %s.", env_path)

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        client = OpenAI(api_key=api_key)
        logger.info("[1/7] OpenAI client initialized.")

        logger.info("[2/7] Loading draft and images from %s.", DRAFT_DIR)
        raw_content, images = FileIOTool.read_input_data(DRAFT_DIR)
        if not raw_content:
            logger.warning("No markdown draft found in %s. Pipeline stopped.", DRAFT_DIR)
            return
        logger.info(
            "[2/7] Draft loaded (content_chars=%d, image_count=%d).",
            len(raw_content),
            len(images),
        )
        image_references = FileIOTool.validate_draft_images(raw_content, images)
        logger.info(
            "[2/7] Draft image validation passed (reference_count=%d).",
            len(image_references),
        )

        logger.info("[3/7] Content Editor and Meta Generator started concurrently.")
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_body = executor.submit(
                call_agent,
                "Content Editor",
                load_prompt(os.path.join(PROMPTS_DIR, "01_editor.md")),
                raw_content,
            )

            current_time = datetime.now().astimezone().isoformat(timespec="seconds")
            meta_input = f"Current Timestamp: {current_time}\n\nDraft Content:\n{raw_content}"
            future_meta = executor.submit(
                call_agent,
                "Meta Generator",
                load_prompt(os.path.join(PROMPTS_DIR, "02_meta.md")),
                meta_input,
            )

            refined_body = future_body.result()
            frontmatter_block = normalize_frontmatter_output(future_meta.result())
        FileIOTool.validate_draft_images(refined_body, images)
        FileIOTool.validate_image_spacing(refined_body)
        frontmatter_block = normalize_frontmatter_category(frontmatter_block)
        logger.info("[3/7] Parallel editing and metadata generation completed.")

        logger.info("[4/7] Asset management and document merge started.")
        asset_prompt = load_prompt(os.path.join(PROMPTS_DIR, "03_asset.md"))
        asset_input = build_asset_input(images, refined_body)
        asset_manifest_output = call_agent(
            "Asset Manager",
            asset_prompt,
            asset_input,
            response_format={"type": "json_object"},
        )
        asset_manifest = parse_asset_manifest(asset_manifest_output, images)
        logger.info("[4/7] Asset management and document merge completed.")

        post_title = extract_frontmatter_value(frontmatter_block, "title", "untitled")
        slug = extract_frontmatter_value(frontmatter_block, "slug", "")
        generated_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"

        category = extract_primary_category(frontmatter_block)
        final_body, published_assets = FileIOTool.publish_images(
            refined_body,
            images,
            asset_manifest,
            ASSETS_IMAGES_DIR,
            category,
            datetime.now().strftime("%Y-%m-%d"),
        )
        FileIOTool.validate_image_spacing(final_body)
        final_output_content = build_final_document(frontmatter_block, final_body)
        logger.info("[4/7] Assets published (count=%d).", len(published_assets))

        logger.info("[5/7] Saving completed draft to %s.", GENERATED_DIR)
        generated_file_path = FileIOTool.save_generated_file(
            GENERATED_DIR,
            generated_filename,
            final_output_content,
        )
        logger.info("[5/7] Completed draft saved (path=%s).", generated_file_path)

        logger.info("[6/7] Publishing generated draft (category=%s).", category)
        target_post_dir, final_post_path = FileIOTool.relocate_to_post(
            generated_file_path,
            POSTS_DIR,
            category,
            generated_filename,
        )
        logger.info("[6/7] Post copied (path=%s).", final_post_path)

        commit_msg = f"blog: add new post {post_title}"
        logger.info("[7/7] Git commit and push started.")
        GitClientTool.commit_and_push([target_post_dir, *published_assets], commit_msg)
        logger.info("[7/7] Git commit and push completed.")
        logger.info("Pipeline completed successfully.")
    except Exception:
        logger.exception("Pipeline failed.")
        raise

if __name__ == "__main__":
    main()
