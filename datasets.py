import shutil
from pathlib import Path
from typing import List, Dict
import wget
from os.path import expanduser


def prepare_dataset(url: str, out_path: Path):
    """
    Downloads and unpacks single dataset.
    If dataset already unpacked does nothing.
    If dataset archive already downloaded, will only unpack it.

    Args:
        url (str): url where to download dataset
        out_path (Path): path where to place dataset
    """
    path = expanduser(out_path)
    root_folder = Path(path)
    root_folder.mkdir(parents=True, exist_ok=True)

    file_name = wget.detect_filename(url)
    dataset_name = file_name.split(".")[0]

    out_path = root_folder / dataset_name

    if out_path.exists():
        print(f'{out_path} exists, skipping')
        return out_path
    
    file_path = out_path.parent / file_name
    
    if not file_path.exists():
        print(f'Downloading dataset from {url} to {file_path}')
        wget.download(url=url, out=str(file_path))
    else:
        print(f'{file_path} exists, skipping')

    print(f'Unpacking {file_path} to {out_path}')
    shutil.unpack_archive(filename=str(file_path), extract_dir=str(out_path))

    return out_path


def find_path(where: Path, pattern: Path):
    """
    Finds file/dir pattern in path. Will raise assertion if found != 1 results.

    Args:
        where (Path): path where to search for pattern
        pattern (Path): pattern to search(same as in glob)
    """
    where = Path(where) if isinstance(where, str) else where
    str_pattern = str(pattern)
    results = list(where.rglob(str_pattern))
    results_count = len(results)
    results_str = '\n'.join(map(str, results))
    assert results_count == 1, f'Expected to find exactly one result in {where} ' \
                               f'with pattern {str_pattern}. Found {results_count}:\n{results_str}'
    return results[0]
