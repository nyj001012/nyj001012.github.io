import os
import re
import base64
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

def call_agent(agent_name, system_prompt, user_content, model="gpt-4o"):
    logger.info("Agent '%s' request started (model=%s).", agent_name, model)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )
    result = response.choices[0].message.content.strip()
    logger.info("Agent '%s' request completed (output_chars=%d).", agent_name, len(result))
    return result


def build_asset_input(images, frontmatter_block, refined_body):
    content = [
        {
            "type": "text",
            "text": (
                f"Images found, in order: {images}\n\n"
                f"Frontmatter:\n{frontmatter_block}\n\nBody:\n{refined_body}"
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


def normalize_markdown_output(content):
    """Extract a complete Jekyll document from occasional agent narration/fences."""
    normalized = content.strip()
    fence_start = re.search(r"```(?:markdown|md)\s*\r?\n", normalized, re.IGNORECASE)
    if fence_start:
        fence_end = normalized.rfind("\n```")
        if fence_end > fence_start.end():
            normalized = normalized[fence_start.end():fence_end].strip()

    frontmatter_start = re.search(r"(?m)^---\s*$", normalized)
    if not frontmatter_start:
        raise ValueError("Agent output does not contain YAML frontmatter.")
    normalized = normalized[frontmatter_start.start():]

    frontmatter = re.match(r"^---\s*\r?\n.*?\r?\n---\s*(?:\r?\n|$)", normalized, re.DOTALL)
    if not frontmatter:
        raise ValueError("Agent output contains incomplete YAML frontmatter.")
    return normalized.rstrip() + "\n"


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
            frontmatter_block = future_meta.result()
        frontmatter_block = normalize_frontmatter_category(frontmatter_block)
        logger.info("[3/7] Parallel editing and metadata generation completed.")

        logger.info("[4/7] Asset management and document merge started.")
        asset_prompt = load_prompt(os.path.join(PROMPTS_DIR, "03_asset.md"))
        asset_input = build_asset_input(images, frontmatter_block, refined_body)
        final_output_content = call_agent(
            "Asset Manager",
            asset_prompt,
            asset_input,
        )
        final_output_content = normalize_markdown_output(final_output_content)
        logger.info("[4/7] Asset management and document merge completed.")

        post_title = extract_frontmatter_value(frontmatter_block, "title", "untitled")
        slug = re.sub(r'[^a-z0-9가-힣]+', '-', post_title.lower()).strip('-')
        generated_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"

        category = extract_primary_category(frontmatter_block)
        final_output_content, published_assets = FileIOTool.publish_images(
            final_output_content,
            images,
            ASSETS_IMAGES_DIR,
            category,
            datetime.now().strftime("%Y-%m-%d"),
        )
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
