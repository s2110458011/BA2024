import tkinter as tk
import customtkinter as ctk

from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller
    

class CreateChart(ctk.CTkToplevel):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.controller = controller
        self.geometry('800x500')
        self.title('Create New Charts')
        self.category1_list = self.controller.get_categories()
        self.category2_list = self.controller.get_categories()
        self.cat1_questions = []
        self.cat2_questions = []
        
        self.create_main_layout()
        
        return None
    
    #region Layout
    
    def create_main_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.data_frame = ctk.CTkFrame(self, corner_radius=0)
        self.data_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.create_data_options_section_widgets()
        self.create_data_options_section_layout()
        return None
    
    def create_data_options_section_widgets(self) -> None:
        self.cb_same_category = ctk.CTkCheckBox(self.data_frame, text='Same categories')
        self.dp_category1 = ctk.CTkComboBox(self.data_frame, width=200, values=self.category1_list, command=self.update_category1_question_list)
        self.dp_category1.set(value='Choose Category 1')
        self.dp_cat1_questions = ctk.CTkComboBox(self.data_frame, values=self.cat1_questions)
        #self.cat1_questions_frame = ctk.CTkFrame(self.data_frame, corner_radius=0, fg_color='#1E1E1D')
        #self.cat1_questions_listbox = tk.Listbox(self.cat1_questions_frame, borderwidth=0)
        #self.cat1_questions_listbox.bind('<<ListboxSelect>>', self.cat1_question_select)
        
        self.dp_category2 = ctk.CTkComboBox(self.data_frame, values=self.category2_list, command=self.update_category2_question_list)
        self.dp_category2.set(value='Choose Category 2')
        self.dp_cat2_questions = ctk.CTkComboBox(self.data_frame, values=self.cat2_questions)
        #self.cat2_questions_frame = ctk.CTkFrame(self.data_frame, corner_radius=0, fg_color='#1E1E1D')
        #self.cat2_questions_listbox = tk.Listbox(self.cat2_questions_frame, borderwidth=0)
        #self.cat2_questions_listbox.bind('<<ListboxSelect>>', self.cat2_question_select)
        
        return None
    
    def create_data_options_section_layout(self) -> None:
        self.cb_same_category.grid(row=0, column=0, pady=5)
        self.dp_category1.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.dp_cat1_questions.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        #self.cat1_questions_frame.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        #self.cat1_questions_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.dp_category2.grid(row=3, column=0, padx=5, pady=(10,5), sticky='nsew')
        self.dp_cat2_questions.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        #self.cat2_questions_frame.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        #self.cat2_questions_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        return None
    
    def create_chart_settings_widgets(self) -> None:
        
        return None
    
    def create_chart_settings_layout(self) -> None:
        
        return None
    
    #endregion
    
    #region Button commands
    
    
    #endregion
    
    #region Update methods
    
    def update_category1_question_list(self, category: str) -> None:
        self.cat1_questions_listbox.delete(0, 'end')
        questions = self.controller.get_questions_by_category(category)
        for idx, question in enumerate(questions):
            self.cat1_questions_listbox.insert(idx, question)
        return None
    
    def update_category2_question_list(self, category: str) -> None:
        self.cat2_questions_listbox.delete(0, 'end')
        questions = self.controller.get_questions_by_category(category)
        for idx, question in enumerate(questions):
            self.cat2_questions_listbox.insert(idx, question)
        return None
    
    def cat1_question_select(self, e) -> None:
        selected_question = self.get_selected_question(self.cat1_questions_listbox)
        return None
    
    def cat2_question_select(self, e) -> None:
        selected_question = self.get_selected_question(self.cat2_questions_listbox)
        return None
    
    #endregion
    
    #region utils
    
    def get_selected_question(self, listbox: tk.Listbox) -> str | None:
        selected_idx = listbox.curselection()
        if selected_idx:
            return listbox.get(selected_idx)
        return None
    
    #endregion