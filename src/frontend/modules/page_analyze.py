import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller

class Analyze(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        self.categories_list = self.controller.get_categories()
        self.charts_list = []
        
        self.create_widgets()
        self.create_main_layout()
        
        return None
    
    def create_widgets(self) -> None:
        # Main setup
        self.settings_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.display_frame = ctk.CTkFrame(self, corner_radius=0)
        self.chart_canvas = ctk.CTkCanvas(self.display_frame)
        self.text_entry = ctk.CTkTextbox(self.display_frame, corner_radius=0)
        self.text_entry.insert('0.0', 'Enter chart description here...')
        self.text_entry.bind('<FocusIn>', command=self.on_entry_click)
        
        self.create_settings_widget()
        self.create_settings_layout()
        
        return None
    
    def create_settings_widget(self) -> None:
        self.dropdown_categories = ctk.CTkComboBox(self.settings_frame, width=280, values=self.categories_list, command=self.get_questions_by_category)
        self.dropdown_categories.set('Choose Category')
        self.listbox_questions_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, bg_color='gray20')
        self.listbox_questions = tk.Listbox(self.listbox_questions_frame, background='gray20', borderwidth=0)
        
        self.dropdown_charts = ctk.CTkComboBox(self.settings_frame, width=280, values=self.charts_list)
        self.dropdown_charts.set('Choose Chart')
        
        self.button_create_chart = ctk.CTkButton(self.settings_frame, text='Create Chart')
        self.button_add_to_report = ctk.CTkButton(self.settings_frame, text='Add to Report')
        
        return None
    
    def create_settings_layout(self) -> None:
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.dropdown_categories.grid(row=0, column=0, padx=10, pady=10)
        self.listbox_questions_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.listbox_questions_frame.grid_columnconfigure(0, weight=1)
        self.listbox_questions.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.dropdown_charts.grid(row=2, column=0, padx=10, pady=10)
        self.button_create_chart.grid(row=3, column=0, padx=10, pady=10)
        self.button_add_to_report.grid(row=4, column=0, padx=10, pady=10)
        
        return None
    
    def create_main_layout(self) -> None:
        self.settings_frame.grid(row=0, column=0, sticky='ns', padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        
        self.display_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)
        self.chart_canvas.grid(row=0, column=0, sticky='nsew', pady=(0,10))
        self.text_entry.grid(row=1, column=0, sticky='ew')
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        return None
    
    def on_entry_click(self, e) -> None:
        self.text_entry.delete('0.0', 'end')
        return None
    
    def get_questions_by_category(self, category) -> None:
        self.listbox_questions.delete(0, 'end')
        questions = self.controller.get_questions_by_category(category)
        for idx, question in enumerate(questions):
            self.listbox_questions.insert(idx, question)
        return None
    
    def update_categories_list(self) -> None:
        self.categories_list = self.controller.get_categories()
        self.dropdown_categories.configure(values=self.categories_list)
        return None