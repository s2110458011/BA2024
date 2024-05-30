import pandas as pd

"""clean the original dataframe, e.g. remove columns or rows
"""

#region Helper functions
def get_count_dropped(dataframes: list) -> int:
    if len(dataframes) == 2:
        df_0 = dataframes[0].shape[1]
        df_1 = dataframes[1].shape[1]
        if  df_0 > df_1:
            return df_0 - df_1
        else:
            return df_1 - df_0
    else:
        return 0

#endregion

# region Feature extraction
def extract_columns_by_name(data: pd.DataFrame, columns: list) -> pd.DataFrame:
    new_df = data[columns]
    return new_df

def prepare_column_for_float(data: pd.DataFrame, column) -> pd.DataFrame:
    values = list(data[column])
    for idx, val in enumerate(values):
        if not isinstance(val, float):
            new = val.replace(',', '.')
            values[idx] = new
    data[column] = values
    return data

def drop_columns_by_name(data: pd.DataFrame, columns: list) -> tuple[int, pd.DataFrame]:
    new_df = data.drop(columns=columns)
    count_dropped = get_count_dropped([data, new_df])
    return count_dropped, new_df

def remove_text_in_column(data: pd.DataFrame, question: str, text: str) -> pd.DataFrame:
    data[question] = data[question].astype('object')
    column = list(data[question])
    for idx, val in enumerate(column):
        if not pd.isna(val):
            n_val = val.replace(text, '').strip()
            column[idx] = n_val
    data[question] = column
    return data

# endregion