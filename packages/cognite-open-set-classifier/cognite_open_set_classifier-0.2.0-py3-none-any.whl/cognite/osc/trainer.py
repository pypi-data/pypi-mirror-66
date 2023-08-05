import copy
import os

import numpy as np
import pandas as pd

from cognite.osc.data_pipe import DataPipe
from cognite.osc.deep_open_classifier import ElementsDeepOpenClassifier
from cognite.osc.open_set_nearest_neighbors import ElementsOpenSetNearestNeighbors
from cognite.osc.performance_open_set import PerformanceOpenSet
from cognite.osc.save_load import (
    load_csv,
    load_feature_dict,
    load_json,
    load_keras_model,
    load_label_encoder_dict,
    load_pickle,
    save_csv,
    save_feature_dict,
    save_json,
    save_keras_model,
    save_label_encoder_dict,
    save_pickle,
)
from cognite.osc.validation import (
    validate_columns_in_df,
    validate_non_empty_feature_columns,
    validate_num_samples_types_of_interest,
    validate_type_col,
    validate_type_of_parametes,
    validate_types_of_interest,
)


class OpenSetClassification(object):
    def __init__(self, type_col, types_of_interest, cols_clean, feature_cols, cols_special_char, cols_char_count):
        self.type_col = type_col
        self.types_of_interest = types_of_interest
        self.cols_clean = cols_clean
        self.feature_cols = feature_cols
        self.cols_special_char = cols_special_char
        self.cols_char_count = cols_char_count
        self.data_pipe = DataPipe()

    def prepare_train_data(self, df_train, val_fraction=0.4):
        """ Common data preparation steps for training data

        Args:
            df_train (pandas DataFrame) : Data frame with samples
            val_fraction (float) : Fraction of samples in df that are in the validation set, default 0.4
        """
        # Validate the type_col parameter
        validate_type_col(type_col=self.type_col, df=df_train)
        # Validate the types_of_interest parameter
        validate_types_of_interest(types_of_interest=self.types_of_interest)
        # There must be at least two unique classes in the training data. If there is only one item in type of interest,
        # other is used as the second class, other is then defined as everything which have a different class than the
        # type of interest
        if len(self.types_of_interest) == 1:
            self.types_of_interest.append("other")
            df_train.loc[~df_train[self.type_col].isin(self.types_of_interest), self.type_col] = "other"
        # Check that all elements in types_of_interest have enough samples
        validate_num_samples_types_of_interest(
            types_of_interest=self.types_of_interest, type_col=self.type_col, df=df_train
        )
        ### Prepare data ###
        if self.feature_cols is None:
            # Use all columns except for type_col as feature_cols if no features cols are provided
            self.feature_cols = [x for x in df_train.columns if x != self.type_col]
        if self.cols_clean is not None:
            validate_type_of_parametes(parameter_list=[self.cols_clean], correct_type_list=[list])
            validate_columns_in_df(df=df_train, columns_list=self.cols_clean)
            validate_type_of_parametes(parameter_list=[self.feature_cols], correct_type_list=[list])
        validate_columns_in_df(df=df_train, columns_list=self.feature_cols)
        (
            self.df_prepared,
            self.feature_cols_string,
            self.feature_cols_encode,
            self.feature_cols_numeric,
        ) = self.data_pipe.prepare_data(df=df_train, cols_clean=self.cols_clean, feature_cols=self.feature_cols)
        if self.cols_special_char is None:
            # Search over all string features if no list of cols_special_char is given
            self.cols_special_char = self.feature_cols_string
        if self.cols_char_count is None:
            # Use all string features if no list of cols_special_char is given
            self.cols_char_count = self.feature_cols_string
        # Check that no column in string_feature_cols is a column of empty strings
        validate_non_empty_feature_columns(df=self.df_prepared, string_feature_columns=self.feature_cols_string)

        # Split into:
        # * known-knowns (samples with a known type that is one of the types of interest)
        # * known-unknowns (samples with a known type, but the type is not one of the types of interest)
        self.df_known_known, self.df_known_unknown = self.data_pipe.split_into_knowns_unknowns(
            df=self.df_prepared, types_of_interest=self.types_of_interest, type_col=self.type_col
        )
        self.label_encoder_dict = self.data_pipe.init_label_encoding_type(types_of_interest=self.types_of_interest)
        # Create a one-hot-encoded version of the y (the dependent variable). Note: Unknowns are in the first column
        y_1hot = self.data_pipe.create_onehot_of_labels(
            df=self.df_prepared, label_encoder_dict=self.label_encoder_dict, col_name=self.type_col
        )
        # Create splits of:
        # 1. Just known-knowns. The known-knowns are split into a train, validation and test set.
        # The training and validation set with only known knowns are used to train a model.
        # 2. The known-unknowns.  The combination of the known-known validation samples and the known-unknown (called
        # all) are used to search for the optimal value of the parameters.
        self.train_idx, self.val_idx = self.data_pipe.create_train_test_split(
            sequence=self.df_known_known.index,
            stratify_vec=np.argmax(y_1hot[self.df_known_known.index], axis=1),
            test_size=val_fraction,
        )

        self.y_train = y_1hot[self.train_idx]
        self.y_val_knownknowns = y_1hot[self.val_idx]
        self.y_val_all = y_1hot[self.val_idx.union(self.df_known_unknown.index, sort=False)]

        # Find columns to count number of characters and number of special characters and validate the column names
        if self.cols_special_char is None:
            # Search over all string features if no list of cols_special_char is given
            self.cols_special_char = self.feature_cols_string
        if self.cols_char_count is None:
            # Use all string features if no list of cols_special_char is given
            self.cols_char_count = self.feature_cols_string
        validate_type_of_parametes(
            parameter_list=[self.cols_special_char, self.cols_char_count], correct_type_list=[list, list]
        )
        validate_columns_in_df(df=df_train, columns_list=list(set(self.cols_special_char + self.cols_char_count)))

    def prepare_predict_data(self, df_predict, stack_features_horizontally):
        """ Common data preparation steps for predict data

        Args:
            df_predict (pandas DataFrame) : Data frame with samples
            stack_features_horizontally (bool) : If True stack the feature arrays horizontally
        """
        df_prepared, _, _, _ = DataPipe().prepare_data(
            df=df_predict, cols_clean=self.param_dict["cols_clean"], feature_cols=self.param_dict["feature_cols"]
        )
        ### Create features ###
        feature_dict = DataPipe().create_feature_matrices(df=df_prepared, feature_dict=self.feature_dict)
        self.X_predict = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict, stack_horizontally=stack_features_horizontally
        )


class DeepOpenClassification(OpenSetClassification):
    def __init__(
        self,
        type_col=None,
        types_of_interest=None,
        feature_cols=None,
        cols_special_char=None,
        cols_char_count=None,
        cols_clean=None,
        cols_tokenize=[],
        min_num_words_tokenizer_columns=2,
        max_num_tokenizer_columns=1,
        n_prototypes=None,
        min_threshold=0.7,
        min_alpha=1,
        max_alpha=3,
        num_alpha=3,
        n_runs=3,
        stop_precision=1,
        stop_recall=1,
    ):
        self.cols_tokenize = cols_tokenize
        self.min_num_words_tokenizer_columns = min_num_words_tokenizer_columns
        self.max_num_tokenizer_columns = max_num_tokenizer_columns
        self.n_prototypes = n_prototypes
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.num_alpha = num_alpha
        self.min_threshold = min_threshold
        self.n_runs = n_runs
        self.stop_precision = stop_precision
        self.stop_recall = stop_recall
        self.doc = ElementsDeepOpenClassifier()

        super().__init__(type_col, types_of_interest, cols_clean, feature_cols, cols_special_char, cols_char_count)

    def fit(self):
        # Check all parameters have the correct type
        validate_type_of_parametes(
            parameter_list=[
                self.cols_tokenize,
                self.min_num_words_tokenizer_columns,
                self.max_num_tokenizer_columns,
                self.n_prototypes,
                self.min_alpha,
                self.max_alpha,
                self.num_alpha,
                self.min_threshold,
                self.n_runs,
                self.stop_precision,
                self.stop_recall,
            ],
            correct_type_list=[
                list,
                [int, type(None)],
                [int, type(None)],
                [int, type(None)],
                [int, float],
                [int, float],
                int,
                float,
                int,
                [int, float],
                [int, float],
            ],
        )
        # Check that all elements in cols_tokenize are in df
        validate_columns_in_df(df=self.df_known_known, columns_list=self.cols_tokenize)
        ### Initialize features ###
        self.feature_dict = self.data_pipe.create_feature_dict(
            df=self.df_known_known.loc[self.train_idx, :],
            include_tokenizer=True,
            cols_tokenize=self.cols_tokenize,
            feature_cols_encode=self.feature_cols_encode,
            min_num_words_tokenizer_columns=self.min_num_words_tokenizer_columns,
            max_num_tokenizer_columns=self.max_num_tokenizer_columns,
            cols_special_char=self.cols_special_char,
            cols_char_count=self.cols_special_char,
            feature_cols_numeric=self.feature_cols_numeric,
        )
        ### Create features ###
        # Training data
        feature_dict_df = copy.deepcopy(self.feature_dict)
        feature_dict_df = self.data_pipe.create_feature_matrices(df=self.df_prepared, feature_dict=feature_dict_df)

        ### Create X for training and for test and validation
        # for only known knowns and for all knowns ###
        X_train = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict_df, stack_horizontally=False, indices=self.train_idx
        )
        X_val_kk = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict_df, stack_horizontally=False, indices=self.val_idx
        )
        X_val_all = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict_df,
            stack_horizontally=False,
            indices=self.val_idx.union(self.df_known_unknown.index, sort=False),
        )

        ### Train the model and find best alpha and the threshold for each class###
        # Remove first column from y_train and y_val_knownknowns (unknown column), the model is trained on just the knowns
        self.y_train = np.delete(self.y_train, 0, 1)
        y_val_knownknowns = np.delete(self.y_val_knownknowns, 0, 1)
        (
            self.model,
            val_f_mu,
            val_precision_mu,
            val_recall_mu,
            best_alpha,
            thresholds,
        ) = self.doc.re_init_weights_choose_best_model(
            feature_dict=feature_dict_df,
            X_train=X_train,
            y_train=self.y_train,
            X_val_known_known=X_val_kk,
            y_val_known_known=y_val_knownknowns,
            X_val_all=X_val_all,
            y_val_all=np.argmax(self.y_val_all, axis=1),
            min_alpha=self.min_alpha,
            max_alpha=self.max_alpha,
            num_alpha=self.num_alpha,
            min_threshold=self.min_threshold,
            n_runs=self.n_runs,
            stop_precision=self.stop_precision,
            stop_recall=self.stop_recall,
        )
        self.param_dict = {
            "algorithm": "deep_open_classification",
            "alpha": best_alpha,
            "thresholds": list(thresholds),
            "cols_clean": self.cols_clean,
            "feature_cols": self.feature_cols,
            "type_col": self.type_col,
        }
        return self

    def dump(self, file_dir=""):
        """ Save model, parameters and feature dictionary

        Args:
            file_dir (str) : Name of directory to save the files
        """
        if file_dir:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

        # Save model
        save_keras_model(model=self.model, file_dir=file_dir)

        # Save param_dict
        save_json(obj=self.param_dict, file_name="param_dict", file_dir=file_dir)

        # Save label_encoder_dict
        save_label_encoder_dict(label_encoder_dict=self.label_encoder_dict, file_dir=file_dir)

        # Save feature_dict
        save_feature_dict(feature_dict=self.feature_dict, file_dir=file_dir)

    def load(self, file_dir=""):
        """ Load output from fitted model

        Args:
            file_dir (str) : Name of directory to load the files from
        """
        # Load saved Tensorflow model
        self.model = load_keras_model(file_dir=file_dir)

        # Load parameters
        self.param_dict = load_json(file_name="param_dict", file_dir=file_dir)

        # Load label_encoder_dict
        self.label_encoder_dict = load_label_encoder_dict(file_dir=file_dir)

        # Load feature_dict
        self.feature_dict = load_feature_dict(file_dir=file_dir)

    def evaluate(self, evaluate_data):
        """ Evaluate the performance of the model on evaluate_data

        Args:
            evaluate_data (pandas Data Frame): Data to use to evaluate the performance of the model
        Returns:
            open_set_performance (dict) : Dictionary of performance measures
        """
        y_1hot = self.data_pipe.create_onehot_of_labels(
            df=evaluate_data, label_encoder_dict=self.label_encoder_dict, col_name=self.param_dict["type_col"]
        )
        y_true = np.argmax(y_1hot, axis=1)
        df_prepared, _, _, _ = DataPipe().prepare_data(
            df=evaluate_data, cols_clean=self.param_dict["cols_clean"], feature_cols=self.param_dict["feature_cols"]
        )
        ### Create features ###
        # Predict class
        y_pred_proba = self.model.predict(self.X_predict)
        y_pred_class = self.doc.extract_class(y_pred_proba=y_pred_proba, thresholds=self.param_dict["thresholds"])
        # Find which values are associated with the "other" class.
        # Set the value to the minimum of the other values for every sample associated with the other class.
        other_values = [k for (k, v) in self.label_encoder_dict["decoder"].items() if v == "other"]
        y_true[np.isin(y_true, other_values)] = min(other_values)
        y_pred_class[np.isin(y_pred_class, other_values)] = min(other_values)
        open_set_performance = PerformanceOpenSet().overall_performance(y_true=y_true, y_predicted=y_pred_class)
        return open_set_performance

    def predict(self):
        """ Predict class for samples

        Returns:
            predict_type (list) : Predicted type for each sample in new_data
        """
        # Check if self.output_unknown is defined, if not create it
        try:
            self.y_pred_proba[0]
        except AttributeError:
            self.y_pred_proba = self.model.predict(self.X_predict)
        y_pred_class = self.doc.extract_class(y_pred_proba=self.y_pred_proba, thresholds=self.param_dict["thresholds"])
        predict_type = [self.label_encoder_dict["decoder"][x] for x in y_pred_class]
        return predict_type

    def predict_proba(self):
        """ Predict probability of belonging to a class for samples

        Returns:
            (list) : Predicted confidence for each sample in new_data. Note, if the predicted class is 0, -1 is
                returned as the predicted confidence
        """
        # Check if self.output_unknown is defined, if not create it
        try:
            self.y_pred_proba[0]
        except AttributeError:
            self.y_pred_proba = self.model.predict(self.X_predict)
        self.output_unknown = pd.DataFrame(
            self.doc.extract_class(y_pred_proba=self.y_pred_proba, thresholds=self.param_dict["thresholds"]),
            columns=["predict_class"],
        )
        self.output_unknown["max_confidence"] = np.max(self.y_pred_proba, axis=1)
        self.output_unknown["confidence_class"] = np.max(self.y_pred_proba, axis=1)
        is_argmax_array = np.zeros_like(self.y_pred_proba)
        is_argmax_array[np.arange(len(self.y_pred_proba)), self.y_pred_proba.argmax(1)] = 1
        confidence_unknown_array = (self.param_dict["thresholds"] - self.y_pred_proba) / self.param_dict["thresholds"]
        self.output_unknown["confidence_unknown"] = np.max(confidence_unknown_array * is_argmax_array, axis=1)
        predict_confidence = np.where(
            self.output_unknown["predict_class"] == 0,
            self.output_unknown["confidence_unknown"],
            self.output_unknown["confidence_class"],
        )
        return list(predict_confidence)


class OpenSetNearestNeighborsClassification(OpenSetClassification):
    def __init__(
        self,
        type_col=None,
        types_of_interest=None,
        feature_cols=None,
        cols_clean=None,
        cols_special_char=None,
        cols_char_count=None,
        n_prototypes=None,
        threshold_feature_selection=0.01,
        min_k=10,
        max_k=20,
        num_k=2,
        min_threshold=0.1,
        max_threshold=0.9,
        num_threshold=9,
    ):
        self.algorithm = "open_set_nearest_neighbors"
        self.n_prototypes = n_prototypes
        self.threshold_feature_selection = threshold_feature_selection
        self.min_k = min_k
        self.max_k = max_k
        self.num_k = num_k
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.num_threshold = num_threshold
        self.osnn = ElementsOpenSetNearestNeighbors()

        super().__init__(type_col, types_of_interest, cols_clean, feature_cols, cols_special_char, cols_char_count)

        # Check all parameters have the correct type
        validate_type_of_parametes(
            parameter_list=[
                self.n_prototypes,
                self.threshold_feature_selection,
                self.min_k,
                self.max_k,
                self.num_k,
                self.min_threshold,
                self.max_threshold,
                self.num_threshold,
            ],
            correct_type_list=[[int, type(None)], float, int, int, int, float, float, int],
        )

    def fit(self):
        ### Find features ###
        self.feature_dict = self.data_pipe.create_feature_dict(
            df=self.df_known_known.loc[self.train_idx, :],
            include_tokenizer=False,
            feature_cols_encode=self.feature_cols_encode,
            n_prototypes_similarity_encoding=self.n_prototypes,
            cols_special_char=self.cols_special_char,
            cols_char_count=self.cols_special_char,
            feature_cols_numeric=self.feature_cols_numeric,
        )
        ### Create features ###
        # Training data
        feature_dict_df = copy.deepcopy(self.feature_dict)
        feature_dict_df = self.data_pipe.create_feature_matrices(df=self.df_prepared, feature_dict=feature_dict_df)

        X_train = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict_df, stack_horizontally=True, indices=self.train_idx
        )
        X_val_all = self.data_pipe.create_feature_arrays(
            feature_dict=feature_dict_df,
            stack_horizontally=True,
            indices=self.val_idx.union(self.df_known_unknown.index, sort=False),
        )

        # Use train and validation set to choose features.
        X_feature_selection = np.vstack([X_train, X_val_all])
        y_feature_selection = np.concatenate([np.argmax(self.y_train, axis=1), np.argmax(self.y_val_all, axis=1)])
        # Return the Select-From-Model transformer based on feature importance from a random forest classifier
        self.sfm_transformer = self.data_pipe.create_feature_selection_transformer(
            X_train=X_feature_selection,
            y_train=y_feature_selection,
            feature_importance_threshold=self.threshold_feature_selection,
        )
        # Transform
        self.X_train_reduced = self.sfm_transformer.transform(X_train)
        X_val_all_reduced = self.sfm_transformer.transform(X_val_all)

        df_output_grid = self.osnn.grid_search(
            min_k=self.min_k,
            max_k=self.max_k,
            num_k=self.num_k,
            min_threshold=self.min_threshold,
            max_threshold=self.max_threshold,
            num_threshold=self.num_threshold,
            X_train=self.X_train_reduced,
            y_train=np.argmax(self.y_train, axis=1),
            X_val=X_val_all_reduced,
            y_val=np.argmax(self.y_val_all, axis=1),
        )
        self.param_dict = {
            "algorithm": "open_set_nearest_neighbors",
            "k": int(df_output_grid.loc[0, "k"]),
            "threshold": float(df_output_grid.loc[0, "threshold"]),
            "cols_clean": self.cols_clean,
            "feature_cols": self.feature_cols,
            "type_col": self.type_col,
        }
        return self

    def dump(self, file_dir=""):
        """ Save model, parameters and feature dictionary

        Args:
            file_dir (str) : Name of directory to save the files
        """
        if file_dir:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

        # Save training data
        save_csv(df=pd.DataFrame(self.X_train_reduced), file_name="training_data_X", file_dir=file_dir)
        save_csv(df=pd.DataFrame(self.y_train), file_name="training_data_y", file_dir=file_dir)

        # Save param_dict
        save_json(obj=self.param_dict, file_name="param_dict", file_dir=file_dir)

        # Save label_encoder_dict
        save_label_encoder_dict(label_encoder_dict=self.label_encoder_dict, file_dir=file_dir)

        # Save select-from-model transformer
        save_pickle(obj=self.sfm_transformer, file_name="select_from_model_transformer", file_dir=file_dir)

        # Save feature_dict
        save_feature_dict(feature_dict=self.feature_dict, file_dir=file_dir)

    def load(self, file_dir=""):
        """ Load output from fitted model

        Args:
            file_dir (str) : Name of directory to load the files from
        """
        # Load csv-files and convert the output to numpy arrays
        self.X_train_reduced = load_csv(file_name="training_data_X", file_dir=file_dir).values
        self.y_train = load_csv(file_name="training_data_y", file_dir=file_dir).values

        # Load parameters
        self.param_dict = load_json(file_name="param_dict", file_dir=file_dir)

        # Load label_encoder_dict
        self.label_encoder_dict = load_label_encoder_dict(file_dir=file_dir)

        # Load select-from-model transformer
        self.sfm_transformer = load_pickle(file_name="select_from_model_transformer", file_dir=file_dir)

        # Load feature_dict
        self.feature_dict = load_feature_dict(file_dir=file_dir)

    def evaluate(self, evaluate_data):
        """ Evaluate the performance of the model on evaluate_data

        Args:
            evaluate_data (pandas Data Frame): Data to use to evaluate the performance of the model
        Returns:
            open_set_performance (dict) : Dictionary of performance measures
        """
        y_1hot = self.data_pipe.create_onehot_of_labels(
            df=evaluate_data, label_encoder_dict=self.label_encoder_dict, col_name=self.param_dict["type_col"]
        )
        y_true = np.argmax(y_1hot, axis=1)
        X_evaluate_reduced = self.sfm_transformer.transform(self.X_predict)
        # Predict class
        predicted = self.osnn.k_nearest_neighbor(
            X_train=self.X_train_reduced,
            y_train=np.argmax(self.y_train, axis=1),
            X_predict=X_evaluate_reduced,
            threshold=self.param_dict["threshold"],
            k=self.param_dict["k"],
            compute_confidence=True,
        )
        predicted_df = pd.DataFrame(predicted, columns=["predict_class", "predict_confidence", "ratio"])
        # Find which values are associated with the "other" class.
        # Set the value to the minimum of the other values for every sample associated with the other class.
        other_values = [k for (k, v) in self.label_encoder_dict["decoder"].items() if v == "other"]
        y_true[np.isin(y_true, other_values)] = min(other_values)
        predicted_df.loc[predicted_df["predict_class"].isin(other_values), "predict_class"] = min(other_values)
        open_set_performance = PerformanceOpenSet().overall_performance(
            y_true=y_true, y_predicted=predicted_df["predict_class"]
        )
        return open_set_performance

    def predict(self):
        """ Predict class for samples

        Returns:
            (list) : Predicted type for each sample in new_data
        """
        # Check if self.output_unknown is defined, if not create it
        try:
            self.output_unknown.head()
        except AttributeError:
            X_predict_reduced = self.sfm_transformer.transform(self.X_predict)
            predicted = self.osnn.k_nearest_neighbor(
                X_train=self.X_train_reduced,
                y_train=np.argmax(self.y_train, axis=1),
                X_predict=X_predict_reduced,
                threshold=self.param_dict["threshold"],
                k=self.param_dict["k"],
                compute_confidence=True,
            )
            self.output_unknown = pd.DataFrame(predicted, columns=["predict_class", "predict_confidence", "ratio"])
            self.output_unknown.loc[self.output_unknown["predict_confidence"] > 1, "predict_confidence"] = 1

        return [self.label_encoder_dict["decoder"][x] for x in self.output_unknown["predict_class"]]

    def predict_proba(self):
        """ Predict probability of belonging to a class for samples

        Returns:
            (list) : Predicted confidence for each sample in new_data. Note, if the predicted class is 0, -1 is
                returned as the predicted confidence
        """
        # Check if self.output_unknown is defined, if not create it
        try:
            self.output_unknown.head()
        except AttributeError:
            X_predict_reduced = self.sfm_transformer.transform(self.X_predict)
            predicted = self.osnn.k_nearest_neighbor(
                X_train=self.X_train_reduced,
                y_train=np.argmax(self.y_train, axis=1),
                X_predict=X_predict_reduced,
                threshold=self.param_dict["threshold"],
                k=self.param_dict["k"],
                compute_confidence=True,
            )
            self.output_unknown = pd.DataFrame(predicted, columns=["predict_class", "predict_confidence", "ratio"])
            self.output_unknown.loc[self.output_unknown["predict_confidence"] > 1, "predict_confidence"] = 1

        return list(self.output_unknown["predict_confidence"])
