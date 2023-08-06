import tensorflow as tf


def tf_env():
    print(f"TF version: {tf.__version__}")
    print(f"{'*'*20}")
    print(f"List of logical devices: {tf.config.list_logical_devices()}")
    print(f"List of physical devices: {tf.config.list_physical_devices()}")
    print(f"List of visible devices: {tf.config.get_visible_devices()}")
    print(f"List of physical GPU devices: {tf.config.list_physical_devices('GPU')}")
    return None
