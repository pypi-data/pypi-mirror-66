from typing import Tuple

from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D


class ModelMobileNetV2:
    def __init__(self, input_shape: Tuple[int], n_targets: int) -> None:
        self.base_model = MobileNetV2(
            weights="imagenet",
            include_top=False,
            input_shape=input_shape,
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils,
        )
        self.layer_1 = GlobalAveragePooling2D()(self.base_model.output)
        self.layer_2 = Flatten()(self.layer_1)
        self.layer_3 = Dense(256, activation="relu")(self.layer_2)
        self.layer_4 = Dropout(0.5)(self.layer_3)
        self.layer_5 = Dense(256)(self.layer_4)
        self.outputs = Dense(n_targets, activation="softmax")(self.layer_5)
        self.model = keras.Model(
            inputs=self.base_model.input, outputs=self.outputs, name="mobilenetv2"
        )
        print(self.model.summary())

    def plot_model(self, to_file: str = "assets/mobilenetv2.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'
