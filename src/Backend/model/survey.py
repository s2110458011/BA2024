import pandas as pd
import backend.data_processor.cleaner as cl
from matplotlib.figure import Figure
from backend.analysis.chart_logic import ChartLogic

class Survey():
    def __init__(self, id:int, name: str, data: pd.DataFrame) -> None:
        self.id = id
        self.name = name
        self.raw_data = data
        self.prepared_data = data
        self.categorized_questions = {}
        self.not_categorized_questions = None
        self.chart_logic = ChartLogic(data)
        self.simple_charts_by_question = self.chart_logic.get_simple_chart_options()
    
    #region getter & setter
    
    def get_data(self) -> pd.DataFrame:
        return self.raw_data
    
    def set_datatype_by_question(self, question, datatype) -> None:
        # insert if -> check if conversion to int/float = parse
        self.prepared_data[question] = self.prepared_data[question].astype(datatype)
        print(self.prepared_data[question].dtype)
        return None
    
    def set_uncategorized_questions(self, free_questions: list) -> None:
        self.not_categorized_questions = free_questions
        return None
    
    def get_uncategorized_questions(self) -> list:
        return self.not_categorized_questions
    
    def get_data_from_category(self, category: str) -> pd.DataFrame:
        category_columns = self.categorized_questions[category]
        df = cl.extract_columns_by_name(category_columns)
        return df
    
    def get_responses_to_question(self, question: str):
        return self.raw_data[question]
    
    def get_chart_options_by_question(self, question: str) -> list:
        return self.simple_charts_by_question[question]
    
    #endregion
    
    def questions_categorized(self) -> bool:
        return self.categorized_questions
    
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
    
    def create_chart(self, chart_type, question) -> Figure:
        match chart_type:
            case 'line':
                return self.chart_logic.create_simple_line_chart(question)
            case 'bar':
                return self.chart_logic.create_simple_bar_chart(question)
            case 'pie':
                return self.chart_logic.create_simple_pie_chart(question)
    
    def switch_axes(self) -> Figure:
        return self.chart_logic.switch_axes_simple_bar_chart()
    
    def set_current_chart_question(self, question) -> None:
        self.chart_logic.set_current_question(question)
        return None