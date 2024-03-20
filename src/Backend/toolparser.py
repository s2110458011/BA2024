import pandas as pd
import numpy as np

def load_data_from_csv(file: str) -> pd.DataFrame:
    """Read CSV-File from path into a Dataframe.

    Args:
        file (str): path to a csv file

    Returns:
        pd.DataFrame: Dataframe with survey data. Columns headers are the questions
    """

    df = pd.read_csv(file, header=0)
    df = df.drop(columns='Zeitstempel')
    return df

def extract_features(df: pd.DataFrame) -> np.array:
    """_summary_

    Args:
        df (pd.DataFrame): Dataframe with survey data, headers are the questions.

    Returns:
        np.array: _description_
    """

    features = []
    for column in df:
        features.append(column)
    features = np.asarray(features)
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

def get_answers_for_question(df: pd.DataFrame, question: str) -> pd.DataFrame:
    all_answers = df[question]
    all_answers = all_answers.to_frame(name=question)
    all_answers = all_answers.groupby(question).size().to_frame(name='Count')
    return all_answers