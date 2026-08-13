import os
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

# Custom Tools Import
from tools.file_io import FileIOTool
from tools.git_client import GitClientTool

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
PROMPTS_DIR = ".agents/prompts"
REVISED_DIR = "generated/revised"

def load_prompt(prompt_path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def call_agent(system_prompt, user_content, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def main():
    print("🚀 Starting Blog Automation Pipeline with Tools...")

    # 1. Input Loading via FileIOTool (Pipeline Item #1)
    raw_content, images = FileIOTool.read_input_data("generated")
    if not raw_content:
        print("No raw draft files found in 'generated/'. Exiting.")
        return

    # 2. Parallel Processing (Pipeline Items #2, #3)
    print("🤖 Running Content Editor and Meta Generator concurrently...")
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_body = executor.submit(call_agent, load_prompt(os.path.join(PROMPTS_DIR, "01_editor.md")), raw_content)

        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
        meta_input = f"Current Timestamp: {current_time}\n\nDraft Content:\n{raw_content}"
        future_meta = executor.submit(call_agent, load_prompt(os.path.join(PROMPTS_DIR, "02_meta.md")), meta_input)

        refined_body = future_body.result()
        frontmatter_block = future_meta.result()

    # 3. Asset Management & Merging (Pipeline Items #4, #5)
    print("🖼️ Managing assets and combining document components...")
    asset_prompt = load_prompt(os.path.join(PROMPTS_DIR, "03_asset.md"))
    asset_input = f"Images found: {images}\n\nFrontmatter:\n{frontmatter_block}\n\nBody:\n{refined_body}"
    final_output_content = call_agent(asset_prompt, asset_input)

    # Extract title & generate filename format: yyyy-MM-dd-{title}.md
    title_match = re.search(r'title:\s*["\'](.+?)["\']', frontmatter_block)
    post_title = title_match.group(1) if title_match else "untitled"
    slug = re.sub(r'[^a-z0-9가-힣]+', '-', post_title.lower()).strip('-')
    revised_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"

    # Save using FileIOTool
    revised_file_path = FileIOTool.save_revised_file(REVISED_DIR, revised_filename, final_output_content)
    print(f"✅ Saved revised draft via Tool to: {revised_file_path}")

    # 4. Publishing & Git Automation (Pipeline Items #6, #7)
    print("🚀 Publishing post and executing Git sync...")
    cat_match = re.search(r'category:\s*\n\s*-\s*([a-zA-Z0-9_-]+)', frontmatter_block)
    category = cat_match.group(1) if cat_match else "uncategorized"

    # Move file using FileIOTool
    target_post_dir, _ = FileIOTool.relocate_to_post(revised_file_path, category, revised_filename)
    print(f"📁 Moved post to: {target_post_dir}")

    # Git Commit & Push using GitClientTool
    commit_msg = f"blog: add new post {post_title}"
    GitClientTool.commit_and_push(target_post_dir, commit_msg)
    print("🎉 Pipeline executed successfully with dedicated tools!")

if __name__ == "__main__":
    main()
