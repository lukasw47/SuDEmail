import os
import pathlib
import shutil
import glob
from typing import Optional

import pandas


def process_csv_files_from_source(source: str, target: str) -> None:
    source_files = find_csv_files(source)
    if source_files is None:
        return
    copy_files_to_target(source_files, target)
    save_combined_files(source_files, target)


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
    target_file = get_target_file_with_index(source_file, target, index)
    shutil.copy(source_file, target_file)


def get_target_file_with_index(source_file: str, target: str, index: int) -> pathlib.Path:
    return get_target_file(source_file, target).with_suffix(f'.{index + 1}.csv')


def save_combined_files(source_files: list[str], target) -> None:
    if len(source_files) == 0:
        return
    target_file = get_target_file(source_file=source_files[0], target=target)
    target_csv_content = get_combined_csv_files(source_files)
    target_file.write_text(target_csv_content)
    print(f'>> combine files in: {target_file}')
    save_excel_file(csv_file=target_file)


def save_excel_file(csv_file: pathlib.Path) -> None:
    excel_file = csv_file.with_suffix('.xlsx')
    pandas.read_csv(csv_file).to_excel(excel_file)
    print(f'>> combine files in: {excel_file}')


def get_target_file(source_file: str, target: str) -> pathlib.Path:
    source_filename = os.path.basename(source_file)
    return pathlib.Path(target, source_filename)


def get_combined_csv_files(source_files: list[str]) -> str:
    combine = ['']
    for combine[0], file_content in map(get_csv_file_header_and_content, source_files):
        combine.extend(file_content)
    return str.join('', combine)


def get_csv_file_header_and_content(source_file: str) -> tuple[str, list[str]]:
    with open(source_file, mode='r') as file:
        header, content = file.readline(), file.readlines()
        return header, content


if __name__ == '__main__':
    source_folder = "quellordner"
    target_folder = "zielordner"

    process_csv_files_from_source(source_folder, target_folder)
