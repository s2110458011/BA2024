import pandas as pd
import numpy as np
import backend.data_processor.toolparser as tp

class ChartLogic():
    def __init__(self, raw_data: pd.DataFrame) -> None:
        self.raw_data = raw_data
        self.charts_per_question_simple = self.initialize_simple_chart_options()
        
        return None
    
    def initialize_simple_chart_options(self) -> dict:
        default_value = []
        question_list = tp.extract_features(self.raw_data)
        self.charts_per_question_simple = {question: default_value for question in question_list}
        self.create_chart_options_list_per_question()
        return self.charts_per_question_simple
    
    def create_chart_options_list_per_question(self) -> dict:
        for key in self.charts_per_question_simple.keys():
            data_column = pd.DataFrame(self.raw_data[key])
            print(data_column)
            print(data_column.dtypes)
            chart_options = self.get_chart_options_single(data_column)
            self.charts_per_question_simple[key] = chart_options
        
        return self.charts_per_question_simple
    
    def get_simple_chart_options(self) -> dict:
        return self.charts_per_question_simple
    
    def get_chart_options_single(self, data: pd.DataFrame) -> list:
        #if data.size == 0:
        if data.empty:
            return []
        else:
            #data = data[~np.isnan(data)]
            data.dropna(inplace=True)
            if data.iloc[:, 0].dtype == 'category':
                return ['bar', 'pie']
            elif np.issubdtype(data.iloc[:, 0].dtype, np.datetime64):
                return ['bar', 'line']