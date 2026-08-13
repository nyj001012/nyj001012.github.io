import subprocess

class GitClientTool:
    @staticmethod
    def commit_and_push(target_dir, message):
        """지정된 디렉토리 변경 사항을 커밋하고 원격 저장소에 푸시합니다."""
        try:
            print(f"📦 Staging changes in: {target_dir}")
            subprocess.run(["git", "add", target_dir], check=True)

            print(f"📝 Committing with message: '{message}'")
            subprocess.run(["git", "commit", "-m", message], check=True)

            print("🚀 Pushing to remote repository...")
            subprocess.run(["git", "push"], check=True)

            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            raise e
