import tensorflow as tf
from tensorflow.keras import backend as K


class TripletLoss:
    def __init__(self, margin=1.0, distance="euclidean", output_type="tripletloss"):
        self.margin = margin
        self.distance = distance
        self.output_type = output_type

    @tf.function()
    def __call__(self, y_true, y_pred):
        embedding_size = int(y_pred.shape[1] / 3)
        anchor = y_pred[:, :embedding_size]
        positive = y_pred[:, embedding_size: 2 * embedding_size]
        negative = y_pred[:, 2 * embedding_size:]

        if self.distance == "euclidean":
            d_a_p = tf.reduce_sum(
                tf.square(tf.subtract(anchor, positive)), 1
            )
            if self.output_type == "d_a_p":
                return d_a_p
            d_a_n = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), 1)
            if self.output_type == "d_a_n":
                return d_a_n
            basic_loss = tf.add(tf.subtract(d_a_p, d_a_n), self.margin)
            loss = tf.reduce_mean(tf.maximum(basic_loss, 0.))
            if self.output_type == "tripletloss":
                return loss
        if self.distance == "cosine":
            d_a_p = K.losses.cosine_proximity(anchor, positive)
            if self.output_type == "d_a_p":
                return d_a_p
            d_a_n = K.losses.cosine_proximity(anchor, negative)
            if self.output_type == "d_a_n":
                return d_a_n
            loss = K.clip(d_a_n - d_a_p + self.margin, 0, None)
            if self.output_type == "tripletloss":
                return loss
        raise ValueError("TripletLoss was initialised with wrong values!!!")
