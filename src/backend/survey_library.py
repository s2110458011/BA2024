from backend.analysis.survey import *

class SurveyLibrary:
    def __init__(self) -> None:
        self.surveys  = {}
        self.current_selected_survey = None
    
    def add_survey(self, id: int, survey: Survey) -> None:
        self.surveys[id] = survey
        return None
    
    def get_survey(self, id: int) -> Survey:
        return self.surveys[id]
    
    def set_current_selection(self, id) -> None:
        self.current_selected_survey = id
        return None
    
    def get_number_entries(self) -> int:
        return len(self.surveys)
    
    def get_current_survey_selection(self) -> str:
        return self.current_selected_survey
    
    def get_survey_list(self) -> list:
        """Iterates through the dictionary of survey and their uuids and returns the attribute name from each survey.

        Returns:
            list: A list of survey names entered by the user when loading the survey.
        """
        survey_names = [survey.name for survey in self.surveys.values()]
        return survey_names
    
    def get_survey_by_name(self, search_name: str) -> str:
        #TODO if name is not found
        for id, name in self.surveys.items():
            if name == search_name:
                return id