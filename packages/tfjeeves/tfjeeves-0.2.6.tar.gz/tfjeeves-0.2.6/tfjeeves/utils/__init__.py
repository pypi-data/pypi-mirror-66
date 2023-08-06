import hashlib
import re
import shutil
import sys
from importlib import util
from pathlib import Path
from typing import Union

import boto3
import pandas as pd
from loguru import logger
from tqdm import tqdm

from .disk2df import disk2df, disk2df_cifar100_superclass
from .presize import presize_directory, presize_file
from .tf_env import TFEnv


def import_pyscript(modname: str, path: Union[str, Path]):
    """Import module (modname) from path python3.6+
    """
    spec = util.spec_from_file_location(modname, path)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fmt = "<yellow>[{time:YYYY-MM-DD_HH:mm:ss}]</yellow><cyan>[{level}]</cyan><magenta>[{file}]</magenta><red>[{function}]</red><blue>[{line}]</blue>: <green>[{message}]</green>"
logger.remove()
logger.add(
    sink=sys.stdout, format=fmt, level="INFO", backtrace=True, diagnose=True, serialize=False,
)


def download_from_s3(*, aws_profile: str, bucket: str, s3_keys: str, dest: str = Union[str, Path]):
    """
    import pandas as pd
    from tfjeeves.utils import download_from_s3
    
    images = pd.read_csv("sql-lab.csv")
    download_from_s3(aws_profile="vistaetl", bucket="etl-out",     s3_keys=images.loc[0:999, "s3_path"], dest="s3")
    """
    session = boto3.Session(profile_name=aws_profile)
    s3_client = session.client("s3")
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    for s3_key in tqdm(s3_keys):
        (dest / s3_key).parent.mkdir(parents=True, exist_ok=True)
        s3_client.download_file(Bucket=bucket, Key=s3_key, Filename=(str(dest / s3_key)))


def _remove_sizechart_discards(image_path, target_path, csv_path):
    """
    from tfjeeves.utils import _remove_sizechart_discards
    _remove_sizechart_discards("s3", "s3-reject", "sql-lab.csv")
    """
    image_path = Path(image_path)
    target_path = Path(target_path)
    images = pd.read_csv(csv_path)
    print(f"Original shape: {images.shape}")
    images = images[images.is_sizechart.notnull() | images.is_discarded.notnull()]
    print(f"New shape: {images.shape}")
    all_images = images.apply(
        lambda row: Path(str(row.category_name))
        / str(row.subcategory_name)
        / str(row.master_name)
        / (str(row.catalog_id) + "_" + str(row.product_id) + "_" + str(row.image_id) + ".jpeg"),
        axis=1,
    )

    counter = 0
    for image in tqdm(all_images):
        print(f"{str(image_path / image)}")
        if (image_path / image).exists():
            (target_path / image).parent.mkdir(parents=True, exist_ok=True)
            (image_path / image).replace(target_path / image)
            counter += 1
    print(f"Total images moved: {counter}")


def _private_download_fn(
    *, csv_path="sql-lab.csv", aws_profile="vistaetl", bucket="etl-out", target_root="s3",
):
    """
    from tfjeeves.utils import _private_download_fn
_private_download_fn()
    """
    images = pd.read_csv(csv_path)
    print(f"Original shape: {images.shape}")
    images = images[images.is_sizechart.isnull()]
    images = images[images.is_discarded.isnull()]
    print(f"New shape: {images.shape}")
    images["path"] = images.apply(
        lambda row: Path(str(row.category_name))
        / str(row.subcategory_name)
        / str(row.master_name)
        / (str(row.catalog_id) + "_" + str(row.product_id) + "_" + str(row.image_id) + ".jpeg"),
        axis=1,
    )
    session = boto3.Session(profile_name=aws_profile)
    s3_client = session.client("s3")
    target_root = Path(target_root)
    all_images = list(zip(images["s3_path"], images["path"]))
    for image in tqdm(all_images):
        s3_path = image[0]
        target_path = image[1]
        if (target_root / target_path).exists():
            continue
        try:
            (target_root / target_path).parent.mkdir(parents=True, exist_ok=True)
            s3_client.download_file(Bucket=bucket, Key=s3_path, Filename=(str(target_root / target_path)))
        except:
            with open("failed_downloads.txt", "a") as f:
                f.write(str(target_root / target_path))
                f.write("\n")


def update_categories(src: Path, dst: Path) -> None:
    rename_cats(src, dst)
    remove_cats(src, dst)
    add_update_cats(src, dst)


def rename_cats(src: Path, dst: Path) -> None:
    for dir in src.iterdir():
        if dir.stem.startswith("RENAME"):
            original_cat, renamed_cat = get_rename_cats(dir.stem)
            (dst / original_cat).rename(dst / renamed_cat)
            logger.info(f"Renamed folder: {dst / original_cat} to {dst / renamed_cat}")


def get_rename_cats(dir_name: str):
    original_cat, renamed_cat = dir_name.replace("RENAME", "").strip("-").split("-to-")
    return original_cat, renamed_cat


def remove_cats(src: Path, dst: Path) -> None:
    before = folder_count(dst)
    for dir in src.iterdir():
        if dir.is_dir():
            if dir.stem.startswith("REMOVE-COMPLETE"):
                cat = get_category_name(dir.stem)
                logger.info(f"Removing category {cat} from {dst}")
                target_dir = dst / cat
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                else:
                    logger.error(f"Can't delete directory, not found: {target_dir}")
            elif dir.stem.startswith("REMOVE-PARTIAL"):
                cat = get_category_name(dir.stem)
                target_dir = dst / cat
                logger.info(f"Removing some files from {target_dir}")
                before_file = file_count(target_dir)
                for item in dir.iterdir():
                    if item.is_file():
                        target = target_dir / item.name
                        if target.exists():
                            target.unlink()
                        else:
                            logger.error(f"File not found: {target}")
                logger.info(
                    f"File counts in {target_dir} before: {before_file}, after: {file_count(target_dir)}, "
                    f"files removed: {before_file - file_count(target_dir)}"
                )
    logger.info(f"Folder counts before: {before}, after: {folder_count(dst)}")


def add_update_cats(src: Path, dst: Path) -> None:
    before = folder_count(dst)
    for item in src.iterdir():
        if item.is_dir():
            if item.stem.startswith("ADD"):
                cat = get_category_name(item.stem)
                target_dir = Path(f"{dst}/{cat}")
                target_dir.mkdir(exist_ok=True, parents=True)
                logger.info(f"Adding/updating category {cat} in {dst}")
                before_file = file_count(target_dir)
                for file in item.iterdir():
                    if file.is_file():
                        target = (target_dir / get_file_name(file=file)).with_suffix(file.suffix)
                        shutil.copy(file, target)
                logger.info(
                    f"File counts in {target_dir} before: {before_file}, after: {file_count(target_dir)}, "
                    f"files added: {file_count(target_dir) - before_file}"
                )
    logger.info(f"Folder counts in {dst} before: {before}, after: {folder_count(dst)}")


def folder_count(dir: Path) -> int:
    return sum([1 if item.is_dir() else 0 for item in dir.iterdir()])


def file_count(dir: Path) -> int:
    return sum([1 if item.is_file() else 0 for item in dir.iterdir()])


def get_category_name(dir_name: str):
    return re.sub(r"(ADD|NEW|REMOVE|SHOP101|ATLAS|COMPLETE|PARTIAL)", "", dir_name).strip("-")


def get_file_name(file: Path) -> str:
    fname = file.name
    shop101_pattern = re.compile(r"(?P<catalog_id>\d+)_(?P<product_id>\d+)_(?P<image_id>\d+)\..+")
    hash_id_pattern = re.compile(r"\A[a-z0-9]+_(?P<image_id>[a-z0-9]+)\..+")
    only_id_pattern = re.compile(r"\A(?P<image_id>[a-z0-9]+)\..+")
    shop101_match = re.match(shop101_pattern, fname)
    if shop101_match:
        return f"{hasher(file)}_" + shop101_match.group("image_id")
    hash_id_match = re.match(hash_id_pattern, fname)
    if hash_id_match:
        return f"{hasher(file)}_" + hash_id_match.group("image_id")[:12]
    only_id_match = re.match(only_id_pattern, fname)
    if only_id_match:
        return f"{hasher(file)}_" + only_id_match.group("image_id")[:12]
    logger.error(f"No image id found for {file}")
    return f"{hasher(file)}_" + fname[:12]


def hasher(file):
    with open(file, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:12]


def batch(iterable, n=100):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]
