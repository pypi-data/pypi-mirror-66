import numpy as np
from pymization.cds import CDS


class Solver:
    """Main class of the package. Solves pre-defined optimization problems.
    """

    def __init__(self, model_name=None):
        self.model_name = model_name
        self.nodes = None
        self.model = None

    def load_data_csv(self, path_file, skip_rows=0):
        self.nodes = np.genfromtxt(path_file, delimiter=",", skiprows=skip_rows)

    def load_data_from_matrix(self, matrix):
        self.nodes = np.asarray(matrix)

    def _handle_model_name(self, model_name):
        if model_name is not None:
            self.model_name = model_name
        if self.model_name is None:
            raise RuntimeError("There wasn't any model defined")

    def run(self, model_name=None):
        self._handle_model_name(model_name)
        self._instance_by_name()
        self.model.run()

    def load_model(self, model=None):
        self._handle_model_name(model)
        self._instance_by_name()

    def _instance_by_name(self):
        if self.nodes is None:
            raise RuntimeError("First load the data using load_data_csv")
        instance_helper = {"CDS": CDS(self.nodes)}
        if self.model_name not in instance_helper:
            raise RuntimeError("Algorithm is not yet implemented")
        self.model = instance_helper[self.model_name]
