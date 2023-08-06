import collections
import itertools
from pathlib import Path
from typing import List, Optional

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from loguru import logger
from sklearn.metrics import pairwise_distances
from tf_explain.core.grad_cam import GradCAM
from tqdm import tqdm

from tfjeeves.datasets import Dataloader, ImageDataset
from tfjeeves.datasets.inference import ModelInference
from tfjeeves.datasets.plotting import fancy_plot
from tfjeeves.utils import batch

AUTOTUNE = tf.data.experimental.AUTOTUNE

dataloader_common_config = {
    "batch_size": 8,
    "img_height": 128,
    "img_width": 128,
    "gpu_count": 1,
    "shuffle_buffer_size": 1000,
    "num_parallel_calls": AUTOTUNE,
}


class ImageStats:
    """
    TODO: Add serialisation and deserialisation methods to this class
    """

    def __init__(self, path: str, shuffle: bool = True):
        self.path = Path(path).expanduser()
        self.mean = tf.constant([0, 0, 0], dtype=tf.float32)
        self.std = tf.constant([0, 0, 0], dtype=tf.float32)
        self.interclass_distance = None
        self.dataset = ImageDataset().from_folder(self.path, shuffle=shuffle)
        label_counts = collections.Counter(self.dataset.labels)
        self.distribution = pd.DataFrame(
            {"label": list(label_counts.keys()), "count": list(label_counts.values())}
        ).sort_values(by=["count"], ascending=False)
        self.size = len(self.dataset.labels)
        self.embeddings = None
        self.distance_matrix = None
        self.inferer = None
        self.model_path = None

    def compute_stats(self):
        """
        Compute channel-wise mean and std for images in a given dataset
        """
        for img in tqdm(self.dataset.images):
            img = self.dataset.read_image(filepath=img)
            m = tf.nn.moments(img, [0, 1])
            self.mean += m[0]
            self.std += m[1]
        self.mean /= self.dataset.length
        self.std /= self.dataset.length
        print(f"final stats: mean - {self.mean}, std - {self.std}")
        # TODO: save the stats somewhere as csv/json
        return self

    def plot_distribution(self, save_path=".", showplot=False):
        """
        Create a plot show the number of images in various classes
        """
        D = self.distribution
        min_class_size = min(D["count"])
        D["minimum"] = min_class_size
        D["count"] -= min_class_size
        bars = D.plot(
            x="label",
            y=["minimum", "count"],
            kind="barh",
            style="ggplot",
            figsize=(20, 40),
            title="Number of images in classes",
            grid=True,
            fontsize=8,
            stacked=True,
        )
        for rect in bars.patches:
            if rect.get_x() == min_class_size:
                height = rect.get_height()
                width = rect.get_width() + min_class_size
                plt.text(
                    width + 12,
                    rect.get_y() + height / 4.0,
                    "%d" % int(width),
                    ha="center",
                    va="bottom",
                )
            else:
                height = rect.get_height()
                width = rect.get_width()
                plt.text(
                    width + 12,
                    rect.get_y() + height / 3.0,
                    "%d" % int(width),
                    ha="center",
                    va="bottom",
                )
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(save_path) / "class_distribution.png", dpi=100)
            if showplot:
                plt.show()
            return self

    def compute_embeddings(
        self,
        model_path,
        dataloader_config: dict = dataloader_common_config,
        bottleneck_index: int = -2,
    ):
        """
        Compute embedding using the given model

        Example:
          cifar10 = ImageStats("~/data-zoo/classification/cifar10/train")
          cifar10.compute_embeddings(model_path="model.h5")
        """
        logger.info("Started computing embeddings...")
        self.model_path = model_path
        self.inferer = ModelInference(model_path=model_path)
        dataloader = Dataloader(**dataloader_config)(dataset=self.dataset)
        self.embeddings = np.array(
            self.inferer.get_bottleneck(dataloader, bottleneck_index).predictions
        )
        logger.info(f"Finished computing embeddings")
        return self

    def compute_class_distance(self):
        """
        Calculates average interclass distance matrix from embeddings
        """
        logger.info("Started computing class distances...")
        indices = {
            cls: np.where(np.array(self.dataset.labels) == cls)[0]
            for cls in self.dataset.CLASS_NAMES
        }
        self.distance_matrix = np.empty(
            [len(self.dataset.CLASS_NAMES), len(self.dataset.CLASS_NAMES)]
        )
        for i, cls1 in tqdm(enumerate(self.dataset.CLASS_NAMES)):
            for j, cls2 in tqdm(enumerate(self.dataset.CLASS_NAMES)):
                self.distance_matrix[i, j] = pairwise_distances(
                    self.embeddings[indices[cls1]], self.embeddings[indices[cls2]]
                ).mean()
        logger.info("Finished computing class distances...")
        return self

    def plot_class_distance(self, save_path="interclass_distance.png"):
        """
        Creates boxplots of average interclass distances
        """

        filtered_distances = []
        for i, _ in enumerate(self.dataset.CLASS_NAMES):
            filtered_distances.append(np.delete(self.distance_matrix[:, i], i))
        df = pd.DataFrame(
            np.array(filtered_distances).transpose(), columns=self.dataset.CLASS_NAMES
        )
        fancy_plot(df.melt(), plot_type="violin", save_path="violin.png")
        fancy_plot(df.melt(), plot_type="box", save_path="box.png")
        return self

    def save(self, save_path="ImageStat.joblib"):
        joblib.dump(
            [
                self.path,
                self.mean,
                self.std,
                self.interclass_distance,
                self.distribution,
                self.size,
                self.embeddings,
                self.distance_matrix,
                self.model_path,
            ],
            filename=save_path,
            compress=3,
        )
        return self

    def load(self, load_path="ImageStat.joblib"):
        (
            self.path,
            self.mean,
            self.std,
            self.interclass_distance,
            self.distribution,
            self.size,
            self.embeddings,
            self.distance_matrix,
            self.model_path,
        ) = joblib.load(load_path)
        logger.info(
            "Note - dataset:ImageDataset(self.path) and inferer:ModelInference(self.model_path) are not loaded."
        )  # TODO: Try and load them!
        return self

    def tf_explainer(
        self,
        model_path: str,
        dataloader_common_config: dict,
        n_images: int,
        output_dir: str,
        category: str,
    ):
        model = ModelInference(model_path=model_path)
        dataset = self.dataset
        mask = [True if label == category else False for label in self.dataset.labels]
        dataset.labels = list(itertools.compress(dataset.labels, mask))
        dataset.images = list(itertools.compress(dataset.images, mask))
        dl = Dataloader(**dataloader_common_config)(dataset=dataset)
        images, targets = dl.get_n_images(n_images)
        self._grad_cam_png(
            model=model.model, images=images, target=targets[0], output_dir=output_dir
        )

    def _grad_cam_png(
        self,
        model: tf.keras.Model,
        images: np.ndarray,
        target: int,
        output_dir: str = ".",
    ):
        explainer = GradCAM()
        for i, image_batch in enumerate(batch(images, 36)):
            grid = explainer.explain(
                validation_data=(image_batch, None), model=model, class_index=target
            )
            explainer.save(grid, output_dir, f"grad_cam_{i + 1}.png")


if __name__ == "__main__":
    # model_path = "cifar10_data/experiment-ymd_2020_04_06-hms_17_04_03/model_keras/experiment-ymd_2020_04_06-hms_17_04_03.h5"
    model_path = "../shop101-classifier-72/tf_servable/v840/1"
    # dataset_path = "cifar10_data/val"
    dataset_path = "shop101cat72/val"
    cifar10 = ImageStats(dataset_path, shuffle=False)
    dataloader_common_config["img_height"] = 256
    dataloader_common_config["img_width"] = 256
    dataloader_common_config["batch_size"] = 16
    cifar10.tf_explainer(
        model_path=model_path,
        dataloader_common_config=dataloader_common_config,
        n_images=10,
        output_dir="grad_cam",
        category="accessories_bags_handbags",
    )
