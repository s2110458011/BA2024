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
    return df

def extract_features(df: pd.DataFrame) -> np.array:
    features = []
    for column in df:
        if column == 'Zeitstempel':
            continue
        features.append(column)
    features = np.asarray(features)
    return features