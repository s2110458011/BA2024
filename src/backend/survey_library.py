from backend.analysis.survey import *

class SurveyLibrary:
    def __init__(self) -> None:
        self.surveys  = {}
    
    def add_survey(self, name: str, survey: Survey) -> None:
        self.surveys[name] = survey
    
    def get_survey(self, name: str) -> Survey:
        return self.surveys[name]
    
    def get_number_entries(self) -> int:
        return len(self.surveys)