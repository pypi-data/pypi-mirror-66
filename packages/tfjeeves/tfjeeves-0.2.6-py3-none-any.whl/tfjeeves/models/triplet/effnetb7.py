from typing import Tuple

from tensorflow import keras
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Flatten,
    GlobalAveragePooling2D,
    Input,
    Lambda,
)
import tensorflow as tf
from efficientnet import tfkeras as efn


class ModelEffNetB7:
    def __init__(self, input_shape: Tuple[int], n_classes: int) -> None:
        self.base_model = efn.EfficientNetB7(
            weights="imagenet",
            include_top=False,
            input_shape=input_shape,
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils,
        )
        self.layer_1 = tf.keras.layers.Dense(1024, activation="relu")(self.base_model.output)
        self.layer_2 = tf.keras.layers.BatchNormalization()(self.layer_1)
        self.layer_3 = tf.keras.layers.Dense(1024, activation="relu")(self.layer_2)
        self.layer_4 = tf.keras.layers.Dropout(0.5)(self.layer_3)
        self.layer_5 = tf.keras.layers.Dense(1024, activation="relu")(self.layer_4)
        self.network = keras.Model(
            inputs=self.base_model.input, outputs=self.layer_normalize, name="effnetb7"
        )
        self.layer_normalize = Lambda(lambda x: tf.math.l2_normalize(x, axis=1))(
            self.network.output
        )
        self.network_normalized = keras.Model(
            inputs=self.base_model.input, outputs=self.layer_normalize, name="effnetb7"
        )
        for layer in self.base_model.layers:
            layer.trainable = False

        # Define the tensors for the three input images
        anchor_input = Input(input_shape, name="anchor_input")
        positive_input = Input(input_shape, name="positive_input")
        negative_input = Input(input_shape, name="negative_input")

        # Generate the encodings (feature vectors) for the three images
        encoded_a = self.network(anchor_input)
        encoded_p = self.network(positive_input)
        encoded_n = self.network(negative_input)
        embedding = tf.concat([encoded_a, encoded_p, encoded_n], axis=1)

        # Connect the inputs with the outputs
        self.model = keras.Model(
            inputs=[anchor_input, positive_input, negative_input], outputs=[embedding]
        )
        print(self.model.summary())

    def plot_model(self, to_file: str = "assets/effnetb7.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'
