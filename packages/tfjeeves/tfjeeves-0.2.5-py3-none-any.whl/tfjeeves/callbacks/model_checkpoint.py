from pathlib import Path
from typing import Any

import tensorflow as tf


def model_checkpoint(
    *,
    model_path: str,
    monitor: str = "val_acc",
    verbose: int = 0,
    save_best_only: bool = False,
    save_weights_only: bool = False,
    mode: str = "auto",
    save_freq: str = "epoch",
) -> Any:
    Path(model_path).parent.mkdir(exist_ok=True, parents=True)
    return tf.keras.callbacks.ModelCheckpoint(
        model_path,
        monitor=monitor,
        verbose=verbose,
        save_best_only=save_best_only,
        save_weights_only=save_weights_only,
        mode=mode,
        save_freq=save_freq,
    )
