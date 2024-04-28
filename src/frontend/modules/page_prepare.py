import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from typing import Type, TYPE_CHECKING

from frontend.modules.window_categorize import Categorize

if TYPE_CHECKING:
    from backend.controller import Controller

class Prepare(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.master = master
        self.controller = controller
        self.cb_surveys_values = self.controller.get_survey_list()
        
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self) -> None:
        self.dropdown_survey_list = ctk.CTkComboBox(self, values=self.cb_surveys_values)
        self.dropdown_survey_list.set('Choose survey')
        self.button_categorize = ctk.CTkButton(self, text='Categorize', command=self.action_button_categorize)
        #self.listbox_questions = tk.Listbox(self)
        
        return None
    
    def create_layout(self) -> None:
        self.dropdown_survey_list.grid(row=0, column=0, padx=20, pady=20)
        self.button_categorize.grid(row=1, column=0, padx=20, pady=20)
        #self.listbox_questions.grid(row=0, column=0, padx=20, pady=20)
        return None
    
    def action_button_categorize(self):
        categorize_window = Categorize(self.master, self.controller)
    
    def update_survey_list(self) -> None:
        """When a new survey is loaded the combobox in 'Prepare' is updated to include the newly loaded survey.

        Returns:
            None: no return value
        """
        self.cb_surveys_values = self.controller.get_survey_list()
        self.dropdown_survey_list.configure(values=self.cb_surveys_values)
        return None