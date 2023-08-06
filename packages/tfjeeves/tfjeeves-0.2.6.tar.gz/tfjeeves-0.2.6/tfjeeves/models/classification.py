from typing import Tuple

from tensorflow import keras
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D, GlobalAveragePooling2D

from tensorflow.keras.applications import MobileNetV2, ResNet101, ResNet50
from efficientnet import tfkeras as efn


def validate_integer(x):
    if not isinstance(x, int):
        raise ValueError(f"Expected to have integer values. You provided {x}")
    return x


class ClassificationBaseline:
    def __init__(self, model_name="none"):
        supported = ["none", "mobilenetv2", "resnet50", "resnet101", "efficientnetb4", "efficientnetb7"]
        print("Pre-trained models supported by `ClassificationBaseline` are:\n")
        print(f"{supported}")
        if model_name not in supported:
            raise ValueError(f"The specified value ({model_name}) for pre-trained model is not supported")
        self.model_name = model_name
        if self.model_name == "mobilenetv2":
            self.model_func = MobileNetV2
        if self.model_name == "resnet50":
            self.model_func = ResNet50
        if self.model_name == "resnet101":
            self.model_func = ResNet101
        if self.model_name == "efficientnetb4":
            self.model_func = efn.EfficientNetB4
        if self.model_name == "efficientnetb7":
            self.model_func = efn.EfficientNetB7

    def __call__(self, input_shape: Tuple[int, int, int], n_classes: int):
        self.input_shape = input_shape
        self.n_classes = n_classes
        self.load_pretrained().extend_model()
        return self

    def __str__(self):
        return str(self.model.summary())

    def remove_last_layer(self):
        self.model = keras.Model(inputs=[self.model.input], outputs=[self.model.layers[-2].output])
        return self

    def change_trainability(self, action="freeze", start=0, end=-1):
        start = validate_integer(start)
        end = validate_integer(end)
        new_trainable_status = False if action == "freeze" else True
        for layer in enumerate(self.model.layers[start:end]):
            layer.trainable = new_trainable_status
        print(self.model.summary())
        return self

    def load_checkpoint(self):
        pass

    def load_pretrained(self):
        if self.model_name == "none":
            input_image = Input(shape=self.input_shape)
            layer1 = Conv2D(128, (3, 3), activation="relu")(input_image)
            layer2 = MaxPool2D(pool_size=(2, 2))(layer1)
            layer3 = Conv2D(256, (3, 3), activation="relu")(layer2)
            layer4 = MaxPool2D(pool_size=(2, 2))(layer3)
            self.base_model = keras.Model(inputs=[input_image], outputs=[layer4])
            self.model = self.base_model
            return self
        self.base_model = self.model_func(
            weights="imagenet",
            include_top=False,
            input_shape=self.input_shape,
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils,
        )
        self.model = self.base_model
        return self

    def extend_model(self, remove_last_layer=False):
        layer_1 = GlobalAveragePooling2D()(self.model.output)
        layer_2 = Flatten()(layer_1)
        layer_3 = Dense(256, activation="relu", name="bottleneck")(layer_2)
        self.outputs = Dense(self.n_classes, activation="softmax", name="final")(layer_3)
        self.model = keras.Model(inputs=self.model.input, outputs=self.outputs)
        print(self.model.summary())
        return self

    def plot_model(self, to_file: str = "model_architechture.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'


if __name__ == "__main__":
    x = ClassificationBaseline("mobilenetv2")
    x = x((224, 224, 3), 10)
    x = x.extend_model()
    print(x)
