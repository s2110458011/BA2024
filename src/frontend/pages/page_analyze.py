import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Type, TYPE_CHECKING

from frontend.windows.window_create_chart import CreateChart

if TYPE_CHECKING:
    from backend.controller import Controller

class Analyze(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.master = master
        self.controller = controller
        self.categories_list = self.controller.get_categories()
        self.charts_list = []
        
        self.create_widgets()
        self.create_main_layout()
        
        return None
    
    #region Layout
    
    def create_widgets(self) -> None:
        # Main setup
        self.settings_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.display_frame = ctk.CTkFrame(self, corner_radius=0)
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
        self.listbox_questions = tk.Listbox(self.listbox_questions_frame, selectmode='browse', background='gray20', borderwidth=0)
        self.listbox_questions.bind('<<ListboxSelect>>', self.on_click_question_list)
        
        self.dropdown_charts = ctk.CTkComboBox(self.settings_frame, width=280, values=self.charts_list, command=self.display_chart)
        self.dropdown_charts.set('Choose Chart')
        
        self.button_create_chart = ctk.CTkButton(self.settings_frame, text='Create Chart', command=self.action_create_chart_button)
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
        self.text_entry.grid(row=1, column=0, sticky='ew')
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        return None
    
    #endregion
    
    #region Eventbindings
    
    def on_entry_click(self, e) -> None:
        self.text_entry.delete('0.0', 'end')
        return None
    
    def on_click_question_list(self, e) -> None:
        self.dropdown_categories.configure(values=['Choose Chart'])
        selected_question = self.get_selected_question()
        self.update_chart_options_list(selected_question)
        return None
    
    #endregion
    
    #region Update methods
    
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
    
    def update_chart_options_list(self, question) -> None:
        chart_options = self.controller.get_chart_options_by_question(question)
        self.dropdown_charts.configure(values=chart_options)
        return None
    
    def display_chart(self, chart_type) -> None:
        question = self.get_selected_question()
        fig = self.controller.get_figure(chart_type, question)
        canvas = FigureCanvasTkAgg(fig, self.display_frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        canvas.draw()
        return None
    
    #endregion
    
    #region Utils
    
    def get_selected_question(self) -> str | None:
        selected_idx = self.listbox_questions.curselection()
        if selected_idx:
            return self.listbox_questions.get(selected_idx)
        return None
    
    #endregion
    
    #region Button commands
    
    def action_create_chart_button(self) -> None:
        CreateChart(self.master, self.controller)
        return None
    
    #endregion