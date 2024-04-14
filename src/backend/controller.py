from backend.survey_library import SurveyLibrary
from frontend.main_window import MainWindow

class Controller:
    def __init__(self) -> None:
        self.model = SurveyLibrary()
        self.view = MainWindow(controller=self, title='AutoGraph', size=(1000,600))
    
    def run(self) -> None:
        self.view.mainloop()
    
    def add_survey_to_library(self, name, survey) -> None:
        self.model.add_survey(name, survey)
    
    def get_id(self) -> int:
        return self.model.get_number_entries()