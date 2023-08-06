import random
import itertools
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import tensorflow as tf

from ..utils import logger
from ..utils.non_image import get_all_images

PathOrStr = Union[Path, str]
StrList = Sequence[str]


class Dataset(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class ImageDataset(Dataset):
    def __init__(
        self, id: str = f"experiment-{str(datetime.now().strftime('ymd_%Y_%m_%d-hms_%H_%M_%S'))}", logger=logger,
    ):
        """
        This class exposes several methods to create a dataset from raw input data.
        """
        self.id = id
        self.logger = logger
        self.path = None

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return f"ImageDataset @ {self.path.as_posix()}"

    # @tf.function
    def read_image(self, *, filepath: PathOrStr, img_width: int = None, img_height: int = None) -> tf.Tensor:
        """
        Reads image file from a path, resizes it and returns a tensor
        """
        img = tf.io.read_file(filepath)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)  # puts data in [0, 1) range
        if (img_width is not None) and (img_height is not None):
            img = tf.image.resize(img, (img_width, img_height))
        return img

    def from_folder(self, path: PathOrStr = ".", shuffle: bool = True, extensions: StrList = None) -> "ImageDataset":
        """Create an `ImageDataset` using images in `path` with correct `extensions`
        """
        path = Path(path)
        if path.is_dir() and path.exists():
            self.path = path
            imgs_n_labels = [(path.as_posix(), path.parts[-2]) for path in list(path.glob("*/*"))]
            if shuffle:
                random.shuffle(imgs_n_labels)
            self.images, self.labels = zip(*imgs_n_labels)
            self.length = len(imgs_n_labels)
            self.CLASS_NAMES = sorted(np.unique([item.name for item in path.glob("*")]))
            self.class_map = tf.lookup.StaticHashTable(
                initializer=tf.lookup.KeyValueTensorInitializer(
                    keys=tf.constant(self.CLASS_NAMES), values=tf.constant(list(range(len(self.CLASS_NAMES)))),
                ),
                default_value=tf.constant(-1),
                name="class_weight",
            )
            self.n_classes = len(self.CLASS_NAMES)
            self.logger.info(f"ImageDataset {self.id} updated from_folder {str(self.path)}")
            self.logger.info(f"Length of updated ImageDataset: {self.length}")
            self.logger.info(f"No of classes in updated ImageDataset: {self.n_classes}")
            self.logger.info(f"Class names in updated ImageDataset: {self.CLASS_NAMES}")
            self.data = imgs_n_labels
            return self
        else:
            raise ValueError(f"{path} is not a valid directory.")
        return self

    def from_csv(self, path: PathOrStr = ".", extensions: StrList = None) -> "ImageDataset":
        """
        Create an `ImageDataset` using images in the csv with correct `extensions`
        """
        path = Path(path)
        if path.exists():
            self.path = path
            df = pd.read_csv(path)
            self.logger.info(f"Creating ImageDataset {self.id} from_csv {str(self.path)}")
            return self.from_df(df=df)
        else:
            raise ValueError(f"{path} does not exist!")

    def from_df(self, df: pd.DataFrame) -> "ImageDataset":
        """
        Create an `ImageDataset` using dataframe
        """
        assert all([col in df for col in ["path", "label"]]), "Data should have both `path` & `label` as columns"

        self.images = df["path"].to_list()
        self.labels = df["label"].to_list()
        self.CLASS_NAMES = np.sort(np.array(list(df["label"].unique())))
        self.length = len(self.images)
        self.n_classes = len(self.CLASS_NAMES)
        self.logger.info("########## ImageDataset update status ##########")
        self.logger.info(f"Length of updated ImageDataset: {self.length}")
        self.logger.info(f"No of classes in updated ImageDataset: {self.n_classes}")
        self.logger.info(f"Class names in updated ImageDataset: {self.CLASS_NAMES}")
        self.logger.info("#################################################")
        self.data = list(zip(self.images, self.labels))
        return self

    def show_batch(self) -> "ImageDataset":
        return self

    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, np.array]:
        """
        Reads in the payload of image file and label, and returns image and label data suitable for training
        """
        return (
            self.read_image(filepath=payload[0], img_width=img_width, img_height=img_height),
            payload[1] == np.array(self.CLASS_NAMES),
        )


class ImageDatasetRegression(ImageDataset):
    def from_df(self, df: pd.DataFrame) -> "ImageDatasetRegression":
        try:
            self.images = df["path"].tolist()
            self.labels = df["target"].tolist()
            self.n_classes = len(df["target"].iloc[0].split("-"))
            self.length = len(self.images)
            self.logger.info(f"Length of updated ImageDataset: {self.length}")
            self.logger.info(f"No of targets in updated ImageDataset: {self.n_classes}")
            return self
        except KeyError:
            logger.exception(f"Input dataFrame should contain both image `path` and `target` columns")

    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, np.array]:
        return (
            self.read_image(filepath=payload[0], img_width=img_width, img_height=img_height),
            tf.map_fn(fn=tf.strings.to_number, elems=tf.strings.split(payload[1], "-"), dtype=tf.float32,),
        )


class ImageDatasetTriplet(ImageDataset):
    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, tf.Tensor]:
        """
        Reads in the payload of image file and label, and returns image and label data suitable for training
        """
        return (
            self.read_image(filepath=payload[0], img_width=img_width, img_height=img_height,),
            self.class_map.lookup(payload[1]),
        )


class ImageDatasetTriplet2(ImageDataset):
    def from_folder_random(self, path: PathOrStr, triplets_per_class: int):
        self.from_folder(path=path)
        self.length = triplets_per_class * self.n_classes
        labels = np.array(self.labels)
        images = np.array(self.images)
        self.labels = []
        self.images = []
        rng = np.random.default_rng()
        for label in self.CLASS_NAMES:
            images_cat = images[labels == label]
            labels_non_cat = labels[labels != label]
            images_non_cat = images[labels != label]
            for i in range(triplets_per_class):
                cat_idx = rng.choice(images_cat.shape[0], 2, replace=False)
                non_cat_idx = rng.choice(images_non_cat.shape[0], 1, replace=False)
                images_triplet = tuple((images_cat[cat_idx].tolist() + images_non_cat[non_cat_idx].tolist()))
                labels_triplet = (label, label, labels_non_cat[non_cat_idx][0])
                self.images.append(images_triplet)
                self.labels.append(labels_triplet)
        return self

    def from_folder_offline(self, path: PathOrStr):
        images = get_all_images(directory=path, recursive=True)
        index = [int(file.stem.split("_")[0]) for file in images]
        image_type = [file.stem.split("_")[1] for file in images]
        category = [file.stem.split("_")[2] for file in images]
        image_df = pd.DataFrame({"index": index, "image_type": image_type, "category": category, "path": images})
        image_df = image_df.pivot_table(
            index=["index"], columns=["image_type"], values=["path", "category"], aggfunc="first"
        )
        image_df.columns = ["_".join(col).strip() for col in image_df.columns]
        self.length = image_df.shape[0]
        self.images = []
        self.labels = []
        for row in image_df.itertuples():
            self.images.append((str(row.path_anchor), str(row.path_positive), str(row.path_negative)))
            self.labels.append((row.category_anchor, row.category_positive, row.category_negative))
        self.CLASS_NAMES = sorted(set(list(itertools.chain.from_iterable(self.labels))))
        self.n_classes = len(self.CLASS_NAMES)
        self.path = path
        return self

    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[Tuple[str, str, str], Tuple[str, str, str]], img_width: int, img_height: int
    ) -> Tuple[Tuple[tf.Tensor, tf.Tensor, tf.Tensor], Tuple[tf.Tensor, tf.Tensor, tf.Tensor]]:
        """
        Reads in the payload of image file and label, and returns image and label data suitable for training
        """
        return (
            (
                self.read_image(filepath=payload[0][0], img_width=img_width, img_height=img_height),
                self.read_image(filepath=payload[0][1], img_width=img_width, img_height=img_height),
                self.read_image(filepath=payload[0][2], img_width=img_width, img_height=img_height),
            ),
            (tf.constant([0, 0, 0])),
        )
