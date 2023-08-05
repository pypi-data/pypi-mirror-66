import pandas as pd

from cognite.osc.exceptions import (
    ColumnNotInDataFrame,
    EmptyFeatureException,
    EmptyListException,
    MissingColumnException,
    TooFewSamplesPerClassException,
    WrongTypeException,
)


def validate_type_col(type_col, df):
    """ Validate that type_col is a column in df

    Args:
        type_col (string) : Name of the column with the target
        df (pandas DataFrame) : Data frame with samples
    """
    validate_type_of_parametes(parameter_list=[type_col], correct_type_list=[str])
    if type_col not in df:
        raise MissingColumnException(f"The target column, {type_col}, must be a column in the data frame.")


def validate_types_of_interest(types_of_interest):
    """ Validate that the types_of_interest-parameter is a list of at least length 1
    Args:
        types_of_interest (list) : List of types of interest
    """
    validate_type_of_parametes(parameter_list=[types_of_interest], correct_type_list=[list])
    if len(types_of_interest) == 0:
        raise EmptyListException(f"The types_of_interest is empty, it must contain at least one item")


def validate_num_samples_types_of_interest(types_of_interest, type_col, df):
    """ Validate that each type_of_interest have at least 2 samples

    Args:
        types_of_interest (list) : List of types of interest
        type_col (string) : Name of the column with the target
        df (pandas DataFrame) : Data frame with samples
    """
    # Count number of samples per unique value in type_col
    count_labels = pd.DataFrame({"num": df.groupby([type_col]).size()}).reset_index()
    # Add types_of_interest that are not in df
    count_labels = pd.merge(pd.Series(types_of_interest, name=type_col), count_labels, how="outer").fillna(0)

    too_few_samples = count_labels.loc[(count_labels["num"] < 2) & count_labels[type_col].isin(types_of_interest), :]
    if too_few_samples.shape[0] > 0:
        raise TooFewSamplesPerClassException(
            f"All types must have at least 2 samples, {list(too_few_samples[type_col])} have "
            f"{list(too_few_samples['num'])}. Create more labels or adjust the train-size."
        )


def validate_columns_in_df(df, columns_list):
    """Validate that all of the items in columns_list are columns in df

    Args:
        df (pandas DataFrame) : Data frame with samples
        columns_list (list) : List of all columns
    """
    columns_not_in_df = [x for x in columns_list if x not in df.columns]
    if len(columns_not_in_df) > 0:
        raise ColumnNotInDataFrame(
            f"Columns {columns_not_in_df} are not in data frame, all input columns must be in data frame."
        )


def validate_type_of_parametes(parameter_list, correct_type_list):
    """Validate that parameters in  parameter_list have the types in correct_type_list

    Args:
        parameter_list (list) : List of the parameters to check
        correct_type_list (list) : List of the type that the parameter should have. If multiple types are accepted for
            the i-th parameter, the i-th element of correct_type_list  is a list of the accepted types
    """
    wrong_type_parameters = []
    correct_types = []
    has_type = []
    add = False
    for i, x in enumerate(parameter_list):
        # The correct type might be a list of different types that are all acceptable
        if type(correct_type_list[i]) == list:
            if type(x) not in correct_type_list[i]:
                add = True
        else:
            if type(x) != correct_type_list[i]:
                add = True
        if add:
            wrong_type_parameters.append(x)
            correct_types.append(correct_type_list[i])
            has_type.append(type(x))

    if add:
        raise WrongTypeException(
            f"The input parameters with value {wrong_type_parameters} has type {has_type}, "
            f"but the parameters must have types {correct_types}."
        )


def validate_non_empty_feature_columns(df, string_feature_columns):
    """Validate that none of the feature columns contain only empty strings

    Args:
        df (pandas DataFrame) : Data frame with samples
        string_feature_columns (list) : List of all columns in df that have type string
    """
    for col in string_feature_columns:
        if sum(df[col] != "") == 0:
            raise EmptyFeatureException(
                "There is at least one feature that only contains empty strings, all string features must include at "
                "least one non-empty string."
            )
