import os
import shutil
import glob
from typing import Optional


def scan_folder(source: str, target: str) -> None:
    source_files = find_csv_files(source)
    if source_files is None:
        return
    copy_files_to_target(files=source_files, target=target)
    print(f'>> combine\n{combine_csv_files(files=source_files)}')


def create_folder_if_not_exists(path_name: str) -> None:
    os.makedirs(path_name, exist_ok=True)


def find_csv_files(path_name: str) -> Optional[list[str]]:
    if not os.path.isdir(path_name):
        print(f'>> error: folder not found: {path_name}')
        return
    source_glob = os.path.join(path_name, '**/*time_record*.csv')
    return glob.glob(source_glob, recursive=True)


def copy_files_to_target(files: list[str], target: str) -> None:
    create_folder_if_not_exists(target)
    for index, source_file in enumerate(files):
        print(f'>> copy {source_file}')
        source_filename = f'{index + 1}_' + os.path.basename(source_file)
        target_file = os.path.join(target, source_filename)
        shutil.copy(source_file, target_file)
    print(f">> files copied: {len(files)}")


def combine_csv_files(files: list[str]) -> str:
    combine = ['']
    for file in files:
        file_header, file_content = get_csv_file_header_and_content(filename=file)
        combine[0] = file_header
        combine.extend(file_content)
    return str.join('', combine)


def get_csv_file_header_and_content(filename: str) -> tuple[str, list[str]]:
    with open(filename, mode='r') as file:
        header = file.readline()
        content = file.readlines()
        return header, content


if __name__ == '__main__':
    path = "."
    sourceFolderName = os.path.join(path, "quellordner")
    targetFolderName = os.path.join(path, "zielordner")

    scan_folder(sourceFolderName, targetFolderName)
