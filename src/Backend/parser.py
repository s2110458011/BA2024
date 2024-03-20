import pandas as pd

def load_data_from_csv(file: str) -> pd.DataFrame:
    df = pd.read_csv(file, header=0)
    return df