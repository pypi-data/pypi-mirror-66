import os
import shutil
import tempfile
import time

import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from cognite.osc.performance_open_set import PerformanceOpenSet


class ElementsDeepOpenClassifier:
    """
    """

    def __init__(self, min_delta=None, n_patience=None):
        self.min_delta = min_delta
        self.n_patience = n_patience
        if self.min_delta is None:
            self.min_delta = 0.1
        if self.n_patience is None:
            self.n_patience = 3

    def create_cnn_layers(self, output_combined, input_combined, ncol, input_dim_emb, maxlen):
        """ Add convolution layers

        Args:
            output_combined (list) : Empty list or list of Tensors
            input_combined (list) : Empty list or list of Tensors
            ncol (int) : Number of columns in data frame that will be used to create the layers
            input_dim_emb (int) : The number of words
            maxlen (int) : Maximum length of all sequences of words
        Returns:
            output_combined (list) : List of Tensors with the Tensor for the cnn layers added
            input_combined (list) : List of Tensors with the Tensor for the cnn layers added
        """
        # Create copies of the lists
        input_combined = list(input_combined)
        output_combined = list(output_combined)
        input_text = layers.Input(shape=(ncol,))
        # create convolution layers for the tokenized column
        embedding = layers.Embedding((input_dim_emb + 1), 256, input_length=ncol)(input_text)
        reshape = layers.Reshape((ncol, 256, 1))(embedding)
        conv_0 = layers.Conv2D(
            512, kernel_size=(2, 256), padding="valid", kernel_initializer="normal", activation="relu"
        )(reshape)
        conv_1 = layers.Conv2D(
            512, kernel_size=(3, 256), padding="valid", kernel_initializer="normal", activation="relu"
        )(reshape)
        maxpool_0 = layers.MaxPool2D(pool_size=(maxlen - 1, 1), strides=(1, 1), padding="valid")(conv_0)
        maxpool_1 = layers.MaxPool2D(pool_size=(maxlen - 2, 1), strides=(1, 1), padding="valid")(conv_1)
        concat = layers.Concatenate(axis=1)([maxpool_0, maxpool_1])
        flatten = layers.Flatten()(concat)
        drop = layers.Dropout(rate=0.5)(flatten)
        x = layers.Dense(16, activation="relu")(drop)
        x = models.Model(inputs=input_text, outputs=x)
        output_combined.append(x.output)
        input_combined.append(x.input)
        return output_combined, input_combined

    def create_feed_forward1(self, output_combined, input_combined, ncol):
        """ Add multilayer perceptron
        Args:
            output_combined (list) : Empty list or list of Tensors
            input_combined (list) : Empty list or list of Tensors
            ncol (int) : Number of columns in data frame that will be used to create the layers
        Returns:
            output_combined (list) : List of Tensors with the Tensor for the feed forward layers added
            input_combined (list) : List of Tensors with the Tensor for the feed forward layers added
        """
        # Create copies of the lists
        input_combined = list(input_combined)
        output_combined = list(output_combined)
        input_tag = layers.Input(shape=(ncol,))
        x = layers.Dense(128, activation="relu")(input_tag)
        x = layers.Dropout(rate=0.5)(x)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dropout(rate=0.3)(x)
        x = layers.Dense(32, activation="relu")(x)
        x = layers.Dropout(rate=0.3)(x)
        x = layers.Dense(16, activation="relu")(x)
        x = models.Model(inputs=input_tag, outputs=x)
        output_combined.append(x.output)
        input_combined.append(x.input)
        return output_combined, input_combined

    def create_feed_forward2(self, output_combined, input_combined, ncol):
        """ Add multilayer perceptron
        Args:
            output_combined (list) : Empty list or list of Tensors
            input_combined (list) : Empty list or list of Tensors
            ncol (int) : Number of columns in data frame that will be used to create the layers
        Returns:
            output_combined (list) : List of Tensors with the Tensor for the feed forward layers added
            input_combined (list) : List of Tensors with the Tensor for the feed forward layers added
        """
        # Create copies of the lists
        input_combined = list(input_combined)
        output_combined = list(output_combined)
        input_basic = layers.Input(shape=(ncol,))
        # create multilayer perceptron for the basic features
        x = layers.Dense(64, activation="relu")(input_basic)
        x = layers.Dropout(rate=0.5)(x)
        x = layers.Dense(32, activation="relu")(x)
        x = layers.Dropout(rate=0.3)(x)
        x = layers.Dense(16, activation="relu")(x)
        x = models.Model(inputs=input_basic, outputs=x)
        output_combined.append(x.output)
        input_combined.append(x.input)
        return output_combined, input_combined

    def init_layers(self, feature_dict_train, X_train):
        """ Initialize layers

        Args:
            feature_dict_train (dict) : Dictionary with each feature type as keys. For each feature_type, the features
                for the traing set
        Returns:
            output_combined (list) : List of Tensors
            input_combined (list) : List of Tensors

        """
        output_combined = []
        input_combined = []
        i = 0

        for feature_type in feature_dict_train:
            feature_type_dict = feature_dict_train[feature_type]
            for col in feature_type_dict.keys():
                if feature_type == "tokenizer":
                    output_combined, input_combined = self.create_cnn_layers(
                        output_combined=output_combined,
                        input_combined=input_combined,
                        ncol=X_train[i].shape[1],
                        input_dim_emb=feature_type_dict[col]["num_words"],
                        maxlen=feature_type_dict[col]["maxlen"],
                    )
                elif feature_type == "similarity":
                    output_combined, input_combined = self.create_feed_forward1(
                        output_combined=output_combined, input_combined=input_combined, ncol=X_train[i].shape[1]
                    )
                else:
                    output_combined, input_combined = self.create_feed_forward2(
                        output_combined=output_combined, input_combined=input_combined, ncol=X_train[i].shape[1]
                    )
                i = i + 1
        return output_combined, input_combined

    def combine_layers(self, output_combined, y_train):
        """ Combine the output fromn the different layers

        Args:
            output_combined (list) : List of Tensors
            y_train (np array) : one-hot encoded array of dependent value for the training data
        Returns:
            combined (Tensor)
        """
        # combine the output
        combined = layers.Concatenate(axis=1)(output_combined)
        combined = layers.Dense(8, activation="relu")(combined)
        combined = layers.Dropout(rate=0.5)(combined)
        combined = layers.Dense(y_train.shape[1], activation="sigmoid")(combined)
        return combined

    def fit_model(self, input_combined, final_output, y_train, X_train, X_val, y_val):
        """ Fit a neural network model

        Args:
            input_combined (list): List of input Tensors
            final_output (Tensor): Tensor from the final layer
            y_train (numpy ndarray): one-hot encoded array of dependent value for the training data
            X_train (list): List of feature arrays for the training data
            X_val (list) : one-hot encoded array of dependent value for the validation data
            y_val (numpy ndarray): List of feature arrays for the validation data
        Returns:
            model (model object) : The fitted model
        """
        model = models.Model(inputs=input_combined, outputs=final_output)
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        weight = compute_class_weight("balanced", range(y_train.shape[1]), np.argmax(y_train, axis=1))
        class_weight = {c: w for c, w in zip(range(y_train.shape[1]), weight)}
        # stop if the model is not improving
        es = EarlyStopping(
            monitor="val_loss", mode="min", verbose=0, patience=self.n_patience, min_delta=self.min_delta
        )

        tempfolderpath = tempfile.mkdtemp()
        checkpoint_dir = os.path.join(tempfolderpath, "{}/".format(time.time()))
        os.mkdir(checkpoint_dir)
        mc = ModelCheckpoint(
            os.path.join(checkpoint_dir, "model.hdf5"), monitor="val_acc", mode="max", verbose=0, save_best_only=True
        )
        model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            class_weight=class_weight,
            batch_size=128,
            epochs=100,
            verbose=0,
            callbacks=[es, mc],
        )
        shutil.rmtree(tempfolderpath)

        return model

    def estimate_thresholds(self, X_train, model, y_train_true, alpha, min_threshold):
        """ Estimate rejection threshold
        The logic is based on https://arxiv.org/pdf/1709.08716.pdf

        Args:
            X_train (list) : List of feature arrays for the training data
            model (model object) : Fitted model
            y_train_true (numpy ndarray): True value of y for the training data (one-hot encoded version)
            alpha (int or float) : The probability threshold is defined as mean subtracted alpha times the standard
                deviation
            min_threshold (float) : The minimum confidence a sample must have in order to be assigned to a class
        Returns:
            thresholds (numpy ndarray) : Array with threshold per class
        """

        y_train_pred = model.predict(x=X_train)
        # For each existing point, create a mirror point
        mirror_points = 1 + (1 - y_train_pred)
        combined = np.vstack([y_train_pred, mirror_points])
        # For each class use the predicted probability for the true class
        dist = np.where(np.vstack([y_train_true, y_train_true]), combined, np.nan)
        # Calculate the standard deviation for each class
        N = np.sum(np.isfinite(dist), axis=0)
        mu = np.nanmean(dist, axis=0)
        stdevs = np.sqrt(np.nansum(np.square(mu - dist), axis=0) / (N - 1))
        estimates = mu - alpha * stdevs
        thresholds = np.where(estimates > min_threshold, estimates, min_threshold)
        return thresholds

    def grid_search_alpha(self, X_train, y_train, X_val, y_val, model, min_alpha, max_alpha, num_alpha, min_threshold):
        """
        Search over a grid of alpha values and choose the one with best performance on validation set.
        Alpha is used to create the rejection threshold.
        """
        y_pred_proba = model.predict(x=X_val)
        best_f_mu = 0
        best_alpha = min_alpha
        for alpha in np.linspace(min_alpha, max_alpha, num_alpha):
            thresholds = self.estimate_thresholds(
                X_train=X_train, model=model, y_train_true=y_train, alpha=alpha, min_threshold=min_threshold
            )
            y_pred_class = self.extract_class(y_pred_proba, thresholds)
            os_perf = PerformanceOpenSet().overall_performance(y_val, y_pred_class)
            f_mu = os_perf["f_mu"]
            if f_mu > best_f_mu:
                best_alpha = alpha
                best_f_mu = f_mu
        return best_alpha

    def extract_class(self, y_pred_proba, thresholds=None, min_threshold=0.5):
        """ Given thresholds and predicted probabilities find the predicted class

        Args:
            y_pred_proba (numpy nd array): Predicted probability per class per sample
            thresholds (list or None) : List of threshold per class. If None, use min_threshold
            min_threshold (float) : Min probability in order for a sample to be assigned to a class
        Return:
            y_pred_class (numpy array) : Array with predicted class (0 if no class)
        """
        if thresholds is None:
            thresholds = np.array([min_threshold] * y_pred_proba.shape[1])

        y_pred_class = np.where(np.sum(y_pred_proba > thresholds, axis=1), np.argmax(y_pred_proba, axis=1) + 1, 0)
        return y_pred_class

    def re_init_weights_choose_best_model(
        self,
        feature_dict,
        X_train,
        y_train,
        X_val_known_known,
        y_val_known_known,
        X_val_all,
        y_val_all,
        min_alpha,
        max_alpha,
        num_alpha,
        min_threshold,
        n_runs,
        stop_precision,
        stop_recall,
    ):
        """ Fit a model up to n_runs-times and select the model with the higest f_mu on the validation set.
        This can be useful because, the initialization of the weights will influence what local minimum the
        optimization ends up in. Re-initializing the weights can significantly improve the performance.
        If precision is higher than stop_precision and recall higher than stop_recall on the validation set,
        the loop is stopped and that model is selected.
        """
        f_mu = np.empty(shape=0)
        precision_mu = np.empty(shape=0)
        recall_mu = np.empty(shape=0)
        model = np.empty(shape=0)
        best_alpha = np.empty(shape=0)
        thresholds = np.empty(shape=(0, y_train.shape[1]))

        for i in range(n_runs):
            output_combined, input_combined = ElementsDeepOpenClassifier().init_layers(
                feature_dict_train=feature_dict, X_train=X_train
            )
            combined = ElementsDeepOpenClassifier().combine_layers(output_combined=output_combined, y_train=y_train)
            model_ = ElementsDeepOpenClassifier().fit_model(
                input_combined=input_combined,
                final_output=combined,
                y_train=y_train,
                X_train=X_train,
                X_val=X_val_known_known,
                y_val=y_val_known_known,
            )
            best_alpha_ = ElementsDeepOpenClassifier().grid_search_alpha(
                X_train=X_train,
                y_train=y_train,
                X_val=X_val_all,
                y_val=y_val_all,
                model=model_,
                min_alpha=min_alpha,
                max_alpha=max_alpha,
                num_alpha=num_alpha,
                min_threshold=min_threshold,
            )
            thresholds_ = ElementsDeepOpenClassifier().estimate_thresholds(
                X_train=X_train, model=model_, y_train_true=y_train, alpha=best_alpha_, min_threshold=min_threshold
            )
            y_pred_proba = model_.predict(x=X_val_all)
            y_pred_class = self.extract_class(y_pred_proba, thresholds_)
            os_perf_val = PerformanceOpenSet().overall_performance(y_val_all, y_pred_class)

            if (os_perf_val["precision_mu"] > stop_precision) & (os_perf_val["recall_mu"] > stop_recall):
                val_f_mu = os_perf_val["f_mu"]
                val_precision_mu = os_perf_val["precision_mu"]
                val_recall_mu = os_perf_val["recall_mu"]
                return model_, val_f_mu, val_precision_mu, val_recall_mu, best_alpha_, thresholds_
            else:
                f_mu = np.append(f_mu, os_perf_val["f_mu"])
                precision_mu = np.append(precision_mu, os_perf_val["precision_mu"])
                recall_mu = np.append(recall_mu, os_perf_val["recall_mu"])
                model = np.append(model, model_)
                best_alpha = np.append(best_alpha, best_alpha_)
                thresholds = np.concatenate((thresholds, thresholds_.reshape(1, len(thresholds_))))

        val_f_mu = f_mu[f_mu == max(f_mu)][0]
        val_precision_mu = precision_mu[f_mu == max(f_mu)][0]
        val_recall_mu = recall_mu[f_mu == max(f_mu)][0]
        best_alpha_ = best_alpha[f_mu == max(f_mu)][0]
        thresholds_ = thresholds[[f_mu == max(f_mu)][0], :]
        model_ = model[f_mu == max(f_mu)][0]

        return model_, val_f_mu, val_precision_mu, val_recall_mu, best_alpha_, thresholds_[0]
