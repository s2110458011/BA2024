import pandas as pd

class SurveyDescription():
    
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
    
    def describe_input_data(self):
        return self.data.describe()
    
    def count_responses(self) -> int:
        return self.data.shape[0]
    
    def number_of_questions(self):
        return self.data.shape[1]
    
    def surveycompletion_counts(self, percentages: list) -> pd.DataFrame:
        row_counts = self.data.notnull().sum(axis=1)
        total_cols = self.data.shape[1]
        row_completion_pct = (row_counts / total_cols) * 100
        
        counts = []
        
        for pct in percentages:
            count = (row_completion_pct == pct).sum()
            counts.append({'Completion_%': pct, 'Count': count})
        
        counts_df = pd.DataFrame(counts)
        return counts_df
    
    def surveycompletion_precentages(self):
        percentages = []
        