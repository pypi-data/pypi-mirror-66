from functools import partial
from pathlib import Path
from typing import Tuple, Union

import numpy as np
import tensorflow as tf

from tfjeeves.datasets import ImageDataset
from tfjeeves.triplet.cifar2 import loss
from tfjeeves.utils import import_file


def test_dl(
    dataset: ImageDataset,
    batch_size: int,
    img_height: int,
    img_width: int,
    gpu_count: int,
    num_parallel_calls: int,
    **kwargs,
):

    return (
        tf.data.Dataset.from_tensor_slices(list(zip(dataset.images, dataset.targets)))
        .map(
            partial(
                dataset.read_image_wrapper, img_height=img_height, img_width=img_width,
            ),
            num_parallel_calls=num_parallel_calls,
        )
        .batch(batch_size * gpu_count)
        .prefetch(buffer_size=num_parallel_calls)
    )


def get_preds(
    img_dir: Union[str, Path],
    model_path: Union[str, Path],
    config_path: Union[str, Path],
) -> Tuple[np.array, Tuple[str]]:
    params = import_file(Path(config_path).stem, config_path).params
    inferenceDataset = ImageDataset().from_folder(path=img_dir)
    inferenceDataloader = test_dl(
        dataset=inferenceDataset, cache_path=".", **params.dataloader_common
    )
    model = tf.keras.models.load_model(str(model_path), compile=False)
    model.compile(loss="binary_crossentropy")
    return model.predict(inferenceDataloader), inferenceDataset.images
