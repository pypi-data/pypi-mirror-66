from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Tuple, Union

import numpy as np
import tensorflow as tf

from tfjeeves.core.dataset import ImageDataset, ImageDatasetTriplet2
from tfjeeves.utils import logger

PathOrStr = Union[Path, str]


class Dataloader:
    # TODO: Create loader_once by default, it needed no config
    def __init__(
        self,
        batch_size: int,
        img_height: int,
        img_width: int,
        shuffle_buffer_size: int,
        gpu_count: int,
        num_parallel_calls: int,
        id: str = f"experiment-{str(datetime.now().strftime('ymd_%Y_%m_%d-hms_%H_%M_%S'))}",
        logger=logger,
    ) -> None:
        """
        Creates a data loader from an ImageDataset instance, creates random batches to train the model.
        """
        self.gpu_count = gpu_count
        self.num_parallel_calls = num_parallel_calls
        self.shuffle_buffer_size = shuffle_buffer_size
        self.batch_size = batch_size
        self.img_height = img_height
        self.img_width = img_width
        self.input_shape = (img_height, img_width, 3)
        self.logger = logger

    def __call__(self, *, dataset: ImageDataset, cache_path: PathOrStr = ".", augment_func=None) -> "Dataloader":
        """
        Converts the dataloader instance into a callable
        """
        self.dataset = dataset
        self.cache_path = Path(cache_path)
        self.n_classes = dataset.n_classes

        if self.dataset.path:
            self.logger.info(
                f"Dataloader created using ImageDataset: {self.dataset.id}, from path: {self.dataset.path}"
            )

        loader = tf.data.Dataset.from_tensor_slices(self.dataset.data).map(
            partial(self.dataset.read_image_wrapper, img_height=self.img_height, img_width=self.img_width,),
            num_parallel_calls=self.num_parallel_calls,
        )
        loader_once = tf.data.Dataset.from_tensor_slices(self.dataset.data).map(
            partial(self.dataset.read_image_wrapper, img_height=self.img_height, img_width=self.img_width,),
            num_parallel_calls=self.num_parallel_calls,
        )

        loader = loader.cache(self.cache_path.as_posix()).shuffle(buffer_size=self.shuffle_buffer_size).repeat()

        if augment_func is not None:
            loader = loader.map(augment_func, num_parallel_calls=self.num_parallel_calls)
            loader_once = loader_once.map(augment_func, num_parallel_calls=self.num_parallel_calls)

        loader = loader.batch(self.batch_size * self.gpu_count).prefetch(buffer_size=self.num_parallel_calls)
        loader_once = loader_once.batch(self.batch_size * self.gpu_count).prefetch(buffer_size=self.num_parallel_calls)

        self.loader = loader
        self.loader_once = loader_once
        return self

    def get_n_images(self, n: int):
        images = []
        targets = []
        for i, batch in enumerate(self.loader_once):
            image, target = batch
            images.append(image.numpy())
            targets.append(target.numpy())
            if (i + 1) * self.batch_size >= n:
                break
        images = np.concatenate(images)[:n]
        targets = np.concatenate(targets)[:n]
        return images, targets.argmax(axis=1)

    def __str__(self) -> str:
        return f"Dataloader for Dataset: {self.dataset}"


class DataloaderTriplet(Dataloader):
    def __call__(self, *, dataset: ImageDatasetTriplet2, cache_path: PathOrStr = ".") -> "Dataloader":
        """
        Converts the dataloader instance into a callable
        """
        self.dataset = dataset
        self.cache_path = Path(cache_path)
        self.n_classes = dataset.n_classes

        self.logger.info(f"Dataloader created using ImageDataset: {self.dataset.id}, from path: {self.dataset.path}")

        self.loader = (
            tf.data.Dataset.from_tensor_slices(list(zip(self.dataset.images, self.dataset.labels)))
            .map(
                partial(self.dataset.read_image_wrapper, img_height=self.img_height, img_width=self.img_width,),
                num_parallel_calls=self.num_parallel_calls,
            )
            .shuffle(buffer_size=self.shuffle_buffer_size)
            .repeat()
            .batch(batch_size=self.batch_size)
            .prefetch(buffer_size=self.num_parallel_calls)
        )
        return self


if __name__ == "__main__":
    from tfjeeves.datasets.dataset import ImageDatasetTriplet2

    ds = ImageDatasetTriplet2().from_folder_offline("cifar10_triplets/train")
    dl = DataloaderTriplet(
        batch_size=128,
        img_height=128,
        img_width=128,
        shuffle_buffer_size=1000,
        gpu_count=1,
        num_parallel_calls=tf.data.experimental.AUTOTUNE,
    )(dataset=ds)
