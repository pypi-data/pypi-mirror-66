import shutil
from pathlib import Path

import numpy as np
from loguru import logger

from tfjeeves.datasets.dataset import ImageDataset


class TripletClassGenerator:
    def __init__(self, *, triplets_per_class: int):
        self.triplets_per_class = triplets_per_class

    def from_dataset_random(self, *, dataset: ImageDataset):
        """
        Generates triplets randomly by sampling 2 images from a class and one image from a different class
        """
        labels = np.array(dataset.labels)
        images = np.array(dataset.images)
        rng = np.random.default_rng()
        self.triplets = []
        for label in dataset.CLASS_NAMES:
            images_cat = images[labels == label]
            labels_non_cat = labels[labels != label]
            images_non_cat = images[labels != label]
            for i in range(self.triplets_per_class):
                cat_idx = rng.choice(images_cat.shape[0], 2, replace=False)
                non_cat_idx = rng.choice(images_non_cat.shape[0], 1, replace=False)
                images_triplet = tuple(
                    (
                        images_cat[cat_idx].tolist()
                        + images_non_cat[non_cat_idx].tolist()
                    )
                )
                labels_triplet = (label, label, labels_non_cat[non_cat_idx][0])
                self.triplets.append((images_triplet, labels_triplet))

    def copy_triplets(self, *, dst: Path):
        logger.info(f"Moving {len(self.triplets)} triplets to : {dst}")
        dst.mkdir(exist_ok=True, parents=True)
        for i, (images, labels) in enumerate(self.triplets):
            anchor, positive, negative = images
            anchor_label, positive_label, negative_label = labels
            dst_anchor = dst / f"{i + 1:04d}_anchor_{anchor_label}_{Path(anchor).name}"
            dst_pos = dst / f"{i + 1:04d}_positive_{positive_label}_{Path(positive).name}"
            dst_neg = dst / f"{i + 1:04d}_negative_{negative_label}_{Path(negative).name}"
            shutil.copy(anchor, dst_anchor)
            shutil.copy(positive, dst_pos)
            shutil.copy(negative, dst_neg)
