import os
import subprocess

def ensure_app_dir():
    """Ensure app directory and venv exist."""
    os.makedirs("app", exist_ok=True)
    if not os.path.exists("app/venv"):
        subprocess.run(["python3", "-m", "venv", "app/venv"])


def run_in_venv(cmd, install_requirements=False):
    """Run a command in the app/venv environment."""
    venv_python = os.path.join("app", "venv", "bin", "python")
    venv_pip = os.path.join("app", "venv", "bin", "pip")
    if install_requirements:
        subprocess.run([venv_pip, "install", "pytest"], check=True)
    result = subprocess.run(f"source app/venv/bin/activate && {cmd}", shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


def get_user_input(prompt):
    return input(prompt)


def print_report(report):
    print("\n===== 总结报告 =====\n")
    print(report) 