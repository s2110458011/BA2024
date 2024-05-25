import pandas as pd
import numpy as np
import seaborn as sns
import backend.data_processor.toolparser as tp
from matplotlib.figure import Figure

from PIL import Image
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ChartLogic():
    def __init__(self, raw_data: pd.DataFrame) -> None:
        self.raw_data = raw_data
        self.charts_per_question_simple = self.initialize_simple_chart_options()
        sns.set_theme(style='darkgrid')
        self.chart_simple_x = None
        self.chart_simple_y = 'count'
        self.current_question = None
        self.chart_data = None
        self.barchart_init_axes = True
        self.img = None
        
        return None
    
    def initialize_simple_chart_options(self) -> dict:
        default_value = []
        question_list = tp.extract_features(self.raw_data)
        self.charts_per_question_simple = {question: default_value for question in question_list}
        self.create_chart_options_list_per_question()
        return self.charts_per_question_simple
    
    def set_current_question(self, question) -> str:
        self.current_question = question
        return question
    
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
        if data.empty:
            return []
        else:
            data.dropna(inplace=True)
            if data.iloc[:, 0].dtype == 'category':
                return ['bar', 'pie']
            elif np.issubdtype(data.iloc[:, 0].dtype, np.datetime64):
                return ['bar', 'line']
    
    def create_simple_line_chart(self, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.chart_data = self.get_data_for_simple_chart(self.current_question)
        self.chart_simple_x = self.current_question
        self.ax.clear()
        sns.lineplot(self.chart_data, x=self.current_question, y=self.chart_simple_y, ax=self.ax)
        if report_image:
            self.create_image()
        return self.figure
    
    def create_simple_bar_chart(self, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.chart_data = self.get_data_for_simple_chart(self.current_question)
        self.chart_simple_x = self.current_question
        if not report_image:
            self.barchart_init_axes = True
        self.ax.clear()
        sns.barplot(self.chart_data, x=self.current_question, y=self.chart_simple_y, ax=self.ax)
        if self.chart_data[self.current_question].size > 5:
            self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90, ha='right')
        if report_image:
            self.create_image()
        return self.figure
    
    def get_image(self) -> Image:
        return self.img
    
    def switch_axes_simple_bar_chart(self) -> Figure:
        self.ax.clear()
        if self.barchart_init_axes:
            sns.barplot(self.chart_data, x=self.chart_simple_y, y=self.chart_simple_x, ax=self.ax)
            if self.chart_data[self.chart_simple_y].size > 5:
                self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90, ha='right')
            self.barchart_init_axes = False
        else:
            sns.barplot(self.chart_data, x=self.chart_simple_x, y=self.chart_simple_y, ax=self.ax)
            if self.chart_data[self.chart_simple_x].size > 5:
                self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90, ha='right')
            self.barchart_init_axes = True
        
        #self.create_image()
        return self.figure
    
    def create_simple_pie_chart(self, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.ax.clear()
        self.chart_data = self.get_data_for_simple_chart(self.current_question)
        self.ax.pie(self.chart_data[self.chart_simple_y], labels=self.chart_data[self.current_question], autopct='%1.1f%%', startangle=140)
        if report_image:
            self.create_image()
        return self.figure
    
    def get_data_for_simple_chart(self, question) -> pd.DataFrame:
        data = self.raw_data[self.current_question]
        if pd.api.types.is_datetime64_any_dtype(data):
            data = pd.DataFrame(data.dt.date)
        result_df = data.value_counts().sort_index().reset_index()
        print(result_df)
        return result_df
    
    def create_image(self) -> None:
        canvas = FigureCanvas(self.figure)
        canvas.draw()
        self.img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        return None
        