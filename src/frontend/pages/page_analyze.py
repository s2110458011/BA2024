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
        self.canvas = FigureCanvasTkAgg()
        self.fig = None
        
        self.create_widgets()
        self.create_main_layout()
        
        return None
    
    #region Layout
    
    def create_widgets(self) -> None:
        # Main setup
        self.settings_frame = ctk.CTkScrollableFrame(self, width=300, corner_radius=0)
        self.display_frame = ctk.CTkFrame(self, corner_radius=0)
        #self.chart_canvas_label = ctk.CTkLabel(self.display_frame, text='', corner_radius=0)
        #self.chart_canvas_label.bind('<Configure>', self.resize_image)
        self.text_entry_description = ctk.CTkTextbox(self.display_frame, corner_radius=0, text_color='gray')
        self.placeholder_text = 'Enter chart description here...'
        self.text_entry_description.insert('0.0', self.placeholder_text)
        self.text_entry_description.bind('<FocusIn>', command=self.focus_in)
        self.text_entry_description.bind('<FocusOut>', command=self.focus_out)
        
        self.create_settings_widget()
        self.create_settings_layout()
        
        return None
    
    def create_main_layout(self) -> None:
        self.settings_frame.grid(row=0, column=0, sticky='ns', padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        
        self.display_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        #self.chart_canvas_label.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(1, weight=1)
        self.text_entry_description.grid(row=1, column=0, sticky='ew')
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        return None
    
    def create_settings_widget(self) -> None:
        self.dropdown_categories = ctk.CTkComboBox(self.settings_frame, width=280, values=self.categories_list, command=self.get_questions_by_category)
        self.dropdown_categories.set('Choose Category')
        self.listbox_questions_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, bg_color='gray20')
        self.listbox_questions = tk.Listbox(self.listbox_questions_frame, selectmode='browse', background='gray20', borderwidth=0)
        self.listbox_questions.bind('<<ListboxSelect>>', self.on_click_question_list)
        
        self.dropdown_charts = ctk.CTkComboBox(self.settings_frame, width=280, values=self.charts_list, command=self.action_create_chart)
        self.dropdown_charts.set('Choose Chart')
        self.chart_settings_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color='transparent')
        self.text_entry_title = ctk.CTkEntry(self.chart_settings_frame, placeholder_text='Enter chart title')
        self.font_title = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.text_entry_xlable = ctk.CTkEntry(self.chart_settings_frame, placeholder_text='Enter x label')
        self.font_xlable = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.text_entry_ylable = ctk.CTkEntry(self.chart_settings_frame, placeholder_text='Enter y label')
        self.font_ylable = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.button_update_chart = ctk.CTkButton(self.chart_settings_frame, text='Update', command=self.action_update_chart_labels_font)
        self.button_switch_axes = ctk.CTkButton(self.chart_settings_frame, text='Switch axes', command=self.action_switch_axes)
        
        self.text_entry_short_description = ctk.CTkEntry(self.settings_frame, placeholder_text='Short description')
        self.button_create_chart = ctk.CTkButton(self.settings_frame, text='Create Chart', command=self.action_create_chart_button)
        self.button_add_to_report = ctk.CTkButton(self.settings_frame, text='Add to Report', command=self.action_add_to_report_item_list)
        
        return None
    
    def create_settings_layout(self) -> None:
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.dropdown_categories.grid(row=0, column=0, padx=10, pady=10)
        self.listbox_questions_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.listbox_questions_frame.grid_columnconfigure(0, weight=1)
        self.listbox_questions.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.dropdown_charts.grid(row=2, column=0, padx=10, pady=10)
        self.chart_settings_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        
        self.chart_settings_frame.grid_columnconfigure(1, weight=1)
        self.text_entry_title.grid(row=0, column=0, padx=(0,10), pady=5)
        self.font_title.grid(row=0, column=1, padx=10, pady=5)
        self.text_entry_xlable.grid(row=1, column=0, padx=(0,10), pady=5)
        self.font_xlable.grid(row=1, column=1, padx=10, pady=5)
        self.text_entry_ylable.grid(row=2, column=0, padx=(0,10), pady=5)
        self.font_ylable.grid(row=2, column=1, padx=10, pady=5)
        self.button_update_chart.grid(row=3, column=0, pady=10)
        self.button_switch_axes.grid(row=3, column=1, padx=10, pady=10)
        
        self.text_entry_short_description.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        self.button_add_to_report.grid(row=5, column=0, padx=10, pady=10)
        self.button_create_chart.grid(row=6, column=0, padx=10, pady=10)
        
        
        return None
    
    #endregion
    
    #region Eventbindings
    
    def resize_image(self, e) -> None:
        label_width = e.width
        label_height = e.height
        image = self.controller.get_tk_image(label_height, label_width)
        self.chart_canvas_label.configure(image=image)
        return None
        
    
    def focus_in(self, e) -> None:
        text = self.text_entry_description.get('1.0', 'end-1c')
        if text == self.placeholder_text:
            self.text_entry_description.delete('0.0', 'end-1c')
            self.text_entry_description.configure(text_color=['gray10', '#DCE4EE'])
        return None
    
    def focus_out(self, e) -> None:
        if not self.text_entry_description.get('1.0', 'end-1c'):
            self.text_entry_description.configure(text_color='gray')
            self.text_entry_description.insert('0.0', self.placeholder_text)
        return None
    
    def on_click_question_list(self, e) -> None:
        #self.dropdown_charts.set('Choose Chart')
        current_selection = self.get_selected_question()
        if current_selection:
            self.selected_question = current_selection
        self.controller.set_current_simple_chart_question(self.selected_question)
        chart_type = self.dropdown_charts.get()
        self.update_chart_options_list(self.selected_question)
        if chart_type not in self.charts_list:
            self.dropdown_charts.set('Choose Chart')
        else:
            self.action_create_chart(chart_type)
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
        self.charts_list = self.controller.get_chart_options_by_question(question)
        self.dropdown_charts.configure(values=self.charts_list)
        return None
    
    def display_chart(self) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, self.display_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw()
        return None
    
    #endregion
    
    #region Utils
    
    def get_selected_question(self) -> str | None:
        selected_idx = self.listbox_questions.curselection()
        if selected_idx:
            return self.listbox_questions.get(selected_idx)
        return None
    
    def set_chart_labels(self, title_size, xlabel_size, ylabel_size, title_str, xlabel_str, ylabel_str) -> None:
        if title_str:
            self.chart_title = title_str
            self.fig.suptitle(title_str)
        if title_size:
            size = int(title_size)
            self.fig.suptitle(self.chart_title, fontsize=size)
        if xlabel_str:
            self.chart_xlabel = xlabel_str
            ax = self.fig.axes[0]
            ax.set_xlabel(xlabel_str)
        if xlabel_size:
            size = int(xlabel_size)
            ax = self.fig.axes[0]
            ax.set_xlabel(self.chart_xlabel, fontsize=size)
        if ylabel_str:
            self.chart_ylabel = ylabel_str
            ax = self.fig.axes[0]
            ax.set_ylabel(ylabel_str)
        if ylabel_size:
            size = int(ylabel_size)
            ax = self.fig.axes[0]
            ax.set_ylabel(self.chart_ylabel, fontsize=size)
        return None
    
    def get_current_figure(self) -> Figure:
        return self.fig
    
    def get_description_text(self) -> str:
        return self.text_entry_description.get('1.0', 'end')
    
    #endregion
    
    #region Button commands
    
    def action_create_chart_button(self) -> None:
        CreateChart(self.master, self.controller)
        return None
    
    def action_create_chart(self, chart_type) -> None:
        self.fig = None
        self.fig = self.controller.get_figure(chart_type, False)
        self.display_chart()
        return None
    
    def action_update_chart_labels_font(self) -> None:
        font_title_value = self.font_title.get()
        font_xlabel_value = self.font_xlable.get()
        font_ylabel_value = self.font_ylable.get()
        title_str = self.text_entry_title.get()
        if title_str:
            self.text_entry_title.delete(0, 'end')
        xlable_str = self.text_entry_xlable.get()
        if xlable_str:
            self.text_entry_xlable.delete(0, 'end')
        ylable_str = self.text_entry_ylable.get()
        if ylable_str:
            self.text_entry_ylable.delete(0, 'end')
        self.set_chart_labels(font_title_value, font_xlabel_value, font_ylabel_value, title_str, xlable_str, ylable_str)
        self.canvas.draw()
        return None
    
    def action_switch_axes(self) -> None:
        self.fig = self.controller.switch_axes()
        self.display_chart()
        return None
    
    def action_add_to_report_item_list(self) -> None:
        description_text = self.text_entry_description.get('1.0', 'end')
        short_description = self.text_entry_short_description.get()
        self.text_entry_short_description.delete(0, 'end')
        chart_type = self.dropdown_charts.get()
        self.controller.get_figure(chart_type, True)
        img = self.controller.get_image()
        if not short_description:
            tk.messagebox.showerror(title='error', message='A short description must be provided to add the report item.')
        if not self.controller.add_item_to_report(img, short_description, description_text):
            tk.messagebox.showerror(title='error', message='Short description must be unique. This is short description already exists.')
        self.controller.update_report_item_listbox()
        return None
    
    #endregion