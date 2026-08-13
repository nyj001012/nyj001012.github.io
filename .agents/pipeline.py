import os
import re
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

logger = logging.getLogger("blog_pipeline")
client = None


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

def main():
    global client

    log_path = setup_logging()
    logger.info("Pipeline started (log=%s).", log_path)

    try:
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
        logger.info("[3/7] Parallel editing and metadata generation completed.")

        logger.info("[4/7] Asset management and document merge started.")
        asset_prompt = load_prompt(os.path.join(PROMPTS_DIR, "03_asset.md"))
        asset_input = f"Images found: {images}\n\nFrontmatter:\n{frontmatter_block}\n\nBody:\n{refined_body}"
        final_output_content = call_agent(
            "Asset Manager",
            asset_prompt,
            asset_input,
        )
        logger.info("[4/7] Asset management and document merge completed.")

        title_match = re.search(r'title:\s*["\'](.+?)["\']', frontmatter_block)
        post_title = title_match.group(1) if title_match else "untitled"
        slug = re.sub(r'[^a-z0-9가-힣]+', '-', post_title.lower()).strip('-')
        generated_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"

        logger.info("[5/7] Saving completed draft to %s.", GENERATED_DIR)
        generated_file_path = FileIOTool.save_generated_file(
            GENERATED_DIR,
            generated_filename,
            final_output_content,
        )
        logger.info("[5/7] Completed draft saved (path=%s).", generated_file_path)

        cat_match = re.search(r'category:\s*\n\s*-\s*([a-zA-Z0-9_-]+)', frontmatter_block)
        category = cat_match.group(1) if cat_match else "uncategorized"

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
        GitClientTool.commit_and_push(target_post_dir, commit_msg)
        logger.info("[7/7] Git commit and push completed.")
        logger.info("Pipeline completed successfully.")
    except Exception:
        logger.exception("Pipeline failed.")
        raise

if __name__ == "__main__":
    main()
