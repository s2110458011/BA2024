from backend.survey_library import SurveyLibrary
from frontend.main_window import MainWindow

class Controller:
    def __init__(self) -> None:
        self.model = SurveyLibrary()
        self.view = MainWindow(controller=self, title='AutoGraph', size=(1000,600))
    
    def run(self) -> None:
        self.view.mainloop()
    
    def add_survey_to_library(self, survey):
        survey_name = '1'
        self.model.add_survey(survey_name, survey)