import mimetypes
from multiprocessing import Pool
from pathlib import Path
from typing import List, Union

import click
from PIL import Image
from tqdm import tqdm


def get_all_images(*, directory: Union[str, Path], recursive: bool) -> List[Path]:
    directory = check_valid_directory(directory=directory)
    if recursive:
        files = Path(directory).rglob("*")
    else:
        files = Path(directory).glob("*")
    img_suffixes = [".jpg", ".jpeg", ".png"]
    files = [
        fpath for fpath in files if (fpath.is_file() and (fpath.suffix in img_suffixes))
    ]
    print(f"Found {len(files)} files in the directory: {directory.resolve()}")
    return files


def get_all_files(*, directory: Union[str, Path], recursive: bool) -> List[Path]:
    directory = check_valid_directory(directory=directory)
    if recursive:
        files = Path(directory).rglob("*")
    else:
        files = Path(directory).glob("*")
    files = [fpath for fpath in files if fpath.is_file()]
    print(f"Found {len(files)} files in the directory: {directory.resolve()}")
    return files


def check_valid_directory(*, directory: Union[str, Path]) -> Path:
    directory = Path(directory)
    if not (directory.exists() and directory.is_dir()):
        raise ValueError(
            "{} doesn't exist or isn't a valid directory!".format(directory.resolve())
        )
    return directory


def check_image_validity(filepath):
    mtype = mimetypes.MimeTypes().guess_type(filepath)[0]
    if mtype is None:
        return (filepath, "no-mimetype-found")
    if not mtype.lower() in ["image/jpeg", "image/jpeg", "image/png"]:
        print(f"File doesn't match Image MimeType: {str(filepath.resolve())}")
        return (filepath, "wrong-mimetype")
    image_obj = Image.open(filepath)
    image_obj.verify()
    if not str(image_obj.format).lower() in ["jpg", "jpeg", "png"]:
        print(f"File doesn't have valid Image Extension: {filepath}")
        return (filepath, "wrong-extension")
    return (filepath, "no-problem-detected")


@click.command()
@click.option(
    "-d",
    "--directory",
    required=True,
    help='directories for which thumbnails will be generated, seperated by space, eg: "dir1/dir2 dir3"',
)
@click.option(
    "-w", "--workers", default=1, help="no of cpus to use for multiprocessing"
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    help="whether to recursively look for files",
)
def check(directory, workers, recursive):
    files = get_all_files(directory=directory, recursive=recursive)
    # files_str = [str(fpath) for fpath in files]

    with Pool(processes=workers) as pool:
        # results = [pool.apply_async(check_image_validity, file) for file in files]
        results = list(tqdm(pool.imap(check_image_validity, files), total=len(files)))

    for result in results:
        filename, status = result
        if status in ["wrong-mimetype", "wrong-extension", "no-mimetype-found"]:
            print("##########")
            print(f"filename: {filename}")
            print()
            print(f"issue: {status}")
            print("##########")


if __name__ == "__main__":
    check()
