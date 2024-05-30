import pandas as pd
import numpy as np

def load_data_from_csv(file: str) -> pd.DataFrame:
    """Read CSV-File from path into a Dataframe.

    Args:
        file (str): path to a csv file

    Returns:
        pd.DataFrame: Dataframe with survey data. Columns headers are the questions
    """

    df = pd.read_csv(file, header=0, parse_dates=[0], dayfirst=True)
    df = infer_datatypes(df)
    #df = df.drop(columns='Zeitstempel')
    return df

def infer_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    for column_name, column in df.items():
        idx = 0
        if column.dtype =='object':
            sample_value = column.iloc[idx]
            while sample_value != sample_value:
                idx += 1
                sample_value = column.iloc[idx]
            if isinstance(sample_value, str):
                df[column_name]= df[column_name].astype('category')
            elif isinstance(sample_value, int):
                df[column_name]= df[column_name].astype('int32')
            elif isinstance(sample_value, float):
                df[column_name]= df[column_name].astype('float')
    return df

def extract_features(df: pd.DataFrame) -> list:
    """_summary_

    Args:
        df (pd.DataFrame): Dataframe with survey data, headers are the questions.

    Returns:
        list: _description_
    """

    features = []
    for column in df:
        features.append(column)
    return features

def extract_possible_answers(df: pd.DataFrame) -> dict:
    """Extract unique (possible) answers from survey data for all questions.

    Args:
        df (pd.DataFrame): Dataframe with survey data, headers are the questions.

    Returns:
        dict: Questions: Unique answers
    """

    answers = {}
    for column in df:
        answers[column] = df[column].unique()
    return answers