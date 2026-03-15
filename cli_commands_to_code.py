import logging
import subprocess

logger = logging.getLogger(__name__)


def deploy_uvicorn():
    command = ["uvicorn", "main:app", "--reload"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Command was Successful:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command Failed:\n{e.stderr}")


deploy_uvicorn()