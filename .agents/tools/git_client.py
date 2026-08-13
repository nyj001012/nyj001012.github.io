import logging
import subprocess

logger = logging.getLogger("blog_pipeline")


class GitClientTool:
    @staticmethod
    def commit_and_push(targets, message):
        """지정된 파일과 디렉토리 변경 사항을 커밋하고 원격 저장소에 푸시합니다."""
        try:
            if isinstance(targets, (str, bytes)):
                targets = [targets]
            for target in targets:
                logger.info("Staging changes (target=%s).", target)
                subprocess.run(["git", "add", target], check=True)

            logger.info("Creating commit (message=%s).", message)
            subprocess.run(["git", "commit", "-m", message], check=True)

            logger.info("Pushing commit to remote repository.")
            subprocess.run(["git", "push"], check=True)

            return True
        except subprocess.CalledProcessError:
            logger.exception("Git operation failed.")
            raise
