import os
import glob
import shutil

class FileIOTool:
    @staticmethod
    def read_input_data(input_dir="generated"):
        """generated 디렉토리에서 초안 마크다운과 이미지 파일들을 스캔합니다."""
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")

        md_files = glob.glob(os.path.join(input_dir, "*.md"))
        if not md_files:
            return None, []

        target_draft = md_files[0]
        with open(target_draft, "r", encoding="utf-8") as f:
            raw_content = f.read()

        images = glob.glob(os.path.join(input_dir, "*.png")) + glob.glob(os.path.join(input_dir, "*.jpg"))
        return raw_content, images

    @staticmethod
    def save_revised_file(revised_dir, filename, content):
        """완성된 초안을 generated/revised/ 에 저장합니다."""
        os.makedirs(revised_dir, exist_ok=True)
        file_path = os.path.join(revised_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    @staticmethod
    def relocate_to_post(revised_file_path, category, filename):
        """완성본을 카테고리에 맞는 _posts/{category} 디렉토리로 이동시킵니다."""
        target_post_dir = f"_posts/{category}"
        os.makedirs(target_post_dir, exist_ok=True)

        final_post_path = os.path.join(target_post_dir, filename)
        shutil.copy(revised_file_path, final_post_path)
        return target_post_dir, final_post_path
