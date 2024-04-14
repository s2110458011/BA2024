import pandas as pd

class Survey():
    def __init__(self, data: pd.DataFrame) -> None:
        self.raw_data = data
    
    def describe_input_data(self) -> pd.DataFrame:
        return self.raw_data.describe()
    
    def count_responses(self) -> int:
        return self.raw_data.shape[0]
    
    def number_of_questions(self) -> tuple[int, int]:
        return self.raw_data.shape[1]
    
    def surveycompletion_counts(self, percentages: list) -> pd.DataFrame:
        row_counts = self.raw_data.notnull().sum(axis=1)
        total_cols = self.raw_data.shape[1]
        row_completion_pct = (row_counts / total_cols) * 100
        
        counts = []
        
        for pct in percentages:
            count = (row_completion_pct == pct).sum()
            counts.append({'Completion_%': pct, 'Count': count})
        
        counts_df = pd.DataFrame(counts)
        return counts_df
    
    def surveycompletion_precentages_per_row(self) -> pd.DataFrame:
        df = self.raw_data.copy()
        num_cols = df.shape[1]
        df['completion'] = (df.notnull().sum(axis=1) / num_cols) * 100
        return df
        