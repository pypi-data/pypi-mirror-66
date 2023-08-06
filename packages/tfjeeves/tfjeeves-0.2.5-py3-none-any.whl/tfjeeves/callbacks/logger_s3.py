import json
from pathlib import Path
from typing import Union

import boto3
import botocore
from attrdict import AttrDict
from botocore.exceptions import ClientError
from tensorflow.keras.callbacks import Callback

PathOrStr = Union[Path, str]
botoClient = botocore.client


class LoggerS3(Callback):
    def __init__(
        self,
        config_path: PathOrStr,
        model_path: PathOrStr,
        monitor: str = "val_accuracy",
    ) -> None:
        super(UploadModel, self).__init__()
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
            path = self.model_path.format(
                epoch=epoch + 1, **{self.monitor: round(logs.get(self.monitor), 2)}
            )
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
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        print(f"Client has been created for {self.bucket_name}")
        return client
