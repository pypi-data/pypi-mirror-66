import multiprocessing
import struct
from functools import partial
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

from PIL import Image, ImageFile, ImageOps
from tqdm import tqdm

from . import logger


def presize(*, binary: bytes, mod: Callable = None, target_size: int = 128):
    try:
        img = Image.open(BytesIO(binary))
        img = ImageOps.exif_transpose(img)
        return generate_image_buffer(img=img, mod=mod, target_size=target_size)
    except IOError:
        return None
    except struct.error:
        logger.error(f"Struct error")
        return generate_image_buffer(img=img, mod=mod, target_size=target_size)
    except IndexError:
        logger.error(f"Index error")
        return generate_image_buffer(img=img, mod=mod, target_size=target_size)
    except Exception as err:
        logger.error(f"[{type(err).__name__}]: {err}")


def generate_image_buffer(*, img: Any, mod: Callable = None, target_size: int = 128):
    w, h = img.size
    factor = min([w, h]) / target_size
    resized = img.resize(
        size=(round(w / factor), round(h / factor)), resample=Image.BICUBIC
    )
    resized = resized.convert("RGB")
    if mod:
        resized = mod(resized)
    img_buffer = BytesIO()
    resized.save(img_buffer, format="JPEG")
    return img_buffer.getvalue()


def presize_directory(
    *, src: Path, dest: Path, mod: Callable = None, target_size: int = 128
):
    """
    from tfjeeves.utils import presize_directory

    presize_directory(src="s3", dest="s3-output-128-nearest", target_size=128)
    presize_directory(src="tfjeeves/tests/fixtures/presize", dest="tfjeeves/tests/fixtures/presize-output", target_size=128)
    """
    src = Path(src)
    dest = Path(dest)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    img_suffixes = [".jpg", ".jpeg", ".png"]
    images = [fpath for fpath in src.rglob("*") if fpath.suffix.lower() in img_suffixes]
    logger.info(f"Found {len(images)} images in {src}")
    dest.mkdir(parents=True, exist_ok=True)

    presizer = partial(
        presize_file, src=src, dest=dest, mod=mod, target_size=target_size
    )
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as p:
        outputs = list(tqdm(p.imap(presizer, images), total=len(images)))
    logger.info(
        f"{outputs.count(False)} images ignored, {outputs.count(True)} images resized."
    )


def presize_file(
    image: Path, src: Path, dest: Path, mod: Callable = None, target_size: int = 128
):
    with open(image, "rb") as binaryfile:
        binary = binaryfile.read()
    output = presize(binary=binary, mod=mod, target_size=target_size)
    if output is None:
        return False
    folder = (dest / image.relative_to(src)).parent
    filename = (folder / image.stem).with_suffix(".jpeg")
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "wb") as binaryfile:
        binaryfile.write(output)
    return True
