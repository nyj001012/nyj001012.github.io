import os
import glob
import shutil

class FileIOTool:
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
            glob.glob(os.path.join(input_dir, "*.png"))
            + glob.glob(os.path.join(input_dir, "*.jpg"))
            + glob.glob(os.path.join(input_dir, "*.jpeg"))
        )
        return raw_content, images

    @staticmethod
    def save_generated_file(generated_dir, filename, content):
        """완성된 초안을 generated/ 에 저장합니다."""
        os.makedirs(generated_dir, exist_ok=True)
        file_path = os.path.join(generated_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    @staticmethod
    def relocate_to_post(generated_file_path, posts_dir, category, filename):
        """완성본을 카테고리에 맞는 _posts/{category} 디렉토리로 복사합니다."""
        target_post_dir = os.path.join(posts_dir, category)
        os.makedirs(target_post_dir, exist_ok=True)

        final_post_path = os.path.join(target_post_dir, filename)
        shutil.copy(generated_file_path, final_post_path)
        return target_post_dir, final_post_path
