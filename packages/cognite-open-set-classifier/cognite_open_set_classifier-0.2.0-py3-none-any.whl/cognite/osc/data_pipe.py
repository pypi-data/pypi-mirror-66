import copy
import re
from collections import defaultdict

import numpy as np
import pandas as pd
from dirty_cat import SimilarityEncoder
from pandas.api.types import is_string_dtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


class DataPipe:
    def __init__(self):
        pass

    def split_into_knowns_unknowns(self, df, types_of_interest, type_col):
        """ Split df into known-known, known-unknown and unknown

        Args:
            df (DataFrame) : DataFrame with all samples
            types_of_interest (list) : List of types of interest

        Returns:
            df_known_known (DataFrame): Pandas DataFrame with samples with a known type that is one of the types of
            interest.
            df_known_unknown (DataFrame): Pandas DataFrame with samples with a known type, but the type is not one
            of the types of interest.
        """
        df_known_known = df[df[type_col].isin(types_of_interest)]
        df_known_unknown = df[~df[type_col].isin(types_of_interest)]
        return df_known_known, df_known_unknown

    def create_onehot_of_labels(self, df, label_encoder_dict, col_name):

        df_labels = df[col_name].apply(lambda x: label_encoder_dict["encoder"][x])
        df_onehot = label_encoder_dict["one_hot_encoder"].transform(df_labels.values.reshape(-1, 1))

        return df_onehot

    def init_label_encoding_type(self, types_of_interest):
        """ The label encoder with default value.

        Args:
            types_of_interest (list) : List of types of interest
        Returns:
             (dict) : Dict with encoding of dependent variable
        """

        label_encoder = defaultdict(int, {val: ind + 1 for ind, val in enumerate(types_of_interest)})

        label_decoder = dict([[v, k] for k, v in label_encoder.items()])
        label_decoder[0] = "other"

        categories = sorted(label_decoder.keys())
        one_hot_encoder = OneHotEncoder(sparse=False, categories=[categories])
        one_hot_encoder.fit(np.array(categories).reshape(-1, 1))

        return {"encoder": label_encoder, "decoder": label_decoder, "one_hot_encoder": one_hot_encoder}

    def create_train_test_split(self, sequence, stratify_vec=None, random_state=0, test_size=0.4):
        """ Create train test split

        Args:
            sequence (list/numpy array/pandas dataframe) : Data to be split
            y_vec (array-like/None) : If not None, data is split in a stratified fashion, using this as the class labels
            random_state (int) : the seed used by the random number generator
            test_size (float) : the proportion of the dataset to include in the test split
        Returns:
            df_train, df_test : Split of df
        """
        df_train, df_test = train_test_split(
            sequence, train_size=1 - test_size, test_size=test_size, stratify=stratify_vec, random_state=random_state
        )
        return df_train, df_test

    def prepare_data(self, df, cols_clean, feature_cols):
        """ Prepare data: Encode cols_clean and fill na and convert to strings for feature_cols

        Args:
            df (DataFrame) : DataFrame with samples
            cols_clean (list) : List of columns to clean, that is all digits [0-9] are set to 1 and non alphanumeric
                characters, dots and spaces are set to #
            feature_cols (list) : List of column names of all features
        Returns:
            df (DataFrame) : DataFrame with na replaced with empty string for all feature_cols and strings in
                cols_clean encoded using _clean_string
            feature_cols_string (list) : List of features that are strings (not numeric), original column names
            feature_cols_encode (list) : List of string features with those that are cleaned replaced by the
                clean name version, these are the ones that will later be encoded using tokenization or similarity
                encoding
            feature_cols_numeric (list) : List of features that have numeric values
        """
        feature_cols_numeric = []
        feature_cols_string = []

        for col in feature_cols:
            # If at least one element in col is a string, convert all to strings
            if is_string_dtype(df[col]):
                df[col].fillna(value="", inplace=True)
                df[col] = df[col].astype(str)
                feature_cols_string.append(col)
            else:
                feature_cols_numeric.append(col)

        feature_cols_encode = list(feature_cols_string)
        if cols_clean is not None:
            for col in cols_clean:
                df[col + "_cleaned"] = df[col].apply(self._clean_string)
                if col in feature_cols:
                    feature_cols_encode.remove(col)
                if col + "_cleaned" not in feature_cols:
                    feature_cols_encode.append(col + "_cleaned")

        return df, feature_cols_string, feature_cols_encode, feature_cols_numeric

    def create_feature_dict(
        self,
        df,
        feature_cols_encode,
        cols_special_char,
        cols_char_count,
        feature_cols_numeric,
        cols_tokenize=[],
        include_tokenizer=False,
        min_num_words_tokenizer_columns=None,
        max_num_tokenizer_columns=None,
        filters='!"#$%&()*+,.:;<=>?@[\\]^_`{|}~\t\n',
        n_prototypes_similarity_encoding=None,
    ):
        """ Create dictionary with information about which columns to use as features for the different feature types
        and how to transform them

        Args:
            df (DataFrame) : DataFrame with samples
            feature_cols_encode ( list) : List of features that are strings (not numeric) that should be either
                tokenized or similarity encoded
            cols_special_char (list) : List of columns to search for special characters
            cols_char_count (list) : List of columns to count number of characters
            feature_cols_numeric (list) : List of columns with numeric values
            cols_tokenize (list) : List of names of columns to tokenize, if empty select the up to
                max_num_tokenizer_columns ones that have the most unique words that have at least
                min_num_words_tokenizer_columns words
            include_tokenizer (bool) : If True do tokenization of one or more columns in string_feature_cols
            min_num_words_tokenizer_columns (int or None) : The minimum number of words in a column for it to be
                tokenized (>1), if None use default from _find_tokenizer_column()
            max_num_tokenizer_columns (int or None) : The maximum number of columns that are to be tokenized, if None
                use default from _find_tokenizer_column()
            filters (str) : A string that specifies which character that will be filtered from the texts when tokenizing.
            n_prototypes_similarity_encoding (int or None) : The number the categories are to be reduced to for
                similarity encoding. If None use default from init_similarity_encoder()

            Returns:
                feature_dict (dict) : Dictionary with information about which columns to use as features for the
                    different feature types and how to transform them
        """
        feature_dict = dict()
        similarity_cols = copy.deepcopy(feature_cols_encode)
        if include_tokenizer:
            # Choose which columns to tokenize
            if len(cols_tokenize) == 0:
                cols_tokenize = self._find_tokenizer_column(
                    feature_cols=feature_cols_encode,
                    df=df,
                    min_words_column=min_num_words_tokenizer_columns,
                    max_num_columns=max_num_tokenizer_columns,
                    filters=filters,
                )
            tokenizer_dict_all = dict()
            # Do similarity encoding on columns not used as tokenizer
            for tokenizer_col in cols_tokenize:
                tokenizer_dict_all = self._init_tokenizer(
                    tokenizer_dict_all=tokenizer_dict_all, df=df, column_name=tokenizer_col, filters=filters
                )
                similarity_cols.remove(tokenizer_col)
                feature_dict["tokenizer"] = tokenizer_dict_all
        # Create similarity encode of all string feature which have not been tokinized
        similarity_dict_all = dict()
        for similarity_col in similarity_cols:
            similarity_dict_all = self._init_similarity_encoder(
                similarity_dict_all=similarity_dict_all,
                df=df,
                column_name=similarity_col,
                n_prototypes=n_prototypes_similarity_encoding,
            )
        feature_dict["similarity"] = similarity_dict_all
        # Add count of special characters
        special_char_dict = self._create_special_char_dict(cols_special_char=cols_special_char, df=df)
        feature_dict["special_char"] = special_char_dict

        # Add count of character as features for columns in cols_char_count
        cols_char_count_dict = {}
        for col in cols_char_count:
            # Calculate min and max per column (used to normalize)
            transformed = self._get_char_counts(pd_series=df[col])
            min_list, max_list = self.create_min_max_list(array=transformed)
            cols_char_count_dict[col] = {"min": min_list, "max": max_list}
        feature_dict["char_count"] = cols_char_count_dict

        # For the columns with numeric values find min and max per column
        if len(feature_cols_numeric) > 0:
            array_cols_numeric = []
            for col in feature_cols_numeric:
                array_cols_numeric.append(df[col])
            array_cols_numeric = np.hstack(array_cols_numeric).reshape((len(df), len(feature_cols_numeric)))
            min_list, max_list = self.create_min_max_list(array=array_cols_numeric)
            feature_dict["numeric_cols"] = {}
            feature_dict["numeric_cols"]["all"] = {"min": min_list, "max": max_list, "columns": feature_cols_numeric}

        return feature_dict

    def create_feature_matrices(self, df, feature_dict):
        """ Create features. The function only support the known feature types

        Args:
            df (DataFrame) : DataFrame with samples
            feature_dict (dict) : Dictionary with each feature type as keys. For each feature type the necessary
                parameters to create feature from the columns in df
        Returns:
            feature_dict (dict) : Dictionary with features matrices added
        """

        for feature_type in feature_dict:
            type_dict = feature_dict[feature_type]
            if feature_type == "tokenizer":
                for col in list(type_dict.keys()):
                    feature_dict[feature_type][col]["feature_matrix"] = self._tokenize(df[col], type_dict[col])
            elif feature_type == "similarity":
                for col in list(type_dict.keys()):
                    feature_matrix = self._similarity_encode(df[col], type_dict[col]["encoder"])
                    feature_matrix_normalized = (feature_matrix - np.array(type_dict[col]["min"])) / (
                        np.array(type_dict[col]["max"]) - np.array(type_dict[col]["min"]) + 0.000001
                    )
                    feature_dict[feature_type][col]["feature_matrix"] = feature_matrix_normalized
            elif feature_type == "special_char":
                for col in list(type_dict.keys()):
                    feature_matrix = self._create_special_char_array(
                        pd_series=df[col], special_char_list=type_dict[col]["special_char_list"]
                    )
                    feature_matrix_normalized = (feature_matrix - np.array(type_dict[col]["min"])) / (
                        np.array(type_dict[col]["max"]) - np.array(type_dict[col]["min"]) + 0.000001
                    )
                    feature_dict[feature_type][col]["feature_matrix"] = feature_matrix_normalized
            elif feature_type == "char_count":
                for col in list(type_dict.keys()):
                    feature_matrix = self._get_char_counts(pd_series=df[col])
                    feature_matrix_normalized = (feature_matrix - np.array(type_dict[col]["min"])) / (
                        np.array(type_dict[col]["max"]) - np.array(type_dict[col]["min"]) + 0.000001
                    )
                    feature_dict[feature_type][col]["feature_matrix"] = feature_matrix_normalized
            elif feature_type == "numeric_cols":
                feature_matrix = df[type_dict["all"]["columns"]].values
                feature_matrix_normalized = (feature_matrix - np.array(type_dict["all"]["min"])) / (
                    np.array(type_dict["all"]["max"]) - np.array(type_dict["all"]["min"]) + 0.000001
                )
                feature_dict[feature_type]["all"]["feature_matrix"] = feature_matrix_normalized
            else:
                pass
        return feature_dict

    def _clean_string(self, string):
        """ Clean string so that is all digits [0-9] are set to 1 and non alphanumeric characters, dots and spaces are
            set to #
        Args:
            string (str)
        Returns:
            (str) : String where all all digest are replaced by  1 and all special characters by #
        """
        return re.sub(r"[^a-zA-Z0-9 \n.]", "#", re.sub(r"\d|\.(?=\d)", "1", string))

    def _get_char_counts(self, pd_series):
        """ Get character count of each string in a pandas series

        Args:
            pd_series (pandas Series) : Series of strings
        Returns:
            char_counts (numpy ndarray) : Numpy ndarray with the character count for each string in pd_series
        """
        char_counts = pd_series.str.len().values
        # Reshape the array to make sure the array so it has shape (len(pd_series),1)
        return char_counts.reshape((len(pd_series), 1))

    def _get_num_words_column(self, df, column_name, filters):
        """ Get number of words in a columns

        Args:
            df (DataFrame): Pandas DataFrame with the training data
            column_name (str): Name of the column
            filters (str) : Specifies which character that will be filtered from the texts when tokenizing.

        Returns:
             total_num_words (int): The number of words in the column
        """
        tokenizer = Tokenizer(lower=True, filters=filters)
        tokenizer.fit_on_texts(df[column_name])
        sequences = tokenizer.texts_to_sequences(df[column_name])
        total_num_words = len([item for sublist in sequences for item in sublist])
        return total_num_words

    def _find_tokenizer_column(self, feature_cols, df, filters, min_words_column=None, max_num_columns=None):
        """ Choose columns to tokenize from the feature_cols. Select the up to max_num_tokenizer_columns columns that
        have the most unique words and that have at least min_words_column words

        Args:
            feature_cols (list) : List of columns that can be used to generate features
            df (DataFrame): Pandas DataFrame with the training data
            min_words_column (int or None) : The minimum number of words in a column for it to be tokenized (>1), if
                None use 100
            max_num_columns (int or None) : The maximum number of columns that are to be tokenized, if None use
                len(feature_cols)
            filters (str) : Specifies which character that will be filtered from the texts when tokenizing.
        Returns:
            tokenizer_col (list) : List of name of columns to use as tokenizer columns
        """
        if min_words_column is None:
            min_words_column = 100
        if max_num_columns is None:
            max_num_columns = len(feature_cols)
        # Create a dictionary with number of words for each column
        num_words_dict = {}
        list_tokenizer_col = []
        for col in feature_cols:
            num_words_dict[col] = self._get_num_words_column(df=df, column_name=col, filters=filters)

        while (len(num_words_dict) > 0) & (len(list_tokenizer_col) < max_num_columns):
            # Get column with highest number of words
            tokenizer_col = max(num_words_dict, key=num_words_dict.get)
            if num_words_dict.get(tokenizer_col) >= min_words_column:
                list_tokenizer_col.append(tokenizer_col)
                del num_words_dict[tokenizer_col]
            else:
                # If the col with maximum number of words has less than min_num_words, stop the loop
                max_num_columns = 0
        return list_tokenizer_col

    def _create_special_char_list(self, df, column_name, minimum_fraction_of_samples=0.01):
        """ Add special features based on a special character

        Args:
            df (pandas dataFrame) : DataFrame with traing data
            column_name (str) : Name of column to check for special characters
            minimum_fraction_of_samples (float) : The minimum share of samples that have at least one instance of the special
                character for it to be included
        Returns:
            special_char_list (list) : List of special characters with at least one instance in at least min_with_char
                of the samples
        """
        special_char_test = ["-", "/", ")", "(", ";", ":", "!"]
        special_char_list = []
        for special_char in special_char_test:
            new_series = pd.Series([len(x.split(special_char)) - 1 for x in df[column_name]])
            if (sum(new_series > 0) / len(df[column_name])) > minimum_fraction_of_samples:
                special_char_list.append(special_char)
        return special_char_list

    def _create_special_char_array(self, pd_series, special_char_list):
        """ Calculate number of special characters

        Args:
            pd_series (pandas series) : Samples to calculate number of special characters
            special_char_list (list) : List of special characters
        Returns:
            special_array (np narray) : Numpy narray with number of occurrences of each special character per sample
        """
        special = []

        for special_char in special_char_list:
            new_series = [len(x.split(special_char)) - 1 for x in pd_series]
            special.append(new_series)
        # Stack the lists and reshape the array to make sure the array dont have shape (x,)
        special_array = np.hstack(special).reshape((len(pd_series), len(special)))

        return special_array

    def _create_special_char_dict(self, cols_special_char, df, min_fraction_with_car=0.05):
        """ Create a dictionary that for each column in cols_special_char has the list of special characters that are
            relevant to count and include as a feature for the column

        Args:
            cols_special_char (list) : List of columns to search for special characters
            df (pandas DataFrame) : Data frame with data
            min_fraction_with_car (float) : Minimum fraction of samples that have a given special character for it to
                be included
        Returns:
            special_char_dict (dict) : Dictionary with column names as keys and for each key a dictionary with
                 "special_char_list" as key and the list of special characters to include for the given column
        """
        special_char_dict = {}
        for i, col in enumerate(cols_special_char):
            special_char_list = self._create_special_char_list(
                df=df, column_name=col, minimum_fraction_of_samples=min_fraction_with_car
            )
            if len(special_char_list) > 0:
                # Calculate min and max per column (used to normalize)
                transformed = self._create_special_char_array(pd_series=df[col], special_char_list=special_char_list)
                min_list, max_list = self.create_min_max_list(array=transformed)
                special_char_dict[col] = {"special_char_list": special_char_list, "min": min_list, "max": max_list}
        return special_char_dict

    def _init_tokenizer(self, tokenizer_dict_all, df, column_name, filters, maxlen=None):
        """ Initialize a tokenizer and add it to tokenizer_dict_all
        
        Args:
            tokenizer_dict_all (dict) : Empty or containing tokenizer dictionaries for other columns
            df (pandas DataFrame) : Pandas DataFrame with the data
            column_name (str) : Name of column to fit similarity encoder
            filters (str) : Specifies which character that will be filtered from the texts when tokenizing.
            maxlen (int or None) : Maximum length of all sequences of words. If None use min of 100 and shape of 
                tokenized data frame
        Retruns:
            tokenizer_dict_all (dict) : Dictionary with tokenizer dictionary for column column_name added
        """
        tokenizer = Tokenizer(lower=True, filters=filters)
        tokenizer.fit_on_texts(df[column_name])
        total_num_words = len(tokenizer.word_index) + 1
        num_words = round(total_num_words / 2)
        tokenizer = Tokenizer(lower=True, num_words=num_words, filters=filters)
        tokenizer.fit_on_texts(df[column_name])

        sequences_train = tokenizer.texts_to_sequences(df[column_name])

        if not maxlen:
            maxlen = min(pd.DataFrame(sequences_train).shape[1], 100)
        tokenizer_dict_all[column_name] = {"tokenizer": tokenizer, "maxlen": maxlen, "num_words": num_words}
        return tokenizer_dict_all

    def _tokenize(self, pd_series, tokenizer_dict):
        """
        Use the tokenizer
        """

        tokenizer = tokenizer_dict["tokenizer"]
        maxlen = tokenizer_dict["maxlen"]
        sequences = tokenizer.texts_to_sequences(pd_series)
        return pad_sequences(sequences, padding="post", maxlen=maxlen)

    def _init_similarity_encoder(
        self,
        similarity_dict_all,
        df,
        column_name,
        similarity="ngram",
        categories="most_frequent",
        n_prototypes=None,
        cut_at=None,
        random_state=10,
    ):
        """  Add a similarity encoder, https://dirty-cat.github.io/stable/

        Args:
            similarity_dict_all (dict) : Empty or containing similarity encoding dictionaries for other columns
            df (pandas DataFrame) : Pandas DataFrame with the data
            column_name (str) : Name of column to fit similarity encoder
            similarity (str) : String similarities method
            categories (str) : Choice of dimensionality reduction technique ("most_frequent" or "k-means")
            n_prototypes (int or None) : The number the categories are to be reduced to. If None use cut_at times
                number of unique values in column
            cut_at (float or None) : Used to set n_prototypes. If None set to 0.75
            random_state (int) : The seed used by the random number generator
        Returns:
            similarity_dict_all (dict) : Dictionary with similarity encoding dictionary for column column_name added
        """
        # Set n_prototypes to max 'cut_at' of number of unique values in the columns
        if cut_at is None:
            cut_at = 0.75
        if n_prototypes is None:
            n_prototypes = int(max(len(df.loc[:, column_name].unique()) * cut_at, 1))

        similarity_encoder = SimilarityEncoder(
            similarity=similarity,
            dtype=np.float32,
            categories=categories,
            n_prototypes=n_prototypes,
            random_state=random_state,
        )
        # Fit similarity_encoder on data. Calculate min and max per column (used to normalize)
        similarity_encoder.fit(df[column_name].values.reshape(-1, 1))
        transformed = self._similarity_encode(pd_series=df[column_name], similarity_encoder=similarity_encoder)
        min_list, max_list = self.create_min_max_list(array=transformed)
        similarity_dict_all[column_name] = {
            "encoder": similarity_encoder,
            "n_prototypes": n_prototypes,
            "min": min_list,
            "max": max_list,
        }
        return similarity_dict_all

    def _similarity_encode(self, pd_series, similarity_encoder):
        """Use the encoder
        """

        return similarity_encoder.transform(pd_series.values.reshape(-1, 1))

    def create_feature_selection_transformer(self, X_train, y_train, feature_importance_threshold=0.01):
        """ Feature selection using feature importance from random forest.
        The features which have feature importance above threshold in the random forest classifier model is kept.

        Args:
            X_train (array-like) : The training input samples
            y_train (array-like) : The training target values
            feature_importance_threshold (float) : The feature importance threshold. Features with importance above this
                threshold are selected
        Returns:
            sfm_transformer (object): SelectFromModel meta-transformer for selecting features based on importance
                weights
        """
        clf = RandomForestClassifier(random_state=42, n_estimators=10)
        clf.fit(X_train, y_train)
        sfm = SelectFromModel(clf, threshold=feature_importance_threshold)
        sfm_transformer = sfm.fit(X_train, y_train)
        return sfm_transformer

    def create_feature_arrays(self, feature_dict, stack_horizontally=True, indices=None):
        """ Create feature arrays

        Args:
            feature_dict (dict) : Dictionary with each feature type as keys. For each feature_type,the feature matrix
                is stored with the key "feature_matrix"
            stack_horizontally (bool) : If True stack the arrays horizontally
            indices (list /None) : If None use the np array as it is, else use the elements corresponding to the indices
                in the indices list
        Return:
            X (list of numpy ndarrays or a numpy ndarray) : Array with all features arrays either as a list of arrays or
                stacked horizontally
        """
        X = []
        for feature_type, feature_type_dict in feature_dict.items():
            for value in feature_type_dict.values():
                array = value["feature_matrix"]
                if indices is not None:
                    array = array[indices]
                X.append(array)
        if stack_horizontally:
            X = np.hstack(X)
        return X

    def create_min_max_list(self, array):
        """Calculate min and max per column in array. If min and max are the same, set min to 0.
        Also convert min and max arrays to list of items of type float64 to be able to save.

        Args:
            array (numpy ndarray): Array to find min and max per column
        Returns:
            min_list (list) : List of minimum values per column in array (0 if min=max)
            max_list (list) : List of maximum values per column in array
        """
        min_columns = array.min(axis=0)
        max_columns = array.max(axis=0)
        # If an element in min_columns and max_columns is the same, set min_columns = 0 and max_columns = 1
        min_list = [float(x) if x != max_columns[i] else 0 for i, x in enumerate(min_columns)]
        max_list = [float(x) for x in max_columns]
        return min_list, max_list
