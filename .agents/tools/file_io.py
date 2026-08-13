import os
import glob
import re
import shutil
from collections import Counter
from urllib.parse import unquote
from collections import Counter
from urllib.parse import unquote

class FileIOTool:
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

    @staticmethod
    def read_input_data(input_dir="draft"):
        """draft 디렉토리에서 초안 마크다운과 이미지 파일들을 스캔합니다."""
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")

        md_files = sorted(glob.glob(os.path.join(input_dir, "*.md")))
        if not md_files:
            return None, []

        target_draft = md_files[0]
        with open(target_draft, "r", encoding="utf-8") as f:
            raw_content = f.read()

        images = sorted(
            path
            for path in glob.glob(os.path.join(input_dir, "*"))
            if os.path.isfile(path)
            and os.path.splitext(path)[1].lower() in FileIOTool.IMAGE_EXTENSIONS
        )
        return raw_content, images

    @staticmethod
    def extract_local_image_references(content):
        """Obsidian/Markdown 형식의 로컬 이미지 파일명을 등장 순서대로 추출합니다."""
        references = []
        matches = []

        for match in re.finditer(r"!\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content):
            matches.append((match.start(), match.group(1).strip()))

        for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", content):
            target = match.group(1).strip()
            if target.startswith("<") and ">" in target:
                target = target[1:target.index(">")]
            else:
                target = target.split(maxsplit=1)[0]
            if target.lower().startswith(("http://", "https://", "data:", "/assets/")):
                continue
            matches.append((match.start(), target))

        for _, target in sorted(matches):
            filename = os.path.basename(unquote(target).replace("\\", "/"))
            if os.path.splitext(filename)[1].lower() in FileIOTool.IMAGE_EXTENSIONS:
                references.append(filename)
        return references

    @staticmethod
    def validate_draft_images(content, images):
        """초안 참조와 draft 폴더의 실제 이미지가 정확히 일치하는지 검증합니다."""
        references = FileIOTool.extract_local_image_references(content)
        image_names = [os.path.basename(path) for path in images]
        reference_counts = Counter(name.casefold() for name in references)
        image_counts = Counter(name.casefold() for name in image_names)

        if len(references) == len(image_names) and reference_counts == image_counts:
            return references

        reference_names = {name.casefold(): name for name in references}
        actual_names = {name.casefold(): name for name in image_names}
        missing = [
            reference_names[name]
            for name in (reference_counts - image_counts).elements()
        ]
        unreferenced = [
            actual_names[name]
            for name in (image_counts - reference_counts).elements()
        ]
        details = [
            "Draft image validation failed",
            f"markdown_references={len(references)}",
            f"draft_files={len(image_names)}",
        ]
        if missing:
            details.append(f"missing_files={missing}")
        if unreferenced:
            details.append(f"unreferenced_files={unreferenced}")
        raise ValueError("; ".join(details))

    @staticmethod
    def extract_local_image_references(content):
        """Obsidian/Markdown 형식의 로컬 이미지 파일명을 등장 순서대로 추출합니다."""
        references = []
        matches = []

        for match in re.finditer(r"!\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content):
            matches.append((match.start(), match.group(1).strip()))

        for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", content):
            target = match.group(1).strip()
            if target.startswith("<") and ">" in target:
                target = target[1:target.index(">")]
            else:
                target = target.split(maxsplit=1)[0]
            if target.lower().startswith(("http://", "https://", "data:", "/assets/")):
                continue
            matches.append((match.start(), target))

        for _, target in sorted(matches):
            filename = os.path.basename(unquote(target).replace("\\", "/"))
            if os.path.splitext(filename)[1].lower() in FileIOTool.IMAGE_EXTENSIONS:
                references.append(filename)
        return references

    @staticmethod
    def validate_draft_images(content, images):
        """초안 참조와 draft 폴더의 실제 이미지가 정확히 일치하는지 검증합니다."""
        references = FileIOTool.extract_local_image_references(content)
        image_names = [os.path.basename(path) for path in images]
        reference_counts = Counter(name.casefold() for name in references)
        image_counts = Counter(name.casefold() for name in image_names)

        if len(references) == len(image_names) and reference_counts == image_counts:
            return references

        reference_names = {name.casefold(): name for name in references}
        actual_names = {name.casefold(): name for name in image_names}
        missing = [
            reference_names[name]
            for name in (reference_counts - image_counts).elements()
        ]
        unreferenced = [
            actual_names[name]
            for name in (image_counts - reference_counts).elements()
        ]
        details = [
            "Draft image validation failed",
            f"markdown_references={len(references)}",
            f"draft_files={len(image_names)}",
        ]
        if missing:
            details.append(f"missing_files={missing}")
        if unreferenced:
            details.append(f"unreferenced_files={unreferenced}")
        raise ValueError("; ".join(details))

    @staticmethod
    def save_generated_file(generated_dir, filename, content):
        """완성된 초안을 generated/ 에 저장합니다."""
        os.makedirs(generated_dir, exist_ok=True)
        file_path = os.path.join(generated_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    @staticmethod
    def publish_images(content, images, assets_root, category, date_prefix):
        """본문 이미지 링크를 공개 경로로 바꾸고 실제 파일을 복사합니다."""
        category_slug = re.sub(r"[^a-z0-9_-]+", "-", category.lower()).strip("-")
        category_slug = category_slug or "uncategorized"
        target_dir = os.path.join(assets_root, category_slug)
        published_paths = []

        markdown_refs = [
            match
            for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", content)
            if not match.group(1).strip().lower().startswith(
                ("http://", "https://", "data:", "/assets/")
            )
        ]
        if len(markdown_refs) != len(images):
            raise ValueError(
                "Generated image validation failed; "
                f"markdown_references={len(markdown_refs)}; "
                f"source_images={len(images)}"
            )

        for index, image_path in enumerate(images, start=1):
            original_ref = markdown_refs[index - 1].group(1).strip().strip("<>")
            source_extension = os.path.splitext(image_path)[1].lower()
            proposed_name = os.path.basename(original_ref.replace("\\", "/"))
            proposed_stem = os.path.splitext(proposed_name)[0]
            safe_stem = re.sub(r"[^a-z0-9_-]+", "-", proposed_stem.lower()).strip("-")
            if not safe_stem or safe_stem.startswith("pasted-image"):
                safe_stem = f"blog-image-{index}"

            target_name = f"{date_prefix}-{safe_stem}{source_extension}"
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, target_name)
            shutil.copy2(image_path, target_path)

            public_path = f"/assets/images/page/{category_slug}/{target_name}"
            content = content.replace(original_ref, public_path, 1)
            published_paths.append(target_path)

        return content, published_paths

    @staticmethod
    def relocate_to_post(generated_file_path, posts_dir, category, filename):
        """완성본을 카테고리에 맞는 _posts/{category} 디렉토리로 복사합니다."""
        target_post_dir = os.path.join(posts_dir, category)
        os.makedirs(target_post_dir, exist_ok=True)

        final_post_path = os.path.join(target_post_dir, filename)
        shutil.copy2(generated_file_path, final_post_path)
        return target_post_dir, final_post_path
