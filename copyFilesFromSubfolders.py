# copyFilesFromSubfolders
# Author:   Ivanov
# Revision: 0.2
#

import os
import shutil
import glob
from typing import Optional


def scanFolder(source, target):
    """ Scans a sourcefolder for csv-files and copies them to target.
        Returns number of files copied."""

    numberOfFilesCopied = 0

    for content in os.scandir(source):
        if content.is_dir():
            print(content.path)
            numberOfFilesCopied += scanFolder(content.path, target)
        elif content.is_file():
            if content.path.endswith(".csv"):
                print(content.path)
                shutil.copy(content, target)
                numberOfFilesCopied += 1

    return numberOfFilesCopied


def scan_folder(source: str, target: str) -> None:
    source_files = find_csv_files(source)
    if source_files is None:
        return
    copy_files_to_target(files=source_files, target=target)
    print(f"Anzahl kopierter Dateien: {len(source_files)}")


def create_folder_if_not_exists(path_name: str) -> None:
    os.makedirs(path_name, exist_ok=True)


def find_csv_files(path_name: str) -> Optional[list[str]]:
    if os.path.isdir(path_name):
        print(f'>> error: folder not found: {path_name}')
        return
    source_glob = os.path.join(path_name, '**/*time_record*.csv')
    return glob.glob(source_glob, recursive=True)


def copy_files_to_target(files: list[str], target: str) -> None:
    create_folder_if_not_exists(target)
    for source_file in files:
        print(f'>> copy {source_file}')
        source_filename = os.path.basename(source_file)
        target_file = os.path.join(target, source_filename)
        shutil.copy(source_file, target_file)


if __name__ == '__main__':
    path = "."
    sourceFolderName = os.path.join(path, "quellordner")
    targetFolderName = os.path.join(path, "zielordner")

    scan_folder(sourceFolderName, targetFolderName)
