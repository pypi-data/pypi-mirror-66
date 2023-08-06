from tensorflow.keras.callbacks import Callback


class StopTrainingOnSuccess(Callback):
    """Stop training when target accuracy is reached
    Arguments:
        `target_acc`: Training will be stopped once this accuracy is 
        reached. Default value is 0.9.
    """

    def __init__(self, target_acc: float = 0.9):
        self._target_acc = target_acc

    def on_epoch_end(self, epoch: int, logs: dict = {}):
        current_accuracy = logs.get("acc")
        print(
            f"\n[StopTrainingOnSuccess] Current accuracy: \
            {100*current_accuracy}% (target accuracy: {self._target_acc})"
        )
        if current_accuracy > self._target_acc:
            print(f"\n[StopTrainingOnSuccess] Stopping training!")
            self.model.stop_training = True


class StopTrainingOnOverfitting(Callback):
    """Stop training when overfittting is detected
    This requires val_acc to be monitored
    Arguments:
        `maxdiff`: Maximum difference to be tolerated between Training 
        and Validation loss. Default value is 0.1.
    """

    def __init__(self, maxdiff: float = 0.1):
        self._maxdiff = maxdiff

    def on_train_begin(self, logs: dict = {}):
        self._divergences = []

    def on_epoch_end(self, epoch: int, logs: dict = {}):
        current_divergence = logs.get("val_loss") - logs.get("loss")
        self._divergences.append(current_divergence)
        print(
            f"\n[StopTrainingOnOverfitting] Current divergence \
            (val_loss-train_loss): {current_divergence} \
            (max allowed divergence: {self._maxdiff})"
        )
        if current_divergence > self._maxdiff:
            print(f"\n[StopTrainingOnOverfitting] Stopping training!")
            self.model.stop_training = True
