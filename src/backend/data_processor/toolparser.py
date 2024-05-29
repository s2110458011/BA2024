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

def count_responses_for_unique_answers(df: pd.DataFrame, question: str) -> pd.DataFrame:
    """Determine count of responses for each unique answer.

    Args:
        df (pd.DataFrame): Dataframe with survey data, headers represent the questions.
        question (str): Question for which the answers should be counted.

    Returns:
        pd.DataFrame: Df, each row represents a unique answer and a column count with how many responses.
    """

    all_answers = df[question]
    all_answers = all_answers.to_frame(name=question)
    all_answers = all_answers.groupby(question).size().to_frame(name='Count')
    return all_answers

def count_responses_for_question(df: pd.DataFrame, question:str) -> int:
    """Count the number of responses for a given question. Does not inclue NaN values = no answer was provided.

    Args:
        df (pd.DataFrame): _description_
        question (str): _description_

    Returns:
        int: _description_
    """
    return df[question].count()

def get_column_by_name(data: pd.DataFrame, column_name: str) -> np.array:
    column = data[column_name]
    return np.array(column)