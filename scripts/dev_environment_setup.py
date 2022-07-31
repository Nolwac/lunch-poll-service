import subprocess
import shlex


def install_requirements() -> None:
    subprocess.run(shlex.split("python -m pip install -r requirements.txt"), shell=True)
    subprocess.run(shlex.split("pre-commit install"), shell=True)


def run_migrations() -> None:
    subprocess.run(shlex.split("python manage.py makemigrations"), shell=True)
    subprocess.run(shlex.split("python manage.py migrate"), shell=True)


if __name__ == "__main__":
    install_requirements()
    run_migrations()
