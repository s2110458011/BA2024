import pandas as pd
import backend.data_processor.cleaner as cl

class Survey():
    def __init__(self, id:int, name: str, data: pd.DataFrame) -> None:
        self.id = id
        self.name = name
        self.raw_data = data
        self.categorized_questions = {}
        self.not_categorized_questions = None
    
    def get_data(self) -> pd.DataFrame:
        return self.raw_data
    
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
    
    def get_uncategorized_questions(self) -> list:
        return self.not_categorized_questions
    
    def set_uncategorized_questions(self, free_questions: list) -> None:
        self.not_categorized_questions = free_questions
        return None
    
    def add_question_to_category(self, category: str, question: str) -> None:
        if category not in self.categorized_questions:
            self.categorized_questions[category] = [question]
        else:
            self.categorized_questions[category].append(question)
        return None
    
    def add_new_category(self, category: str) -> None:
        if category not in self.categorized_questions:
            self.categorized_questions[category] = []
        return None
    
    def get_data_from_category(self, category: str) -> pd.DataFrame:
        category_columns = self.categorized_questions[category]
        df = cl.extract_columns_by_name(category_columns)
        return df