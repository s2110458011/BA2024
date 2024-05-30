import pandas as pd
import numpy as np
import seaborn as sns
import backend.analysis.toolparser as tp
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from PIL import Image
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class ChartLogic():
    def __init__(self, raw_data: pd.DataFrame) -> None:
        self.charts_per_question_simple: dict = self.initialize_simple_chart_options(raw_data)
        sns.set_theme(style='darkgrid')
        self.chart_simple_x: str = None
        self.chart_simple_y: str = 'count'
        self.current_question: str = None
        self.chart_data: pd.DataFrame = None
        self.barchart_init_axes: bool = True
        self.advanced_chart_dimensions: dict[str: str] = {'x': None, 'y': None, 'z': None}
        self.advanced_chart_data: pd.DataFrame = None
        self.img: Image = None
        return None
    
    #region Simple Charts
    
    def initialize_simple_chart_options(self, raw_data: pd.DataFrame) -> dict:
        default_value = []
        question_list = tp.extract_features(raw_data)
        self.charts_per_question_simple = {question: default_value for question in question_list}
        self.create_chart_options_list_per_question(raw_data)
        return self.charts_per_question_simple
    
    def update_simple_chart_options(self, raw_data: pd.DataFrame) -> None:
        self.initialize_simple_chart_options(raw_data)
        return None
    
    def set_current_question(self, question) -> str:
        self.current_question = question
        return question
    
    def create_chart_options_list_per_question(self, raw_data: pd.DataFrame) -> dict:
        for key in self.charts_per_question_simple.keys():
            data_column = pd.DataFrame(raw_data[key])
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
            elif data.iloc[:, 0].dtype == 'float':
                return ['bar', 'histogram']
            elif data.iloc[:, 0].dtype == 'int':
                return ['bar', 'histogram']
            elif np.issubdtype(data.iloc[:, 0].dtype, np.datetime64):
                return ['bar', 'line']
    
    def create_simple_line_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.chart_data = self.get_data_for_simple_chart(raw_data)
        self.chart_simple_x = self.current_question
        self.ax.clear()
        sns.lineplot(self.chart_data, x=self.current_question, y=self.chart_simple_y, ax=self.ax)
        if report_image:
            self.create_image()
        return self.figure
    
    def create_simple_bar_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.chart_data = self.get_data_for_simple_chart(raw_data)
        self.chart_simple_x = self.current_question
        if not report_image:
            self.barchart_init_axes = True
        self.ax.clear()
        sns.barplot(self.chart_data, x=self.current_question, y=self.chart_simple_y, ax=self.ax)
        if self.chart_data[self.current_question].size > 5:
            self.ax.tick_params(axis='x', rotation=55)
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
                self.ax.tick_params(axis='x', rotation=55)
            self.barchart_init_axes = False
        else:
            sns.barplot(self.chart_data, x=self.chart_simple_x, y=self.chart_simple_y, ax=self.ax)
            if self.chart_data[self.chart_simple_x].size > 5:
                self.ax.tick_params(axis='x', rotation=55)
            self.barchart_init_axes = True
        return self.figure
    
    def create_simple_pie_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.ax.clear()
        self.chart_data = self.get_data_for_simple_chart(raw_data)
        self.ax.pie(self.chart_data[self.chart_simple_y], labels=self.chart_data[self.current_question], autopct='%1.1f%%', startangle=140)
        if report_image:
            self.create_image()
        return self.figure
    
    def get_data_for_simple_chart(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        data = raw_data[self.current_question]
        if pd.api.types.is_datetime64_any_dtype(data):
            data = pd.DataFrame(data.dt.date)
        result_df = data.value_counts().sort_index().reset_index()
        return result_df
    
    def create_image(self) -> None:
        canvas = FigureCanvas(self.figure)
        canvas.draw()
        self.img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        return None
    
    #endregion Simple Charts
    
    #region Advanced Charts
    
    def update_plot_dimensions(self, df_column: str, dimension: str) -> None:
        self.advanced_chart_dimensions[dimension] = df_column
        return None
    
    def create_catplot_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        self.set_up_figure(report_image)
        
        x = self.advanced_chart_dimensions['x']
        y = self.advanced_chart_dimensions['y']
        z = self.advanced_chart_dimensions['z']
        self.chart_data = raw_data[[x, y, z]]
        catplot = sns.catplot(data=self.chart_data, x=x, y=y, col=z)
        if self.chart_data[x].size > 3:
            for ax in catplot.axes.flat:
                ax.tick_params(axis='x', rotation=55)
        plt.close(catplot.figure)
        self.figure = catplot.figure
        if report_image:
            self.create_image()
        return self.figure
    
    def create_sns_scatterplot_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        self.set_up_figure(report_image)
        
        x = self.advanced_chart_dimensions['x']
        y = self.advanced_chart_dimensions['y']
        df = self.compute_counts_of_observation(raw_data, x, y)
        sns.scatterplot(data=df, x=x, y=y, size='count', ax=self.ax)
        self.ax.tick_params(axis='x', rotation=55)
        if report_image:
            self.create_image()
        return self.figure
    
    def compute_counts_of_observation(self, raw_data: pd.DataFrame, cat1: str, cat2: str) -> pd.DataFrame:
        df_counts = raw_data.groupby([cat1, cat2]).size().reset_index()
        df_counts.columns.values[df_counts.columns==0] = 'count'
        return df_counts
    
    def create_countplot_chart(self, raw_data: pd.DataFrame, report_image: bool) -> Figure:
        self.set_up_figure(report_image)
        
        x = self.advanced_chart_dimensions['x']
        y = self.advanced_chart_dimensions['y']
        self.chart_data = raw_data[[x, y]]
        sns.countplot(data=self.chart_data, x=x, hue=y, ax=self.ax)
        if report_image:
            self.create_image()
        return self.figure
    
    def set_up_figure(self, report_image: bool) -> None:
        if report_image:
            self.figure = Figure(figsize=(6, 4), dpi=300, tight_layout=True)
        else:
            self.figure = Figure(tight_layout=True)
        self.ax = self.figure.subplots()
        self.ax.clear()
        return None
    
    #endregion Advanced Charts
        