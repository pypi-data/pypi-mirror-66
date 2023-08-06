import tensorflow as tf
from loguru import logger
from tensorflow import keras


class ClassifierTriplet:
    def __init__(self, classifier_path: str):
        self.classifier_path = classifier_path
        logger.info(f"Loading classifier at: {classifier_path}")
        self.classifier = tf.keras.models.load_model(filepath=self.classifier_path)
        if hasattr(self.classifier, "model"):
            self.classifier = self.classifier.model
        self.classifier = tf.keras.Model(inputs=[self.classifier.input], outputs=[self.classifier.layers[-2].output])
        self.layer_index = {layer.name: i for i, layer in enumerate(self.classifier.layers)}
        for layer in self.classifier.layers[:self.layer_index["top_activation"] + 2]:
            layer.trainable = False
        print(f"Classifier: {self.classifier.summary()}")

    def create_triplet_model(self):
        # Define the tensors for the three input images
        anchor_input = keras.layers.Input(self.classifier.input_shape[1:], name="anchor_input")
        positive_input = keras.layers.Input(self.classifier.input_shape[1:], name="positive_input")
        negative_input = keras.layers.Input(self.classifier.input_shape[1:], name="negative_input")

        # Generate the encodings (feature vectors) for the three images
        encoded_a = self.classifier(anchor_input)
        encoded_p = self.classifier(positive_input)
        encoded_n = self.classifier(negative_input)
        embedding = tf.concat([encoded_a, encoded_p, encoded_n], axis=1)

        # Connect the inputs with the outputs
        self.model = keras.Model(
            inputs=[anchor_input, positive_input, negative_input], outputs=[embedding]
        )
        return self

    def plot_model(self, to_file: str = "assets/triplet_model.png") -> None:
        keras.utils.plot_model(
            self.model,
            to_file=to_file,
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=300,
        )  # 'LR' vs 'TB'
