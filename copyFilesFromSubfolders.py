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
    create_folder_if_not_exist(target)
    source_glob = os.path.join(source, '**/*.csv')
    source_files = glob.glob(source_glob, recursive=True)
    for source_file in source_files:
        print(f'>> copy {source_file}')
        source_filename = os.path.basename(source_file)
        target_file = os.path.join(target, source_filename)
        shutil.copy(source_file, target_file)
    return len(source_files)


def create_folder_if_not_exist(name):
    os.makedirs(name, exist_ok=True)


if __name__ == '__main__':
    # configuration
    path = "."
    sourceFolderName = os.path.join(path, "quellordner")
    targetFolderName = os.path.join(path, "zielordner")

    # action
    resultNumber = scan_folder(sourceFolderName, targetFolderName)
    print(f"Anzahl kopierter Dateien: {resultNumber}")
