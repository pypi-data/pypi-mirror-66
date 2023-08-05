import numpy as np

from cognite.osc.exceptions import MissingTypeNumOrTypeNameException


class PerformanceOpenSet:
    """ Calculate the performance of an open set classifier.
    The setup for calculation the performance measures in a open-set scenario are taken from the paper
    "Nearest neighbors distance ratio open-set classifier", https://link.springer.com/article/10.1007/s10994-016-5610-8
    """

    def __init__(self):
        pass

    def precision_recall(self, true_positives, false_positives, false_negatives, n=None):
        """ Calculate micro-averaging open-set precision, recall and f-measure (mu), and
        macro-averaging open-set precision, recall and f-measure (M) given true_positives,
        false_positives and false_negatives

        Args:
            true_positives (int) : Number of true positives
            false_positives (int) : Number of false positives
            false_negatives (int) : Number of false negatives
            n (int or None) : Dived micro-averaging by n to get macro-averaging
        Returns:
            precision_mu (float) : Micro precision
            recall_mu (float) : Micro recall
            f_mu (float) : Micro f-score
            precision_M (float) : Macro precision
            recall_M (float) : Macro recall
            f_M (float) : Macro f-score
        """
        if n == None:
            l = 1
        else:
            l = n + 1
        if (true_positives + false_positives) == 0:
            precision_mu = 0
            precision_M = 0
        else:
            precision_mu = true_positives / (true_positives + false_positives)
            precision_M = (true_positives / (true_positives + false_positives)) / max((l - 1), 1)
        if (true_positives + false_negatives) == 0:
            recall_mu = 0
            recall_M = 0
        else:
            recall_mu = _mu = true_positives / (true_positives + false_negatives)
            recall_M = (true_positives / (true_positives + false_negatives)) / max((l - 1), 1)
        if (precision_mu + recall_mu) == 0:
            f_mu = 0
            f_M = 0
        else:
            f_mu = 2 * precision_mu * recall_mu / (precision_mu + recall_mu)
            f_M = 2 * precision_M * recall_M / (precision_M + recall_M)

        return precision_mu, recall_mu, f_mu, precision_M, recall_M, f_M

    def overall_performance(self, y_true, y_predicted, lambda_r=0.5):
        """ Calculate overall performance. Assumption: samples with no class (called other or unknown) have value 0
        samples with a classes have value >0

        Args:
            y_true (array-like) : Actual value of the target
            y_predicted (array-like) : Predicted value of target
            lambda_r (float): The parameter that decides the weight given to the accuracy of the known and unknown
                samples in the normalized accuracy
        Returns:
            (dict) : Dictionary with overall performance measurers
        """
        # True positives only consider samples correctly classified as one of the n available classes
        true_positives = sum(y_true[y_predicted > 0] == y_predicted[y_predicted > 0])
        # Flase positives and false negatives also consider false unknown and false known respectively
        false_positives = sum(y_true[y_predicted > 0] != y_predicted[y_predicted > 0])
        false_negatives = sum(y_true[y_true > 0] != y_predicted[y_true > 0])
        precision_mu, recall_mu, f_mu, precision_M, recall_M, f_M = self.precision_recall(
            true_positives=true_positives,
            false_positives=false_positives,
            false_negatives=false_negatives,
            n=len(np.unique(y_true)),
        )
        # Accuracy known samples
        if sum(y_predicted > 0) == 0:
            accuracy_known_samples = 0
        else:
            accuracy_known_samples = true_positives / sum(y_predicted > 0)
        # Accuracy unknown samples
        if sum(y_predicted == 0) == 0:
            accuracy_unknown_samples = 0
        else:
            accuracy_unknown_samples = sum(y_true[y_predicted == 0] == y_predicted[y_predicted == 0]) / sum(
                y_predicted == 0
            )
        # Normalized accuracy
        normalized_accuracy = lambda_r * accuracy_known_samples + (1 - lambda_r) * accuracy_unknown_samples

        values = [
            true_positives,
            false_positives,
            false_negatives,
            precision_mu,
            recall_mu,
            f_mu,
            precision_M,
            recall_M,
            f_M,
            accuracy_known_samples,
            accuracy_unknown_samples,
            normalized_accuracy,
        ]
        keys = [
            "true_positives",
            "false_positives",
            "false_negatives",
            "precision_mu",
            "recall_mu",
            "f_mu",
            "precision_M",
            "recall_M",
            "f_M",
            "accuracy_known",
            "accuracy_unknown",
            "normalized_accuracy",
        ]
        return dict(zip(keys, values))

    def performance_per_type(self, y_true, y_predicted, type_name=None, encoder=None, type_num=None):
        """ Calculate overall performance per type

        Args:
            y_true (array-like) : Actual value of the target in the test set
            y_predicted (array-like) : Predicted value of target
            type_name (string or None) : Name of type
            encoder : Encoder that encodes a type_name to the type_num
            type_num (int) : Number for the type
        Returns:
            (dict) : Dictionary with performance measurers for the type
        """
        if type_num is None:
            if (type_name is None) and (encoder is None):
                raise MissingTypeNumOrTypeNameException("Need type number or type name and label encoder")
            else:
                type_num = encoder[type_name]
        true_positives = sum(y_true[y_predicted == type_num] == y_predicted[y_predicted == type_num])
        false_positives = sum(y_predicted[y_predicted == type_num] != y_true[y_predicted == type_num])
        false_negatives = sum(y_true[y_true == type_num] != y_predicted[y_true == type_num])

        precision_mu, recall_mu, f_mu, precision_M, recall_M, f_M = self.precision_recall(
            true_positives, false_positives, false_negatives
        )
        # Accuracy
        if sum(y_predicted == type_num) == 0:
            accuracy = 0
        else:
            accuracy = true_positives / sum(y_predicted == type_num)

        values = [true_positives, false_positives, false_negatives, precision_mu, recall_mu, f_mu, accuracy]
        keys = ["true_positives", "false_positives", "false_negatives", "precision_mu", "recall_mu", "f_mu", "accuracy"]

        return dict(zip(keys, values))
