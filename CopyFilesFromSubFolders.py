import glob
import os
import pathlib
import shutil
from typing import Mapping

import pandas


def main():
    source_folder = pathlib.Path("quellordner")
    target_folder = pathlib.Path("zielordner")

    try:
        process_csv_files_from_source(source_folder, target_folder)

    except FileNotFoundError as error:
        print(f'>> error: {error}')


def process_csv_files_from_source(source: pathlib.Path, target: pathlib.Path) -> None:
    check_if_path_is_folder(path=source)
    create_folder_if_not_exists(path=target)
    csv_source_paths = get_csv_source_paths_in_path_grouped_by_filenames(path=source)
    process_csv_source_paths(csv_source_paths, target)


def check_if_path_is_folder(path: pathlib.Path) -> None:
    if not path.is_dir():
        raise FileNotFoundError(f'folder not found: {path}')


def create_folder_if_not_exists(path: pathlib.Path) -> None:
    os.makedirs(path, exist_ok=True)


def get_csv_source_paths_in_path_grouped_by_filenames(path: pathlib.Path) -> Mapping[str, list[pathlib.Path]]:
    csv_filepaths = load_csv_filepaths_in_path(path)
    return get_source_paths_grouped_by_filenames(filepaths=csv_filepaths)


def load_csv_filepaths_in_path(path: pathlib.Path) -> tuple[pathlib.Path]:
    return tuple(path.glob('**/*time_record*.csv'))


def get_source_paths_grouped_by_filenames(filepaths: tuple[pathlib.Path]) -> Mapping[str, list[pathlib.Path]]:
    source_paths = {}
    for file in map(pathlib.Path, filepaths):
        source_paths.setdefault(file.name, []).append(file)
    return source_paths


def process_csv_source_paths(csv_source_paths: Mapping[str, list[pathlib.Path]], target: pathlib.Path) -> None:
    for filename, filepaths in csv_source_paths.items():
        target_filepath = pathlib.Path(target, filename)
        copy_files_to_target(filepaths, target_filepath)
        print(f">> files copied: {len(filepaths) + 1}")
        save_combined_files(filepaths, target_filepath)


def copy_files_to_target(filepaths: list[pathlib.Path], target_filepath: pathlib.Path) -> None:
    for index, source_file in enumerate(filepaths):
        copy_file_to_target(source_file, target_filepath, index)


def copy_file_to_target(source_file: pathlib.Path, target_filepath: pathlib.Path, index: int) -> None:
    target_csv_file = get_target_csv_file_with_index(target_filepath, index)
    shutil.copy(source_file, target_csv_file)
    print(f'>> copy "{source_file}" to "{target_csv_file}"')


def get_target_csv_file_with_index(target_filepath: pathlib.Path, index: int) -> pathlib.Path:
    return target_filepath.with_suffix(f'.{index + 1}.csv')


def save_combined_files(filepaths: list[pathlib.Path], target_filepath: pathlib.Path) -> None:
    if len(filepaths) == 0:
        return
    target_csv_content, lines_copied = get_combined_csv_files(filepaths)
    print(f'>> total combined lines: {lines_copied}')
    target_filepath.write_text(target_csv_content)
    print(f'>> combine files in: {target_filepath}')
    save_excel_file(csv_file=target_filepath)


def get_combined_csv_files(filepaths: list[pathlib.Path]) -> tuple[str, int]:
    combine = ['']
    for combine[0], file_content in map(get_csv_file_header_and_content, filepaths):
        combine.extend(file_content)
    lines_copied = len(combine) + len(filepaths) - 1
    return str.join('', combine), lines_copied


def get_csv_file_header_and_content(filepath: pathlib.Path) -> tuple[str, list[str]]:
    with open(filepath, mode='r') as file:
        return file.readline(), file.readlines()


def save_excel_file(csv_file: pathlib.Path) -> None:
    excel_file = csv_file.with_suffix('.xlsx')
    pandas.read_csv(csv_file, delimiter=';').to_excel(excel_file)
    print(f'>> save to excel: {excel_file}')


if __name__ == '__main__':
    main()
