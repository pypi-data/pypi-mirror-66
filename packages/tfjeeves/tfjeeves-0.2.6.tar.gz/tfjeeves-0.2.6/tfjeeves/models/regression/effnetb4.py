from typing import Tuple

from tensorflow import keras
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    GlobalAveragePooling2D,
)
from efficientnet import tfkeras as efn


class ModelEffNetB4:
    def __init__(self, input_shape: Tuple[int], n_targets: int, unfreeze: int = 0, weights: str = "imagenet") -> None:
        self.base_model = efn.EfficientNetB4(
            weights=weights,
            include_top=False,
            input_shape=input_shape,
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils,
        )
        self.layer_1 = GlobalAveragePooling2D()(self.base_model.output)
        self.layer_2 = Dense(2048, activation="relu")(self.layer_1)
        self.layer_3 = Dropout(0.5)(self.layer_2)
        self.layer_4 = Dense(1024, activation="relu")(self.layer_3)
        self.outputs = Dense(n_targets)(self.layer_4)
        self.model = keras.Model(
            inputs=self.base_model.input, outputs=self.outputs, name="effnetb4"
        )
        for i, layer in enumerate(self.model.layers):
            if i + unfreeze - len(self.model.layers) <= 0:
                layer.trainable = False

        print(self.model.summary())

    def plot_model(self, to_file: str = "assets/effnetb4.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'
