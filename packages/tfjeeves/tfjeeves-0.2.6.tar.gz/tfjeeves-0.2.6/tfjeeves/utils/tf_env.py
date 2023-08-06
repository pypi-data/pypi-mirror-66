import tensorflow as tf
from multiprocessing import cpu_count

class TFEnv:
    def __init__(self):
        self.env = {
            "tensorflow": f"{tf.__name__} {tf.version.VERSION}",
            "keras": f"{tf.keras.__name__} {tf.keras.__version__}",
            "COMPILER_VERSION": f"{tf.version.COMPILER_VERSION}",
            "GRAPH_DEF_VERSION": f"{tf.version.GRAPH_DEF_VERSION}",
            "GIT_VERSION": f"{tf.version.GIT_VERSION}",
            "tf.config.optimizer.get_jit()?": f"{tf.config.optimizer.get_jit()}",
            "GRAPH_DEF_VERSION_MIN_CONSUMER": f"{tf.version.GRAPH_DEF_VERSION_MIN_CONSUMER}",
            "GRAPH_DEF_VERSION_MIN_PRODUCER": f"{tf.version.GRAPH_DEF_VERSION_MIN_PRODUCER}",
            "gpu_enabled?": f"{tf.test.is_gpu_available()}",
            "gpu_count": f"{len(tf.config.list_physical_devices('GPU'))}",
            "cpu_count": f"{cpu_count()}"
        }
    
    def __str__(self):
        repr = ""
        for key in self.env.keys():
            repr += f"{key}: {self.env[key]} \n"
        return repr
    
    def log_to_hyperdash(self, exp):
        for key in self.env.keys():
            exp.param(key, self.env[key])

if __name__=="__main__":
    print(TFEnv())