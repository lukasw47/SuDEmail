import os
import pathlib
import shutil
import glob
from typing import Optional


def scan_folder(source: str, target: str) -> None:
    source_files = find_csv_files(source)
    if source_files is None:
        return
    copy_files_to_target(source_files=source_files, target=target)
    print(f'>> combine\n{combine_csv_files(files=source_files)}')


def find_csv_files(path_name: str) -> Optional[list[str]]:
    if not os.path.isdir(path_name):
        print(f'>> error: folder not found: {path_name}')
        return
    source_glob = os.path.join(path_name, '**/*time_record*.csv')
    return glob.glob(source_glob, recursive=True)


def copy_files_to_target(source_files: list[str], target: str) -> None:
    create_folder_if_not_exists(target)
    for index, source_file in enumerate(source_files):
        copy_file_to_target(index, source_file, target)
    print(f">> files copied: {len(source_files)}")


def create_folder_if_not_exists(path_name: str) -> None:
    os.makedirs(path_name, exist_ok=True)


def copy_file_to_target(index: int, source_file: str, target: str) -> None:
    print(f'>> copy {source_file}')
    target_filename = get_target_filename(index, source_file, target)
    shutil.copy(source_file, target_filename)


def get_target_filename(index: int, source_file: str, target: str) -> pathlib.Path:
    source_filename = os.path.basename(source_file)
    return pathlib.Path(target, source_filename).with_suffix(f'_{index + 1}.csv')


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
