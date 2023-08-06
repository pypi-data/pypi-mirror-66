import time
from multiprocessing import cpu_count

import tensorflow as tf
from hyperdash import Experiment
from tensorflow import keras
from tensorflow.keras.callbacks import Callback


class LoggerHyperDash(Callback):
    def __init__(self, experiment_label: str) -> None:
        super(LoggerHyperDash, self).__init__()
        self.experiment = None
        self.experiment_label = experiment_label
        self.epoch_time_start = None

    def on_train_begin(self, logs: dict = {}) -> None:
        self.exp = Experiment(self.experiment_label)
        self.exp.param("tensorflow", f"{tf.__name__} {tf.__version__}")
        self.exp.param("keras", f"{keras.__name__} {keras.__version__}")
        self.exp.param("gpu_enabled?", tf.test.is_gpu_available())
        # self.exp.param("logical_devices", f"{tf.config.list_logical_devices()}")
        # self.exp.param("physical_devices", f"{tf.config.list_physical_devices()}")
        # self.exp.param("visible_devices", f"{tf.config.get_visible_devices()}")
        self.exp.param(
            "gpu_count", f"{len(tf.config.experimental.list_physical_devices('GPU'))}"
        )
        self.exp.param("cpu_count", f"{cpu_count()}")
        # self.exp.param("physical_gpu_devices", f"{tf.config.list_physical_devices('GPU')}")

        if hasattr(self.model.optimizer, "lr"):
            lr = (
                self.model.optimizer.lr
                if isinstance(self.model.optimizer.lr, float)
                else keras.backend.eval(self.model.optimizer.lr)
            )
            self.exp.param("learning_rate_start", lr)
        if hasattr(self.model.optimizer, "epsilon"):
            epsilon = (
                self.model.optimizer.epsilon
                if isinstance(self.model.optimizer.epsilon, float)
                else keras.backend.eval(self.model.optimizer.epsilon)
            )
            self.exp.param("epsilon_start", epsilon)
        # sum_list = ["\n#################################\n"]
        # self.model.summary(line_length=40, print_fn=sum_list.append)
        # summary = '\n'.join(sum_list)
        # self.exp.param('model_summary', summary +
        # "\n#################################\n")

    def on_train_end(self, logs: dict = {}) -> None:
        self.exp.end()

    def on_epoch_begin(self, epoch: int, logs: dict = {}) -> None:
        if hasattr(self.model.optimizer, "lr"):
            lr = (
                self.model.optimizer.lr
                if isinstance(self.model.optimizer.lr, float)
                else keras.backend.eval(self.model.optimizer.lr)
            )
            self.exp.metric("learning_rate_epoch_start", lr)
        self.epoch_time_start = time.time()

    def on_epoch_end(self, epoch: int, logs: dict = {}) -> None:
        train_acc = logs.get("accuracy")
        train_loss = logs.get("loss")
        val_acc = logs.get("val_accuracy")
        val_loss = logs.get("val_loss")
        time_taken = time.time() - self.epoch_time_start
        if val_acc:
            self.exp.metric("val_accuracy", val_acc)
        if val_loss:
            self.exp.metric("val_loss", val_loss)
        if train_acc:
            self.exp.metric("train_acc", train_acc)
        if train_loss:
            self.exp.metric("train_loss", train_loss)
        if train_loss and val_acc:
            self.exp.metric("generalization_loss", train_loss - val_loss)
        if time_taken:
            self.exp.metric("epoch duration", time_taken)
