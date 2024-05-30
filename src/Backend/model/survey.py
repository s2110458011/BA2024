import pandas as pd
import backend.analysis.cleaner as cl
import backend.analysis.toolparser as tp
import backend.constants as constants
from matplotlib.figure import Figure
from backend.analysis.chart_logic import ChartLogic
from backend.model.report_model import PDFReport
from backend.model.report_item_model import ReportItem

class Survey():
    def __init__(self, id:int, name: str, data: pd.DataFrame) -> None:
        self.id = id
        self.name: str = name
        self.raw_data: pd.DataFrame = data
        self.categorized_questions: dict[str, list[str]] = {}
        self.not_categorized_questions: list = tp.extract_features(self.raw_data)
        self.selected_question: str = None
        self.chart_logic = ChartLogic(data)
        self.simple_charts_by_question = self.chart_logic.get_simple_chart_options()
        self.next_report_item_number = 1
        self.report_items: dict = {}
        self.pdf_report: PDFReport = None
        
    
    #region getter & setter
    
    def get_data(self) -> pd.DataFrame:
        return self.raw_data
    
    def set_datatype_by_question(self, question: str, datatype: str) -> str | None:
        # insert if -> check if conversion to int/float = parse
        try:
            self.raw_data[question] = self.raw_data[question].astype(datatype)
            self.chart_logic.update_simple_chart_options(self.raw_data)
        except ValueError:
            if datatype == 'float':
                self.raw_data = cl.prepare_column_for_float(self.raw_data, question)
                self.raw_data[question] = self.raw_data[question].astype(datatype)
                self.chart_logic.update_simple_chart_options(self.raw_data)
            if datatype == 'int':
                return 'Cannot convert to datatype int, convert to float instead?'
        return None
    
    def set_uncategorized_questions(self, free_questions: list) -> None:
        self.not_categorized_questions = free_questions
        return None
    
    def set_current_chart_question(self, question) -> None:
        self.chart_logic.set_current_question(question)
        return None
    
    def set_current_preparation_question(self, question) -> None:
        self.selected_question = question
        return None
    
    def get_current_preparation_question(self) -> str | None:
        return self.selected_question
    
    def get_uncategorized_questions(self) -> list:
        return self.not_categorized_questions
    
    def get_responses_to_question(self, question: str):
        return self.raw_data[question]
    
    def get_chart_options_by_question(self, question: str) -> list:
        return self.simple_charts_by_question[question]
    
    def get_next_report_item_number(self) -> int:
        return self.next_report_item_number
    
    def get_report_items_list(self) -> list:
        return self.report_items.keys()
    
    def get_report_item(self, key) -> ReportItem:
        return self.report_items[key]
    
    def get_pdf_report(self) -> PDFReport:
        return self.pdf_report
    
    def get_prepare_infobox_information(self, question) -> dict:
        infobox_info = {}
        infobox_info[constants.InfoBoxItem.CURRENT_DATATYPE] = self.raw_data[question].dtype
        infobox_info[constants.InfoBoxItem.COUNT_RESPONSES] = self.count_responses(question)
        infobox_info[constants.InfoBoxItem.NO_UNIQUE_RESPONES] = self.count_unique_responses(question)
        return infobox_info
    
    def get_unique_resposes(self, question) -> list:
        column = pd.Series(self.raw_data[question])
        return column.unique()
    
    #endregion
    
    def drop_column(self, column: str) -> None:
        dropped, new_data = cl.drop_columns_by_name(self.raw_data, [column])
        if dropped > 0:
            self.raw_data = new_data
            if column in self.not_categorized_questions:
                self.not_categorized_questions.remove(column)
            else:
                category = self.find_category_by_question(column)
                if category:
                    try:
                        self.categorized_questions[category].remove(column)
                    except ValueError:
                        print('Category not found.')
        return None
    
    def remove_text_in_column(self, question: str, text: str) -> list:
        self.raw_data = cl.remove_text_in_column(self.raw_data, question, text)
        return list(self.raw_data[question])
    
    def questions_categorized(self) -> bool:
        return self.categorized_questions
    
    def count_responses(self, question) -> int:
        column = pd.Series(self.raw_data[question])
        return column.count()
    
    def count_unique_responses(self, question) -> int:
        column = pd.Series(self.raw_data[question])
        return len(column.unique())
    
    def get_columns_with_unique_values_by_threshold(self, threshold: int) -> list:
        unique_responses = tp.extract_possible_answers(self.raw_data)
        columns = []
        for key, value in unique_responses.items():
            if len(value) <= threshold:
                columns.append(key)
        return columns
    
    def update_plot_dimensions(self, column: str, dimension: str) -> None:
        self.chart_logic.update_plot_dimensions(column, dimension)
        return None
    
    def add_question_to_category(self, category: str, question: str) -> None:
        if category not in self.categorized_questions:
            self.categorized_questions[category] = [question]
            self.not_categorized_questions.remove(question)
        else:
            self.categorized_questions[category].append(question)
            self.not_categorized_questions.remove(question)
        return None
    
    def remove_question_from_category(self, category: str, question: str) -> None:
        if category in self.categorized_questions:
            try:
                self.categorized_questions[category].remove(question)
                self.not_categorized_questions.insert(0, question)
            except ValueError:
                print('Category not found!')
        return None
    
    def find_category_by_question(self, question: str) -> str | None:
        for category, items in self.categorized_questions.items():
            if question in items:
                return category
        return None
    
    def add_new_category(self, category: str) -> None:
        if category not in self.categorized_questions:
            self.categorized_questions[category] = []
        return None
    
    def create_chart(self, chart_type: str, report_image: bool) -> Figure:
        match chart_type:
            case 'line':
                return self.chart_logic.create_simple_line_chart(self.raw_data, report_image)
            case 'bar':
                return self.chart_logic.create_simple_bar_chart(self.raw_data, report_image)
            case 'pie':
                return self.chart_logic.create_simple_pie_chart(self.raw_data, report_image)
            case 'scatterplot':
                return self.chart_logic.create_sns_scatterplot_chart(self.raw_data, report_image)
            case 'catplot':
                return self.chart_logic.create_catplot_chart(self.raw_data, report_image)
            case 'countplot':
                return self.chart_logic.create_countplot_chart(self.raw_data, report_image)
    
    def switch_axes(self) -> Figure:
        return self.chart_logic.switch_axes_simple_bar_chart()

    
    def add_item_to_report_items_list(self, short_description: str,  item: ReportItem) -> bool:
        if short_description in self.report_items:
            return False
        self.report_items[short_description] = item
        self.next_report_item_number += 1
        return True
    
    def create_new_pdf_report(self, survey_title: str) -> None:
        self.pdf_report = PDFReport(survey_title)
        return None