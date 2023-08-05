from pymization.algorithms import Algorithms
import numpy as np
import logging


class CDS(Algorithms):
    def __init__(self, nodes=None):
        description = "blabla"
        super().__init__("CDS", description)
        self.nodes = nodes
        self.n_nodes = 0
        if nodes is not None:
            self.n_nodes = self.nodes.shape[1]
            self.n_jobs = self.nodes.shape[0]
        self.final_sequence = []
        self.objetive_function = np.Infinity
        self.first_mock_machine = []
        self.second_mock_machine = []
        self.first_nodes_set = []
        self.second_nodes_set = []

    def run(self):
        self.objetive_function = np.Infinity
        for i in range(self.n_nodes - 1):  # permutation numbers
            self.first_mock_machine, self.second_mock_machine = [], []
            self.first_node_set, self.second_node_set = [], []
            self.get_sets(i)
            logging.debug(
                f"M1: {self.first_mock_machine} | M2: {self.second_mock_machine} "
            )
            logging.debug(
                f"Set1: {self.first_node_set} | Set2: {self.second_node_set} "
            )
            self.first_node_set = sorted(
                self.first_node_set, key=lambda key: key["time"],
            )
            self.second_node_set = sorted(
                self.second_node_set, key=lambda key: key["time"], reverse=True
            )
            logging.debug(
                f"Sorted 1: {self.first_node_set} | Sorted 2: {self.second_node_set}"
            )
            self.min_makespan(
                jobs_sequence_dict=list(self.first_node_set + self.second_node_set)
            )
        print(
            f"Best seq: {self.final_sequence} | Objective function: {self.objetive_function}"
        )

    def get_sets(self, permutation):
        """Get two different sets of 'Fake' machines to use Johnson's algorithm
        
        Arguments:
            permutation {int} -- Number of permutation. K=..
        """
        for index_job in range(self.n_jobs):
            self.first_mock_machine.append(
                np.sum(self.nodes[index_job][:(permutation)])
            )
            self.second_mock_machine.append(
                np.sum(self.nodes[index_job])
                - np.sum(self.nodes[index_job][:(permutation)])
            )
            if self.first_mock_machine[index_job] < self.second_mock_machine[index_job]:
                self.first_node_set.append(
                    {"index": index_job, "time": self.first_mock_machine[index_job]}
                )
            else:
                self.second_node_set.append(
                    {"index": index_job, "time": self.second_mock_machine[index_job]}
                )

    def _update_objective_function(self, time_job, seq):
        if self.objetive_function > time_job[-1]:
            self.objetive_function = time_job[-1]
            self.final_sequence = seq.copy()

    @staticmethod
    def _job_dictionary_to_sequence(job_seq_dic):
        return [job["index"] for job in job_seq_dic]

    def min_makespan(self, jobs_sequence=None, jobs_sequence_dict=None):
        """Calculate min makespan for job sequences given nodes.
           Disclaimer: Does not get all permutations in equal cases.
        Keyword Arguments:
            jobs_sequence {list} -- List of the sorted index of jobs (Johnson's algorithm) (default: {None}))
            jobs_sequence_dict {list} -- List of dictionaries {'index': 0, 'time': time_of_job} used to debug  (default: {None})
        """
        if jobs_sequence_dict is not None:
            jobs_sequence = self._job_dictionary_to_sequence(jobs_sequence_dict)
        time_previous_job = [0] * self.n_jobs
        time_previous_job[0] = self.nodes[jobs_sequence[0]][0]
        for i in range(1, self.n_nodes):
            time_previous_job[i] = (
                self.nodes[jobs_sequence[0]][i] + time_previous_job[i - 1]
            )
        time_job = [0] * self.n_nodes
        iterSecuencia = iter(jobs_sequence)
        next(iterSecuencia)
        for _, job in enumerate(iterSecuencia):
            time_job[0] = time_previous_job[0] + self.nodes[job][0]
            for j in range(1, self.n_nodes):
                if time_previous_job[j] >= time_job[j - 1]:
                    time_job[j] = self.nodes[job][j] + time_previous_job[j]
                else:
                    time_job[j] = self.nodes[job][j] + time_job[j - 1]
            time_previous_job = time_job.copy()
        self._update_objective_function(time_job, jobs_sequence)
