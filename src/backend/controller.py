import uuid
import pandas as pd
import backend.analysis.chart_logic as lgc
import backend.data_processor.toolparser as tp
import backend.constants as constants
from matplotlib.figure import Figure
from backend.model.survey_library import SurveyLibrary
from frontend.main_window import MainWindow
from backend.model.survey import Survey
from backend.model.report_item_model import ReportItem
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_report import Report

from PIL import Image, ImageTk

""" from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.modules.page_prepare import Prepare """

class Controller:
    def __init__(self) -> None:
        self.model = SurveyLibrary()
        self.view = MainWindow(controller=self, title='AutoGraph', size=(1000,600))
        return None
        
    
    def run(self) -> None:
        self.view.mainloop()
        return None
    
    def add_survey_to_library(self, survey_name: str, data: pd.DataFrame) -> str:
        id = str(uuid.uuid4())
        survey = Survey(id, survey_name, data)
        self.model.add_survey(id, survey)
        return id
    
    def get_survey_id(self, survey_name: str) -> str:
        return self.model.get_survey_id_by_name(survey_name)
    
    def get_survey_data_raw(self, id: int) -> pd.DataFrame:
        return self.model.get_survey(id).get_data()
    
    def load_data_from_file(self, path) -> pd.DataFrame:
        return tp.load_data_from_csv(path)
    
    def set_current_survey_selection(self, id: str) -> None:
        self.model.set_current_selection(id)
        self.update_category_list()
        return None
    
    def check_survey_selected(self) -> bool:
        current_survey = self.model.current_selected_survey
        if current_survey is not None:
            return True
        else:
            return False
    
    def get_selected_survey(self) -> Survey:
        current_id = self.model.get_current_survey_selection()
        if current_id is not None:
            return self.model.get_survey(current_id)
        else:
            return None
    
    # region Prepare
    def add_question_to_category(self, category: str, question: str) -> None:
        survey = self.get_selected_survey()
        survey.add_question_to_category(category, question)
        return None
    
    def remove_question_from_category(self, category: str, question: str) -> None:
        survey = self.get_selected_survey()
        survey.remove_question_from_category(category, question)
        return None
        
    def get_questions_to_categorize(self) -> list:
        survey = self.get_selected_survey()
        questions = survey.get_uncategorized_questions()
        return questions
    
    def get_categorized_questions(self) -> dict:
        survey = self.get_selected_survey()
        return survey.categorized_questions
    
    def save_not_categorized_questions(self, free_questions: list) -> None:
        survey = self.get_selected_survey()
        survey.set_uncategorized_questions(free_questions)
        return None
    
    def add_new_category(self, category: str) -> None:
        survey = self.get_selected_survey()
        survey.add_new_category(category)
        view = self.view.get_page(Analyze)
        view.update_categories_list()
        return None
        
    def get_survey_list(self) -> list:
        return self.model.get_survey_list()
    
    def check_categorized_questions_empty(self) -> bool:
        survey = self.get_selected_survey()
        if survey.categorized_questions:
            return False
        else:
            return True
    
    def update_survey_list(self) -> None:
        view = self.view.get_page(Prepare)
        view.update_survey_list()
        return None
    
    def activate_categorize_button(self) -> None:
        view = self.view.get_page(Prepare)
        view.activate_categorize_button()
        return None
    
    def set_cb_survey_list_to_selected_survey(self) -> None:
        view = self.view.get_page(Prepare)
        view.set_combobox_selected_value()
        return None
    
    def get_responses_to_question(self, question) -> list:
        survey = self.get_selected_survey()
        return survey.get_responses_to_question(question)
    
    def set_datatype_by_question(self, question: str, datatype: str) -> None:
        survey = self.get_selected_survey()
        survey.set_datatype_by_question(question, datatype)
        return None
    
    # endregion
    
    # region AnalysisController
    def get_questions_by_category(self, category: str) -> list:
        survey = self.get_selected_survey()
        if category == 'All':
            return tp.extract_features(survey.get_data())
        else:
            category_dict = survey.categorized_questions
            return category_dict[category]
    
    def get_categories(self) -> list:
        survey = self.get_selected_survey()
        if survey:
            if survey.questions_categorized():
                category_dict = survey.categorized_questions
                categories = ['All'] + list(category_dict.keys())
            else:
                categories = ['All']
        else:
            categories = []
        return categories
    
    def update_category_list(self) ->  None:
        view = self.view.get_page(Analyze)
        view.update_categories_list()
        return None
    
    def get_chart_options_by_question(self, question: str) -> list:
        survey = self.get_selected_survey()
        return survey.get_chart_options_by_question(question)
    
    def get_figure(self, chart_type: str, report_image: bool) -> Figure:
        survey = self.get_selected_survey()
        return survey.create_chart(chart_type, report_image)
    
    def get_image(self) -> Image:
        survey = self.get_selected_survey()
        image = survey.chart_logic.get_image()
        return image
    
    def get_tk_image(self, label_height, label_width) -> ImageTk:
        survey = self.get_selected_survey()
        image = survey.chart_logic.get_image()
        resized_image = image.resize((label_width, label_height))
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image
    
    def switch_axes(self) -> Figure:
        survey = self.get_selected_survey()
        return survey.switch_axes()
    
    def set_current_simple_chart_question(self, question) -> None:
        survey = self.get_selected_survey()
        survey.set_current_chart_question(question)
        return None
    
    def add_item_to_report(self, image: Image, short_description:str, description: str) -> bool:
        survey = self.get_selected_survey()
        item_no = survey.get_next_report_item_number()
        if description == constants.DESCRIPTION:
            description = ''
        new_item = ReportItem(item_no, image, short_description, description)
        if not survey.add_item_to_report_items_list(short_description, new_item):
            return False
        return True
    
    def set_navigation_button_state(self, button_name: str, state: str) -> None:
        navigation = self.view.get_navigation()
        match button_name:
            case 'Save':
                navigation.set_save_button_state(state)
        return None
            
    
    # endregion
    
    # region Report
    
    def update_report_item_listbox(self) -> None:
        survey = self.get_selected_survey()
        report_item_list = survey.get_report_items_list()
        view = self.view.get_page(Report)
        view.update_report_items_list(report_item_list)
        return None
    
    def create_new_report(self, report_title: str) -> None:
        survey = self.get_selected_survey()
        survey.create_new_pdf_report(report_title)
        return None
    
    def update_report_title(self, new_title: str) -> bool | None:
        survey = self.get_selected_survey()
        report = survey.get_pdf_report()
        if report:
            report.update_title(new_title)
            return True
        return None
    
    def update_final_report_items_list(self, item: str, type: str) -> None:
        survey = self.get_selected_survey()
        report = survey.get_pdf_report()
        if type == constants.ItemType.HEADING:
            report.add_report_item(item)
        elif type == constants.ItemType.PLOT:
            plot = survey.get_report_item(item)
            report.add_report_item(plot)
        return None
    
    # endregion
    
    #region Save
    
    def valid_to_save(self) -> bool:
        view = self.view.get_page(Analyze)
        figure = view.get_current_figure()
        if figure:
            return True
        else:
            return False
    
    def get_current_chart_to_save(self, include_text: bool) -> Figure:
        view = self.view.get_page(Analyze)
        figure = view.get_current_figure()
        if include_text:
            description = view.get_description_text()
            ax = figure.axes[0]
            ax.text(-0.05, -0.05, description, ha='left', va='top', fontsize=10, transform=ax.transAxes)
            figure.tight_layout()
            figure.subplots_adjust(bottom=0.2)
        return figure
    
    def save_chart_to_image(self, file_path: str, include_description: bool) -> None:
        if include_description:
            figure = self.get_current_chart_to_save(True)
        else:
            figure = self.get_current_chart_to_save(False)
        figure.savefig(file_path)
        return None
    
    def save_report_to_pdf(self, file_path: str) -> None:
        report = self.get_selected_survey().get_pdf_report()
        report.print_report_as_pdf(file_path)
        return None
        
    
    #endregion