import json
import time
from pathlib import Path
from typing import Union
from attrdict import AttrDict
import numpy as np
import boto3
import botocore
from botocore.exceptions import ClientError
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import Callback
from hyperdash import Experiment
from tfjeeves.utils.tf_env import TFEnv

PathOrStr = Union[Path, str]
botoClient = botocore.client


class LoggerS3(Callback):
    def __init__(self, config_path: PathOrStr, model_path: PathOrStr, monitor: str = "val_accuracy",) -> None:
        super(LoggerS3, self).__init__()
        self.model_path = model_path
        self.monitor = monitor

        with open(config_path) as config_json_file:
            configs = AttrDict(json.load(config_json_file))
        self.bucket_name = configs.s3.bucket_name
        self.aws_access_key_id = configs.s3.aws_access_key_id
        self.aws_secret_access_key = configs.s3.aws_secret_access_key

    def on_epoch_end(self, epoch: int, logs: dict = {}) -> bool:
        try:
            client = self.create_s3_client()
            path = self.model_path.format(epoch=epoch + 1, **{self.monitor: round(logs.get(self.monitor), 2)})
            model_name = "/".join(path.split("/")[-2:])

            print(f"Uploading {model_name}")
            client.upload_file(path, self.bucket_name, model_name)
        except ClientError as err:
            print(f"Error encountered: {err}")
            return False

        print(f"Model: {model_name} successfully loaded to {self.bucket_name}")
        return True

    def create_s3_client(self) -> botoClient:
        client = boto3.client(
            "s3", aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key,
        )
        print(f"Client has been created for {self.bucket_name}")
        return client


class LoggerHyperDash(Callback):
    def __init__(self, experiment_label: str) -> None:
        super(LoggerHyperDash, self).__init__()
        self.experiment = None
        self.experiment_label = experiment_label
        self.epoch_time_start = None

    def on_train_begin(self, logs: dict = {}) -> None:
        self.exp = Experiment(self.experiment_label)
        TFEnv().log_to_hyperdash(self.exp)

        if hasattr(self.model.optimizer, "lr"):
            lr = (
                self.model.optimizer.lr
                if isinstance(self.model.optimizer.lr, float)
                else K.eval(self.model.optimizer.lr)
            )
            self.exp.param("learning_rate", lr)
        if hasattr(self.model.optimizer, "epsilon"):
            epsilon = (
                self.model.optimizer.epsilon
                if isinstance(self.model.optimizer.epsilon, float)
                else K.eval(self.model.optimizer.epsilon)
            )
            self.exp.param("epsilon", epsilon)
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
                else K.eval(self.model.optimizer.lr)
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


# Adapted from https://github.com/csachs/keras-nvidia-statistics

try:
    import py3nvml.py3nvml as nvml
except ImportError:
    nvml = None


def _bytes_to_megabytes(b_):
    return b_ / 1024.0 / 1024.0


class LoggerNvidia(Callback):
    reportable_values = dict(
        memory_total=lambda handle: _bytes_to_megabytes(nvml.nvmlDeviceGetMemoryInfo(handle).total),
        memory_used=lambda handle: _bytes_to_megabytes(nvml.nvmlDeviceGetMemoryInfo(handle).used),
        memory_free=lambda handle: _bytes_to_megabytes(
            nvml.nvmlDeviceGetMemoryInfo(handle).total - nvml.nvmlDeviceGetMemoryInfo(handle).used
        ),
        temperature=lambda handle: nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU),
        power_state=nvml.nvmlDeviceGetPowerState,
        power_draw=lambda handle: nvml.nvmlDeviceGetPowerUsage(handle) / 1000.0,
        utilization_gpu=lambda handle: nvml.nvmlDeviceGetUtilizationRates(handle).gpu,
        utilization_memory=lambda handle: nvml.nvmlDeviceGetUtilizationRates(handle).memory,
    )

    def __init__(self, report=None, devices=None, quiet=False, always_suffix=False):
        super(self.__class__, self).__init__()

        if nvml is None:
            if not quiet:
                print("Could not load py3nvml, cannot report any nvidia device statistics.")
            report = []
        else:
            nvml.nvmlInit()

            device_count = nvml.nvmlDeviceGetCount()

            if devices is None:
                devices = list(range(device_count))
            else:
                devices = [int(device) for device in devices if 0 <= int(device) < device_count]

            self.devices = devices
            self.deviceHandles = [nvml.nvmlDeviceGetHandleByIndex(device) for device in devices]

            if not quiet:
                for n, handle in enumerate(self.deviceHandles):
                    print("Collecting statistics for device #% 2d: %s" % (n, nvml.nvmlDeviceGetName(handle)))

        if report is None:
            report = ["temperature", "utilization_gpu"]
        elif report == "all":
            report = list(self.reportable_values.keys())

        self.report = report
        self.always_suffix = always_suffix

    def __del__(self):
        if nvml:
            nvml.nvmlShutdown()

    def on_epoch_end(self, epoch: int, logs: dict = None):
        for item in self.report:
            try:
                suffix = handle = None
                for n, handle in enumerate(self.deviceHandles):
                    if len(self.deviceHandles) == 1 and not self.always_suffix:
                        suffix = ""
                    else:
                        suffix = "%02d" % (n,)

                logs["nvidia:" + item + suffix] = np.float32(self.reportable_values[item](handle))
            except nvml.NVMLError as err:
                print("Error trying to read out value from NVML: %r" % (err,))
