import logging
import subprocess

logger = logging.getLogger("blog_pipeline")


class GitClientTool:
    @staticmethod
    def commit_and_push(target_dir, message):
        """지정된 디렉토리 변경 사항을 커밋하고 원격 저장소에 푸시합니다."""
        try:
            logger.info("Staging changes (target=%s).", target_dir)
            subprocess.run(["git", "add", target_dir], check=True)

            logger.info("Creating commit (message=%s).", message)
            subprocess.run(["git", "commit", "-m", message], check=True)

            logger.info("Pushing commit to remote repository.")
            subprocess.run(["git", "push"], check=True)

            return True
        except subprocess.CalledProcessError:
            logger.exception("Git operation failed.")
            raise
