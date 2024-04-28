import pandas as pd
import uuid
from backend.survey_library import SurveyLibrary
from frontend.main_window import MainWindow
from backend.data_processor.toolparser import *
from backend.analysis.survey import Survey
from frontend.modules.page_prepare import Prepare

from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.modules.page_prepare import Prepare

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
    
    def get_id(self) -> int:
        return self.model.get_number_entries()
    
    def get_survey_data_raw(self, id: int) -> pd.DataFrame:
        return self.model.get_survey(id).get_data()
    
    def load_data_from_file(self, path):
        return load_data_from_csv(path)
    
    def set_current_survey_selection(self, id: str) -> None:
        self.model.set_current_selection(id)
        return None
    
    def add_question_to_category(self, category, question):
        self.model.get_survey()
        
    def get_questions(self):
        current_id = self.model.get_current_survey_selection()
        survey = self.model.get_survey(current_id)
        questions = extract_features(survey.get_data())
        return questions
    
    def add_new_category(self, category: str) -> None:
        current_id = self.model.get_current_survey_selection()
        survey = self.model.get_survey(current_id)
        survey.add_new_category(category)
        return None
        
    def get_survey_list(self) -> list:
        return self.model.get_survey_list()
    
    def update_survey_list(self) -> list:
        view = self.view.get_page(Prepare)
        view.update_survey_list()