import inspect
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Sequence, Union

import loguru
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from plot_keras_history import plot_history
from tensorflow.keras.callbacks import CSVLogger

from tfjeeves.utils import logger
from tfjeeves.core import Dataloader

PathOrStr = Union[Path, str]
NPArrayMask = np.ndarray
NPImage = np.ndarray
FilePathList = Sequence[Path]
Floats = Union[float, Sequence[float]]
ImgLabel = str
ImgLabels = Sequence[ImgLabel]
NPArrayableList = Sequence[Union[np.ndarray, list]]
NPArrayList = Sequence[np.ndarray]
NPArrayMask = np.ndarray
StrList = Sequence[str]
OptStrList = Optional[StrList]

Logger = loguru._logger.Logger
Callback = tf.keras.callbacks.Callback
Callbacks = Sequence[Callback]
Loss = Union[str, Any]
Metrics = Sequence[Union[str, Any]]
# https://github.com/fastai/fastai/blob/450bdd1de7ecb532d94e35590275d0f1d5ebb3f0/fastai/core.py

cifar_stats = ([0.491, 0.482, 0.447], [0.247, 0.243, 0.261])
imagenet_stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
mnist_stats = ([0.131], [0.308])

Optimiser = Union[str, Any]


class Experiment:
    def __config_path__(self, experiment_path: PathOrStr) -> None:
        if Path(experiment_path).exists():
            self.experiment_path = Path(experiment_path) / self.id
            self.experiment_path.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError(f"Provided experiment_path {str(experiment_path)} doesn't exist!")
        self.cache_path = self.experiment_path / "cache"
        self.cache_path.mkdir(exist_ok=True)
        self.cache_path_train = self.cache_path / "train.tfcache"
        self.cache_path_val = self.cache_path / "val.tfcache"
        self.cache_path_test = self.cache_path / "test.tfcache"

        self.model_save_path_keras = self.experiment_path / "model_keras"
        self.model_save_path_tf = self.experiment_path / "model_tf"
        self.model_save_path_keras.mkdir(exist_ok=True)
        self.model_save_path_tf.mkdir(exist_ok=True)

    def __config_logging__(self, logger: Logger) -> None:
        logger.add(
            sink=self.experiment_path / "loguru.log",
            format=fmt,
            level="INFO",
            backtrace=True,
            diagnose=True,
            serialize=False,
        )
        self.logger = logger

    def __config_dataloaders__(self, dataloaders: Sequence[Dataloader]):
        if len(dataloaders) == 3:
            self.train_dl, self.val_dl, self.test_dl = dataloaders
            self.TEST_FLAG = True
        elif len(dataloaders) == 2:
            self.train_dl, self.val_dl = dataloaders
        else:
            raise ValueError(f"Expected 2 or 3 dataloaders, received {len(dataloaders)})")
        if hasattr(self.train_dl.dataset, "CLASS_NAMES"):
            if set(self.train_dl.dataset.CLASS_NAMES) != set(self.val_dl.dataset.CLASS_NAMES):
                raise ValueError("Some classes in train are missing in val")
            if self.TEST_FLAG and (set(self.train_dl.dataset.CLASS_NAMES) != set(self.test_dl.dataset.CLASS_NAMES)):
                raise ValueError("Some classes in train are missing in test")

    def __init__(
        self,
        *,
        id: str = f"experiment-{str(datetime.now().strftime('ymd_%Y_%m_%d-hms_%H_%M_%S'))}",
        dataloaders: List[Dataloader],
        logger: Logger = logger,
        experiment_path: PathOrStr = ".",
    ) -> None:
        """
        This class manages training, evaluation and saving the model after training. Also saves the history of training.
        """
        self.id = id
        self.__config_path__(experiment_path)
        # self.__config_logging__(logger)
        self.logger = logger
        self.TEST_FLAG = False
        if isinstance(dataloaders, list):
            self.__config_dataloaders__(dataloaders)
        else:
            raise ValueError(f"dataloaders is expected to be a list!")

    def __str__(self) -> str:
        return f"Experiment @ {self.id}"

    def train(
        self,
        modelobj,
        optimizer: Optimiser,
        loss: Loss,
        metrics: Metrics,
        epochs: int,
        callbacks: Callbacks = [],
        weights_path: Optional[str] = None,
    ) -> "Experiment":
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.epochs = epochs
        self.callbacks = callbacks

        from tfjeeves.models.classification import ClassificationBaseline

        if isinstance(modelobj, ClassificationBaseline):
            self.MODEL = modelobj(input_shape=self.train_dl.input_shape, n_classes=self.train_dl.dataset.n_classes,)

            if weights_path:
                logger.info(f"Loading weights from: {weights_path}")
                self.MODEL.model.load_weights(weights_path)
        else:
            self.MODEL = modelobj

        self.MODEL.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        self.logger.info(f"train_dl path: {self.train_dl.dataset.path}")
        self.logger.info(f"val_dl path: {self.val_dl.dataset.path}")
        self.logger.info(f"test_dl path: {self.test_dl.dataset.path}")
        self.logger.info(f"train_dl image_count: {self.train_dl.dataset.length}")
        self.logger.info(f"val_dl image_count: {self.val_dl.dataset.length}")
        self.logger.info(f"test_dl image_count: {self.test_dl.dataset.length}")
        if hasattr(self.train_dl.dataset, "CLASS_NAMES"):
            self.logger.info(f"train_dl CLASS_NAMES: {self.train_dl.dataset.CLASS_NAMES}")
            self.logger.info(f"val_dl CLASS_NAMES: {self.val_dl.dataset.CLASS_NAMES}")
            self.logger.info(f"test_dl CLASS_NAMES: {self.test_dl.dataset.CLASS_NAMES}")

        self.history = self.MODEL.model.fit(
            self.train_dl.loader,
            validation_data=self.val_dl.loader,
            steps_per_epoch=self.train_dl.dataset.length // self.train_dl.batch_size,
            validation_steps=self.val_dl.dataset.length // self.val_dl.batch_size,
            callbacks=callbacks + [CSVLogger(self.experiment_path / "history.csv")],
            epochs=self.epochs,
        )
        self.save_model_keras(self.id + ".h5")
        self.save_model_tf()
        self.plot_training_history()
        self.plot_training_history2()
        return self

    def evaluate(self) -> "Experiment":
        self.test_scores = self.MODEL.model.evaluate(
            self.test_dl.loader, steps=self.test_dl.dataset.length // self.test_dl.batch_size, verbose=2,
        )
        self.logger.info(f"Test loss: {self.test_scores[0]}")
        self.logger.info(f"Test accuracy: {self.test_scores[1]}")
        return self

    def save_model_keras(self, filename: str) -> "Experiment":
        self.MODEL.model.save(self.model_save_path_keras / filename)
        self.logger.info(f"(keras format) model saved to {self.model_save_path_keras / filename}")
        return self

    def save_model_tf(self) -> "Experiment":
        self.MODEL.model.save(self.model_save_path_tf.as_posix(), save_format="tf")
        self.logger.info(f"(tf format) model saved to {self.model_save_path_tf.as_posix()}")
        return self

    def plot_training_history(self) -> "Experiment":
        history = pd.read_csv(self.experiment_path / "history.csv")
        plot_history(history, path=self.experiment_path / "history.png")  # Use self.history?
        plt.close()
        self.logger.info(f"Training history plotted to {self.experiment_path / 'history.png'}")
        return self

    def plot_training_history2(self) -> "Experiment":
        plot_history(self.history.history, path=self.experiment_path / "history2.png")  # Use self.history?
        plt.close()
        self.logger.info(f"Training history2 plotted to {self.experiment_path / 'history2.png'}")
        return self

    def retrain(self) -> "Experiment":
        return self
