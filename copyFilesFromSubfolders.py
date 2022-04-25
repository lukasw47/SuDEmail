# copyFilesFromSubfolders
# Author:   Ivanov
# Revision: 0.2
#

import os
import shutil
import glob


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


def scan_folder(source, target):
    source_files = find_csv_files(source)
    copy_files_to_target(files=source_files, target=target)
    return len(source_files)


def create_folder_if_not_exists(path_name: str):
    os.makedirs(path_name, exist_ok=True)


def find_csv_files(path_name: str) -> list[str]:
    source_glob = os.path.join(path_name, '**/*.csv')
    return glob.glob(source_glob, recursive=True)


def copy_files_to_target(files: list[str], target: str):
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

    resultNumber = scan_folder(sourceFolderName, targetFolderName)
    print(f"Anzahl kopierter Dateien: {resultNumber}")
