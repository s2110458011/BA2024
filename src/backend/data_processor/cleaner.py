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

def set_index_column_by_name(data: pd.DataFrame, index_column: str) -> pd.DataFrame:
    new_df = data.set_index(index_column)
    return new_df

def drop_time_component(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if column == 'index':
        try:
            data.index = pd.to_datetime(data.index, dayfirst=True)
            data.index = data.index.date
        except ValueError:
            #TODO catch error
            pass
    else:
        try:
            data[column] = pd.to_datetime(data[column])
            data[column] = data[column].dt.date
        except ValueError:
            #TODO catch error
            pass
    return data

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

def drop_rows_by_index(data: pd.DataFrame, indices: list) -> tuple[int, pd.DataFrame]:
    new_df = data.drop([indices])
    count_dropped = get_count_dropped([data, new_df])
    return count_dropped, new_df

def drop_rows_by_threshold(data: pd.DataFrame, column: str, threshold: float) -> tuple[int, pd.DataFrame]:
    new_df = data.drop(data[data[column] > threshold].index)
    count_dropped = get_count_dropped([data, new_df])
    return count_dropped, new_df

def drop_rows_by_value(data: pd.DataFrame, column: str, value_condition: str) -> tuple[int, pd.DataFrame]:
    new_df = data.drop(data[data[column] == value_condition].index)
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