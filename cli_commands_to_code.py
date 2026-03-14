import subprocess

def deploy_uvicorn():
    command = ["uvicorn", "main:app", "--reload"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Command was Successful:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Command Failed:\n", e.stderr)

deploy_uvicorn()