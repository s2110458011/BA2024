import customtkinter as ctk
from typing import Type, TYPE_CHECKING

from frontend.windows.window_categorize import Categorize
from frontend.windows.window_datatypes import AssignDatatypes

if TYPE_CHECKING:
    from backend.controller import Controller

class Prepare(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.master = master
        self.controller: Type['Controller'] = controller
        self.cb_surveys_values: list = self.controller.get_survey_list()
        
        self.create_widgets()
        self.create_main_layout()
        self.check_survey_selection()
        return None
    
    #region Layout
    
    def create_widgets(self) -> None:
        self.dropdown_survey_list = ctk.CTkComboBox(self, corner_radius=3, values=self.cb_surveys_values, command=self.select_survey)
        self.dropdown_survey_list.set('Choose survey')
        
        self.create_preprocessing_frame_widgets()
        self.create_categorizing_frame_widgets()
        return None
    
    def create_preprocessing_frame_widgets(self) -> None:
        self.preprocessing_frame = ctk.CTkFrame(self, corner_radius=0)
        self.preprocessing_frame.grid(row=1, column=0, padx=20, pady=(0,5), sticky='nsew')
        
        self.label_preprocessing = ctk.CTkLabel(self.preprocessing_frame, text='Preprocessing Data')
        self.label_preprocessing.grid(row=0, column=0, padx=20)
        
        self.button_set_dtypes = ctk.CTkButton(self.preprocessing_frame, text='Set Datatypes', corner_radius=0, command=self.action_button_datatypes)
        self.button_set_dtypes.grid(row=1, column=0, padx=20, pady=(10,20))
        return None
    
    def create_categorizing_frame_widgets(self) -> None:
        self.categorizing_frame = ctk.CTkFrame(self, corner_radius=0)
        self.categorizing_frame.grid(row=2, column=0, padx=20, pady=5, sticky='nsew')
        
        self.label_categorizing = ctk.CTkLabel(self.categorizing_frame, text='Categorizing Questions')
        self.label_categorizing.grid(row=0, column=0, padx=20)
        
        self.button_categorize = ctk.CTkButton(self.categorizing_frame, text='Categorize', state='disabled', corner_radius=0, command=self.action_button_categorize)
        self.button_categorize.grid(row=1, column=0, padx=20, pady=(10,20))
        return None
    
    def create_main_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.dropdown_survey_list.grid(row=0, column=0, padx=20, pady=20, sticky='w')
        return None
    
    #endregion Layout
    
    #region Action commands
    
    def action_button_categorize(self) -> None:
        Categorize(self.master, self.controller)
        return None
    
    def action_button_datatypes(self) -> None:
        AssignDatatypes(self.master, self.controller)
        return None
    
    #endregion
    
    def update_survey_list(self) -> None:
        """When a new survey is loaded the combobox in 'Prepare' is updated to include the newly loaded survey.

        Returns:
            None: no return value
        """
        self.cb_surveys_values = self.controller.get_survey_list()
        self.dropdown_survey_list.configure(values=self.cb_surveys_values)
        return None
    
    def check_survey_selection(self) -> None:
        if self.controller.check_survey_selected():
            self.button_categorize.configure(state='normal')
        return None
    
    def activate_categorize_button(self) -> None:
        self.button_categorize.configure(state='normal')
        return None
    
    def select_survey(self, survey) -> None:
        #TODO get survey Id, set current selected survey, activate categorize button
        id = self.controller.get_survey_id(survey)
        self.controller.set_current_survey_selection(id)
        self.button_categorize.configure(state='normal')
        return None
    
    def set_combobox_selected_value(self) -> None:
        if self.controller.check_survey_selected():
            survey = self.controller.get_selected_survey()
            self.dropdown_survey_list.set(survey.name)
        else:
            self.dropdown_survey_list.set('Choose survey')
        return None