from typing import Tuple

from tensorflow import keras
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D


class ModelBaseline:
    def __init__(self, input_shape: Tuple[int], n_targets: int) -> None:
        self.input_shape = input_shape
        self.inputs_image = Input(shape=self.input_shape)
        self.layer1 = Conv2D(256, (3, 3), activation="relu")(self.inputs_image)
        self.layer2 = MaxPool2D(pool_size=(2, 2))(self.layer1)
        self.layer3 = Conv2D(256, (3, 3), activation="relu")(self.layer2)
        self.layer4 = MaxPool2D(pool_size=(2, 2))(self.layer3)
        self.layer5 = Conv2D(512, (3, 3), activation="relu")(self.layer4)
        self.layer6 = MaxPool2D(pool_size=(2, 2))(self.layer5)
        self.layer7 = Conv2D(512, (3, 3), activation="relu")(self.layer6)
        self.layer8 = MaxPool2D(pool_size=(2, 2))(self.layer7)
        self.layer9 = Flatten()(self.layer8)
        self.layer10 = Dense(256)(self.layer9)
        self.layer11 = Dropout(0.5)(self.layer10)
        self.layer12 = Dense(256)(self.layer11)
        self.outputs = Dense(n_targets)(self.layer12)

        self.model = keras.Model(
            inputs=self.inputs_image, outputs=self.outputs, name="baseline"
        )
        print(self.model.summary())

    def plot_model(self, to_file: str = "assets/baseline.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'
