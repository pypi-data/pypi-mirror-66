import multiprocessing
from collections import Counter

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import ParameterGrid

from cognite.osc.performance_open_set import PerformanceOpenSet


class ElementsOpenSetNearestNeighbors:
    """ Create an Open Set Nearest Neighbors classifier
    """

    def __init__(self):
        pass

    def predict(self, X_train, y_train, x_predict, threshold, k, compute_confidence=False, unknown_value=0):
        """ Predict y for one sample with feature values x_predict
        Args:
            X_train (numpy ndarray) : Array of feature values for the training data
            y_train (numpy array) : Array of class for training data
            x_predict (numpy ndarray) : Array of feature values for sample to predict class
            threshold (float) : If distance ratio is above threshold, the sample gets class unknown_value
            k (int) : Number of neighbors (samples) to look for the most common class among.
            compute_confidence (bool) : If True compute confidence
            unknown_value: The value to return as the class if ratio is larger than threshold
        Returns:
            (value or list) : If compute_confidence is False either unknown_value or predicted class. If
                compute_confidence is True list of unknown_value or predicted class, predicted confidence and ratio.
        """
        # create list for distances and targets
        distances = np.sqrt(np.sum(np.square(x_predict - X_train), axis=1))
        distances = np.transpose(np.vstack((distances, y_train)))

        df_distances = pd.DataFrame(distances)
        df_distances.columns = ["distance", "class"]
        # sort the dataframe
        df_distances = df_distances.sort_values(by=["distance"]).reset_index(drop=True)

        # Find the samples that are the closeset to the sample and the sample
        # that is the closest to the sample and is in a different group.
        neighbor_t = df_distances.loc[0, :]
        neighbor_u = df_distances[df_distances["class"] != neighbor_t["class"]].iloc[0]
        # Compute nearest neighbor distance ratio
        if neighbor_u.distance == 0:
            ratio = threshold + 1
        else:
            ratio = neighbor_t.distance / neighbor_u.distance

        if ratio >= threshold:
            # If ratio is larger than threshold classify as 'unknown'
            if compute_confidence:
                # Calculate confidence of a sample being unknown as max(1, threshold/ratio-1)
                return [unknown_value, min(1, ratio / threshold - 1), ratio]
            else:
                return unknown_value
        else:
            if compute_confidence:
                # Find the most commen class among the k nearest neighbors
                # Use a weighted sum of w times confidence of the class (num from most common class divided by k) and
                # (1-w) times confidence in the sample being known (ratio/threshold)
                counter = Counter(df_distances.loc[0 : k - 1, "class"]).most_common(1)[0]
                confidence_class = counter[1] / k
                confidence_known = ratio / threshold
                weight_confidence_class = 0.8
                return [
                    counter[0],
                    weight_confidence_class * confidence_class + (1 - weight_confidence_class) * confidence_known,
                    ratio,
                ]
            else:
                return Counter(df_distances.loc[0 : k - 1, "class"]).most_common(1)[0][0]

    def k_nearest_neighbor(self, X_train, y_train, X_predict, threshold, k, compute_confidence, unknown_value=0):
        """ Predict class for all samples with feature values X_predict in parallel
        Args:
            X_train (numpy ndarray) : Array of feature values for the training data
            y_train (numpy array) : Array of class for training data
            x_predict (numpy ndarray) : Array of feature values for samples to predict classes
            threshold (float) : If distance ratio is above threshold, the sample gets class unknown_value
            k (int) : Number of neighbors (samples) to look for the most common class among.
            compute_confidence (bool) : If True compute confidence
            unknown_value: The value to return as the class if ratio is larger than threshold
        Returns:
            (list of values or lists) : If compute_confidence is False either unknown_value or predicted class. If
                compute_confidence is True list of unknown_value or predicted class, predicted confidence and ratio.
        """
        num_cores = multiprocessing.cpu_count()
        predicted = Parallel(n_jobs=num_cores)(
            delayed(self.predict)(X_train, y_train, X_predict[j, :], threshold, k, compute_confidence, unknown_value)
            for j in range(len(X_predict))
        )
        return predicted

    def grid_search(
        self, min_k, max_k, num_k, min_threshold, max_threshold, num_threshold, X_train, y_train, X_val, y_val
    ):
        """ Do grid search over parameters k and threshold. Use validation data to estimat performance for the different
        combinations of k and threshold.

        Args:
            min_k (int) : Minimum value of k
            max_k (int) : Maximum value of k
            num_k (int) : Number of k values to search over. Search values are divided evenly between min_k and max_k
            min_threshold (float) : Minimum threshold
            max_threshold (float) : Maximum threshold
            num_threshold (int): Number of thresholds to search over. Search values are divided evenly between
                min_thrshold and max_threshold
            X_train (numpy ndarray) : Array of feature values for the training data
            y_train (numpy array) : Array of integers corresponding to the classes of the training data,
            X_val (numpy ndarray) : Array of feature values for the validation data
            y_val (numpy array) : Array of integers corresponding to the classes for the validation data. 0 is reserved
                for the other/unknown class
        Returns:
            df_output_grid (pandas data frame) : Data frame with one row per (k, threshold)-combination and the
                calculated performance on the validation set for each combination. Sorted by highest f_mu value.
        """
        param_grid = {
            "param_k": [int(x) for x in np.linspace(start=min_k, stop=max_k, num=num_k)],
            "param_t": [round(x, 2) for x in np.linspace(start=min_threshold, stop=max_threshold, num=num_threshold)],
        }
        grid = ParameterGrid(param_grid)
        performance_measures_grid = ["f_mu", "precision_mu", "recall_mu"]

        output_grid = []
        for params in grid:
            predictions = self.k_nearest_neighbor(
                X_train=X_train,
                y_train=y_train,
                X_predict=X_val,
                threshold=params["param_t"],
                k=params["param_k"],
                compute_confidence=False,
            )
            predictions = np.asarray(predictions)
            os_perf_val = PerformanceOpenSet().overall_performance(y_val, predictions)
            performance_grid = [os_perf_val[x] for x in performance_measures_grid]
            output_grid.append([params["param_k"], params["param_t"]] + performance_grid)

        df_output_grid = pd.DataFrame(output_grid)
        df_output_grid.columns = [
            "k",
            "threshold",
            "validation_f_mu",
            "validation_precision_mu",
            "validation_recall_mu",
        ]
        df_output_grid = df_output_grid.sort_values(
            by=["validation_f_mu", "validation_precision_mu", "validation_recall_mu"], ascending=False
        ).reset_index(drop=True)

        return df_output_grid
