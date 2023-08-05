import json
import os
import pickle

import pandas as pd
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.models import model_from_json
from tensorflow.keras.utils import CustomObjectScope


def save_keras_model(model, file_name="model", file_dir=""):
    """ Save a Keras model

    Args:
        model: Keras model
        file_name (str) : Name of the saved file
        file_dir (str) : Name of directory to save the model
    """
    file_path = os.path.join(file_dir, file_name)
    model_json = model.to_json()
    with open(file_path + ".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(file_path + ".h5")


def load_keras_model(file_name="model", file_dir=""):
    """ Load a Keras model

    Args:
        file_name (str) : Name of the file with the model
        file_dir (str) : Name of directory where the model is saved
    Returns:
        model: Keras model
    """
    file_path = os.path.join(file_dir, file_name)
    json_file = open(file_path + ".json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    # load the saved model
    with CustomObjectScope({"GlorotUniform": glorot_uniform()}):
        model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(file_path + ".h5")
    return model


def save_json(obj, file_name, file_dir=""):
    """ Save a json object

    Args:
        obj: The object to be saved in a json file
        file_name (str) : Name of the saved file
        file_dir (str) : Name of directory to save the json
    """
    file_path = os.path.join(file_dir, file_name)
    with open(file_path + ".txt", "w") as outfile:
        json.dump(obj, outfile)


def load_json(file_name, file_dir=""):
    """ Load a json object

    Args:
        file_name (str) : Name of the file with the json
        file_dir (str) : Name of directory where the json is saved
    Returns:
        obj: The object in the json file
    """
    file_path = os.path.join(file_dir, file_name)
    with open(file_path + ".txt") as json_file:
        obj = json.load(json_file)
    return obj


def save_csv(df, file_name, file_dir=""):
    """ Save a csv file

    Args:
        df (data frame) : Pandas data frame that will be saved as a csv
        file_name (str) : Name of the saved file
        file_dir (str) : Name of directory to save the csv
    """
    file_path = os.path.join(file_dir, file_name)
    df.to_csv(file_path + ".csv", index=False)


def load_csv(file_name, file_dir=""):
    """ Load a csv file

    Args:
        file_name (str) : Name of the file with the csv
        file_dir (str) : Name of directory where the csv file is saved
    Returns:
        df (data frame) : The pandas data frame stored in the csv
    """
    file_path = os.path.join(file_dir, file_name)
    df = pd.read_csv(file_path + ".csv")
    return df


def save_pickle(obj, file_name, file_dir=""):
    """ Save a pickle file

    Args:
        obj : The object to save
        file_name (str) : Name of the saved file
        file_dir (str) : Name of directory to save the file
    """
    file_path = os.path.join(file_dir, file_name)
    with open(file_path + ".pickle", "wb") as handle:
        pickle.dump(obj, handle)


def load_pickle(file_name, file_dir=""):
    """ Load a pickle file

    Args:
        file_name (str) : Name of the file with the pickle
        file_dir (str) : Name of directory where the pickle file is saved
    Returns:
        obj: The object saved in the file
    """
    file_path = os.path.join(file_dir, file_name)
    with open(file_path + ".pickle", "rb") as handle:
        obj = pickle.load(handle)
    return obj


def save_label_encoder_dict(label_encoder_dict, file_dir=""):
    """ Save the one-hot encoder as pickle files and remove it from label_encoder_dict.
    Save the label_encoder_dict as a json

    Args:
        label_encoder_dict (dict) : Dictionary with one-hot encoder, type decoder and encoder
        file_dir (str) : Name of directory to save the feature_dict
    """
    for encoder_type in label_encoder_dict:
        if encoder_type == "one_hot_encoder":
            one_hot_encoder = label_encoder_dict[encoder_type]
            save_pickle(obj=one_hot_encoder, file_name="one_hot_encoder", file_dir=file_dir)
            label_encoder_dict[encoder_type] = ""
    save_json(obj=label_encoder_dict, file_name="label_encoder_dict", file_dir=file_dir)


def load_label_encoder_dict(file_dir=""):
    """ Load label_encoder_dict from json file and load the one-hot-encoder from pickle files and add it
    to the label_encoder_dict

    Args:
        file_dir (str) : Name of directory to save the feature_dict
    Returns:
        label_encoder_dict (dict) : Dictionary with one-hot encoder, type decoder and encoder
    """
    # Load feature_dict
    label_encoder_dict = load_json(file_name="label_encoder_dict", file_dir=file_dir)
    # Load the tokenizer and similarity encoder and add them to feature_dict
    for encoder_type in label_encoder_dict:
        if encoder_type == "one_hot_encoder":
            one_hot_encoder = load_pickle(file_name="one_hot_encoder", file_dir=file_dir)
            label_encoder_dict["one_hot_encoder"] = one_hot_encoder
        if encoder_type == "decoder":
            # Convert keys back to int
            decoder = {int(k): v for k, v in label_encoder_dict["decoder"].items()}
            label_encoder_dict["decoder"] = decoder
    return label_encoder_dict


def save_feature_dict(feature_dict, file_dir=""):
    """ Save the tokenizer and similarity encoder as pickle files and remove them from feature_dict.
    Save the feature_dict as a json

    Args:
        feature_dict (dict) : Dictionary with each feature type as keys
        file_dir (str) : Name of directory to save the feature_dict
    """
    for feature_type in feature_dict:
        if feature_type == "tokenizer":
            type_dict = feature_dict[feature_type]
            for col in list(type_dict.keys()):
                save_pickle(obj=type_dict[col]["tokenizer"], file_name=f"tokenizer_{col}", file_dir=file_dir)
                feature_dict["tokenizer"][col]["tokenizer"] = ""
        if feature_type == "similarity":
            type_dict = feature_dict[feature_type]
            for col in list(type_dict.keys()):
                save_pickle(obj=type_dict[col]["encoder"], file_name=f"similarity_{col}", file_dir=file_dir)
                feature_dict["similarity"][col]["encoder"] = ""
    save_json(obj=feature_dict, file_name="feature_dict", file_dir=file_dir)


def load_feature_dict(file_dir=""):
    """ Load feature_dict from json file and load the tokenizer and similarity encoder from pickle files and add them
    to the feature_dict

    Args:
        file_dir (str) : Name of directory to save the feature_dict
    Returns:
        feature_dict (dict) : Dictionary with each feature type as keys
    """
    # Load feature_dict
    feature_dict = load_json(file_name="feature_dict", file_dir=file_dir)
    # Load the tokenizer and similarity encoder and add them to feature_dict
    for feature_type in feature_dict:
        if feature_type == "tokenizer":
            type_dict = feature_dict[feature_type]
            for col in list(type_dict.keys()):
                tokenizer = load_pickle(file_name=f"tokenizer_{col}", file_dir=file_dir)
                feature_dict["tokenizer"][col]["tokenizer"] = tokenizer
        if feature_type == "similarity":
            type_dict = feature_dict[feature_type]
            for col in list(type_dict.keys()):
                similarity_encoder = load_pickle(file_name=f"similarity_{col}", file_dir=file_dir)
                feature_dict["similarity"][col]["encoder"] = similarity_encoder
    return feature_dict
