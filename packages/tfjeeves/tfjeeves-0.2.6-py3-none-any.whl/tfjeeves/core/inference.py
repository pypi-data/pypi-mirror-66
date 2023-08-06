import tensorflow as tf
from loguru import logger

from tfjeeves.core import Dataloader, ImageDataset

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
if len(gpu_devices) > 0:
    tf.config.experimental.set_memory_growth(gpu_devices[0], True)


class ModelInference:
    def __init__(self, model_path):
        self.model_path = model_path
        logger.info(f"Loading model: {model_path}")
        self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
        if hasattr(self.model, "model"):
            self.model = self.model.model
        self.model.compile(loss="binary_crossentropy")

    def get_preds(self, dataloader):
        """
        pass in dataloader using the appropriate datasets. Eg:
        for triplets:
        dataset = ImageDatasetTriplet().from_folder(path=img_dir)
        dataloader = Dataloader(**dataloader_params)(dataset)
        for classification:
        dataloader = Dataloader(**dataloader_params)(dataset=ImageDataset().from_folder(path))
        """
        self.predictions = self.model.predict(dataloader.loader_once)
        return self

    def get_bottleneck(self, dataloader, bottleneck_index: int = -2):
        model = tf.keras.Model(inputs=[self.model.input], outputs=[self.model.layers[bottleneck_index].output],)
        self.predictions = model.predict(dataloader.loader_once)
        return self


if __name__ == "__main__":
    from configs.cifar10 import params

    inference = ModelInference(
        model_path="cifar10_data/experiment-ymd_2020_04_06-hms_17_04_03/model_keras/experiment-ymd_2020_04_06-hms_17_04_03.h5"
    )
    dataset = ImageDataset().from_folder("cifar10_data/test")
    dataloader = Dataloader(**params.dataloader_common)(dataset=dataset)
    inference.get_bottleneck(dataloader, -2)
    print(inference.predictions[0])
    print(inference.predictions.shape)
