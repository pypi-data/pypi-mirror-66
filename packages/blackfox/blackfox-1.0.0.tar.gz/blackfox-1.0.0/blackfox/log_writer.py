from datetime import datetime
import sys

class LogWriter(object):
    """LogWriter provides logging capabilities for an ongoing Black Fox optimization.

    Parameters
    ----------
    file : str
        Optional file or sys.stdout used for logging

    """

    def __init__(self, file=sys.stdout):
        self.log_file = file

    def write_neural_network_statues(self, id, statuses, metric):
        status = statuses[-1]
        msg = ("%s - %s, "
               "Generation: %s/%s, "
               "Validation set %s: %f, "
               "Training set %s: %f, "
               "Epoch: %d, "
               "Optimization Id: %s") % (
            datetime.now(),
            status.state,
            status.generation,
            status.total_generations,
            metric,
            status.validation_set_error,
            metric,
            status.training_set_error,
            status.epoch,
            id
        )
        self.write_string(msg)

    def write_random_forest_statues(self, id, statuses, metric):
        status = statuses[-1]
        msg = ("%s - %s, "
               "Generation: %s/%s, "
               "Validation set %s: %f, "
               "Training set %s: %f, "
               "Optimization Id: %s") % (
            datetime.now(),
            status.state,
            status.generation,
            status.total_generations,
            metric,
            status.validation_set_error,
            metric,
            status.training_set_error,
            id
        )
        self.write_string(msg)

    def write_xgboost_statues(self, id, statuses, metric):
        self.write_random_forest_statues(id, statuses, metric)

    def write_string(self, msg):
        if isinstance(self.log_file, str):
            with open(self.log_file, mode='a', encoding='utf-8', buffering=1) as f:
                f.write(msg+'\n')
        else:
            self.log_file.write(msg+'\n')
            self.log_file.flush()
