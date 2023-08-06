from typing import Tuple

from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import (
    Concatenate,
    Dense,
    Flatten,
    GlobalAveragePooling2D,
    Input,
)


# https://colab.research.google.com/drive/1VgOTzr_VZNHkXh2z9IiTAcEgg5qr19y0#scrollTo=h8N9Vn8XevGx
class ModelResNet50:
    def __init__(self, input_shape: Tuple[int], embedding_size: int) -> None:
        self.resnet50fe = ResNet50(
            weights="imagenet",
            include_top=False,
            input_shape=input_shape,
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils,
        )
        self.pooled = GlobalAveragePooling2D(name="pooling")(self.resnet50fe.output)
        self.flattened = Flatten(name="embedding")(self.pooled)
        self.embeddings = Dense(embedding_size)(self.flattened)

        self.base_model = keras.Model(
            input=self.resnet50fe.input,
            output=self.embeddings,
            name="resnet50base_model",
        )
        for layer in self.base_model.layers:
            layer.trainable = False
        print(self.base_model.summary())

        a = self.base_model.input
        p = Input(shape=input_shape)
        n = Input(shape=input_shape)

        a_emb = self.base_model(a)
        p_emb = self.base_model(p)
        n_emb = self.base_model(n)

        merged_output = Concatenate()([a_emb, p_emb, n_emb])

        self.resnet50triplet = keras.Model(input=[a, p, n], output=[merged_output])
