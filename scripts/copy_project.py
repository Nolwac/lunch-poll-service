"""
This script is only meant for testing setup automation script.
tips: some utility functions like copy_files, recursively_create_dir and copy_file may be imported
to be used outside this script.
"""

import subprocess
import shutil
from pathlib import Path
from typing import List


def recursively_create_dir(path: Path) -> None:
    """create a directory whether the parent exists or not"""
    try:
        path.mkdir()
    except FileNotFoundError:
        recursively_create_dir(path.parent)
        path.mkdir()


def copy_file(source_file: Path, destination: Path) -> None:
    """copy file to a different destination, whether the destination exist or not"""
    try:
        shutil.copy(source_file, destination, follow_symlinks=True)
    except FileNotFoundError:
        recursively_create_dir(destination.parent)
        shutil.copy(source_file, destination, follow_symlinks=True)
        print(f"{source_file} successfully copied ----> {destination}")


def copy_files(files: List[str], source: Path, destination: Path) -> None:
    for file in files:
        file_destination = destination / file
        file_path = source / file
        print(file_path, file_destination, "\n")
        copy_file(file_path, file_destination)


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    list_of_files = subprocess.check_output("git ls-files", shell=True).decode("utf-8").strip("\n").split("\n")
    # copy files to destination
    destination = root.parent / ".temp"
    try:
        copy_files(list_of_files, root, destination)
    except Exception as error:
        print(error)

    # copy git folder
    try:
        shutil.copytree(root / ".git", destination / ".git")
    except FileExistsError:
        print("git directory already exist")
