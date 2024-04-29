import pandas as pd
import uuid
from backend.model.survey_library import SurveyLibrary
from frontend.main_window import MainWindow
from backend.data_processor.toolparser import *
from backend.model.survey import Survey
from frontend.modules.page_prepare import Prepare
from frontend.modules.page_analyze import Analyze

""" from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.modules.page_prepare import Prepare """

class Controller:
    def __init__(self) -> None:
        self.model = SurveyLibrary()
        self.view = MainWindow(controller=self, title='AutoGraph', size=(1000,600))
    
    def run(self) -> None:
        self.view.mainloop()
    
    def exit(self) -> None:
        self.view.destroy()
    
    def add_survey_to_library(self, survey_name: str, data: pd.DataFrame):
        id = str(uuid.uuid4())
        survey = Survey(id, survey_name, data)
        self.model.add_survey(id, survey)
        return id
    
    def get_survey_id(self, survey_name: str) -> str:
        return self.model.get_survey_id_by_name(survey_name)
    
    def get_survey_data_raw(self, id: int) -> pd.DataFrame:
        return self.model.get_survey(id).get_data()
    
    def load_data_from_file(self, path):
        return load_data_from_csv(path)
    
    def set_current_survey_selection(self, id: str) -> None:
        self.model.set_current_selection(id)
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
    def add_question_to_category(self, category, question):
        survey = self.get_selected_survey()
        survey.add_question_to_category(category, question)
        
    def get_questions_to_categorize(self):
        survey = self.get_selected_survey()
        if survey.not_categorized_questions is None:
            questions = extract_features(survey.get_data())
        else:
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
    
    # endregion
    
    # region AnalysisController
    def get_questions_by_category(self, category: str) -> list:
        survey = self.get_selected_survey()
        category_dict = survey.categorized_questions
        return category_dict[category]
    
    def get_categories(self) -> list:
        survey = self.get_selected_survey()
        if survey:
            category_dict = survey.categorized_questions
            categories = list(category_dict.keys())
        else:
            categories = []
        return categories
    
    def update_category_list(self) ->  None:
        view = self.view.get_page(Analyze)
        view.update_categories_list()
        return None
    
    # endregion
    
    # region Report
    
    
    # endregion