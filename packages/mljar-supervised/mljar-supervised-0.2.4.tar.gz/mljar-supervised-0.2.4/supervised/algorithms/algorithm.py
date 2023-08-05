import uuid


class BaseAlgorithm:
    """
    This is an abstract class.
    All algorithms inherit from BaseAlgorithm.
    """

    algorithm_name = "Unknown"
    algorithm_short_name = "Unknown"

    def __init__(self, params):
        self.params = params
        self.stop_training = False
        self.library_version = None
        self.model = None
        self.uid = params.get("uid", str(uuid.uuid4()))

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

    def update(self, update_params):
        pass

    def copy(self):
        pass

    def save(self, model_file_path):
        pass

    def load(self, model_file_path):
        pass

    def interpret(
        self, X, y, model_file_path, learner_name, target_name=None, class_names=None
    ):
        pass

    # def importance(self, column_names, normalize = True):
    #    pass
