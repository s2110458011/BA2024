import tkinter as tk
import customtkinter as ctk
import backend.constants as constants
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
        self.controller: Type['Controller'] = controller
        self.categories_list: list = self.controller.get_categories()
        self.col_threshold: int = 2
        self.third_question_list: list = self.controller.get_third_questions(self.col_threshold)
        self.questions_list: list = []
        self.selected_question: str = None
        self.charts_list: list = []
        self.chart_finder_matrix: dict[str: bool] = {'x': False, 'y': False, 'hue': False, 'col': False}
        self.canvas = FigureCanvasTkAgg()
        self.fig: Figure = None
        
        self.more_options: bool = False
        self.create_widgets()
        self.create_main_layout()
        
        return None
    
    #region Layout
    
    def create_widgets(self) -> None:
        # Main setup
        self.settings_frame = ctk.CTkScrollableFrame(self, width=300, corner_radius=0)
        self.display_frame = ctk.CTkFrame(self, corner_radius=0)
        self.text_entry_description = ctk.CTkTextbox(self.display_frame, corner_radius=0, text_color='gray')
        self.text_entry_description.insert('0.0', constants.DESCRIPTION)
        self.text_entry_description.bind('<FocusIn>', command=self.focus_in)
        self.text_entry_description.bind('<FocusOut>', command=self.focus_out)
        
        self.create_settings_widget()
        self.create_settings_layout()
        self.create_more_options_widget()
        self.create_more_options_layout()
        
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
        self.yscrollbar_questions = ttk.Scrollbar(self.listbox_questions_frame, orient='vertical', command=self.listbox_questions.yview)
        self.xscrollbar_questions = ttk.Scrollbar(self.listbox_questions_frame, orient='horizontal', command=self.listbox_questions.xview)
        self.listbox_questions.config(yscrollcommand=self.yscrollbar_questions.set, xscrollcommand=self.xscrollbar_questions.set)
        self.listbox_questions.bind('<<ListboxSelect>>', self.on_click_question_list)
        
        self.dropdown_charts = ctk.CTkComboBox(self.settings_frame, width=280, values=self.charts_list, command=self.action_create_chart)
        self.dropdown_charts.set('Choose Chart')
        self.chart_settings_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color='transparent')
        self.text_entry_title = ctk.CTkEntry(self.chart_settings_frame, corner_radius=0, placeholder_text='Enter chart title')
        self.font_title = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.text_entry_xlable = ctk.CTkEntry(self.chart_settings_frame, corner_radius=0, placeholder_text='Enter x label')
        self.font_xlable = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.text_entry_ylable = ctk.CTkEntry(self.chart_settings_frame, corner_radius=0, placeholder_text='Enter y label')
        self.font_ylable = ttk.Spinbox(self.chart_settings_frame, from_=8, to=20, width=5)
        self.button_update_chart = ctk.CTkButton(self.chart_settings_frame, text='Update', corner_radius=0, command=self.action_update_chart_labels_font)
        self.button_switch_axes = ctk.CTkButton(self.chart_settings_frame, text='Switch Axes', corner_radius=0, state='disabled', command=self.action_switch_axes)
        
        self.text_entry_short_description = ctk.CTkEntry(self.settings_frame, corner_radius=0, placeholder_text='Short description')
        self.button_create_chart = ctk.CTkButton(self.settings_frame, text='Create Chart', corner_radius=0, command=self.action_create_chart_button)
        self.button_more_options = ctk.CTkButton(self.settings_frame, text='More Options', corner_radius=0, command=self.action_show_more_options)
        self.button_add_to_report = ctk.CTkButton(self.settings_frame, text='Add to Report', corner_radius=0, command=self.action_add_to_report_item_list)
        
        return None
    
    def create_settings_layout(self) -> None:
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.dropdown_categories.grid(row=0, column=0, padx=10, pady=10)
        self.listbox_questions_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.listbox_questions_frame.grid_columnconfigure(0, weight=1)
        self.listbox_questions.pack(side='left', fill='both', expand=True)
        self.listbox_questions.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.yscrollbar_questions.grid(row=0, column=1, sticky='ns')
        self.xscrollbar_questions.grid(row=1, column=0, sticky='ew')
        
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
        self.button_more_options.grid(row=6, column=0, padx=10, pady=10)
        
        
        return None
    
    def create_more_options_widget(self) -> None:
        self.frame_more_options = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color='transparent')
        self.dropdown_second_category = ctk.CTkComboBox(self.frame_more_options, width=200, values=self.categories_list, command=self.get_questions_second_category)
        self.dropdown_second_category.set('Choose Second Category')
        self.dropdown_second_question = ctk.CTkComboBox(self.frame_more_options, width=200, values=self.questions_list, command=self.set_chart_dimension_second)
        self.dropdown_second_question.set('Choose Second Question')
        self.cb_var_second = tk.IntVar()
        self.cb_second_question = ctk.CTkCheckBox(self.frame_more_options, text='include', state='disabled', corner_radius=0, checkbox_width=16, checkbox_height=16, border_width=2, variable=self.cb_var_second, onvalue=1, offvalue=0, command=self.on_click_cb_second)
        #self.dropdown_third_category = ctk.CTkComboBox(self.frame_more_options, width=200, values=self.categories_list, command=self.get_questions_hue_category)
        #self.dropdown_third_category.set('Choose Third Category')
        self.dropdown_third_question = ctk.CTkComboBox(self.frame_more_options, width=200, values=self.questions_list, command=self.set_chart_dimension_third)
        self.dropdown_third_question.set('Choose Third Question')
        self.cb_var_third = tk.IntVar()
        self.cb_third_question = ctk.CTkCheckBox(self.frame_more_options, text='include', state='disabled', corner_radius=0, checkbox_width=16, checkbox_height=16, border_width=2, variable=self.cb_var_third, onvalue=1, offvalue=0, command=self.on_click_cb_third)
        self.rb_frame = ctk.CTkFrame(self.frame_more_options, corner_radius=0, fg_color='transparent')
        self.rb_var = tk.IntVar()
        self.rb_label = ctk.CTkLabel(self.rb_frame, text='Chart Columns:')
        self.rb_two = ctk.CTkRadioButton(self.rb_frame, text='2', value=2, variable=self.rb_var, command=self.on_click_radiobutton)
        self.rb_three = ctk.CTkRadioButton(self.rb_frame, text='3', value=3, variable=self.rb_var, command=self.on_click_radiobutton)
        self.rb_var.set(2)
        return None
    
    def create_more_options_layout(self) -> None:
        self.dropdown_second_category.grid(row=0, column=0, padx=10, pady=(10,0), sticky='w')
        self.dropdown_second_question.grid(row=1, column=0, padx=10, pady=(5,10), sticky='w')
        self.cb_second_question.grid(row=1, column=1, padx=5, pady=(5,10))
        #self.dropdown_third_category.grid(row=2, column=0, padx=10)
        self.dropdown_third_question.grid(row=3, column=0, padx=10, pady=(5,10))
        self.cb_third_question.grid(row=3, column=1, padx=10, pady=(5,10))  
        self.rb_frame.grid(row=4, column=0, columnspan=2, sticky='nsew')
        self.rb_label.grid(row=0, column=0, padx=10, pady=(5,10), sticky='w')
        self.rb_two.grid(row=0, column=1, padx=5, pady=(5,10))
        self.rb_three.grid(row=0, column=2, padx=5, pady=(5,10))
        return None
    
    
    #endregion
    
    #region Eventbindings
    
    def focus_in(self, e) -> None:
        text = self.text_entry_description.get('1.0', 'end-1c')
        if text == constants.DESCRIPTION:
            self.text_entry_description.delete('0.0', 'end-1c')
            self.text_entry_description.configure(text_color=['gray10', '#DCE4EE'])
        return None
    
    def focus_out(self, e) -> None:
        if not self.text_entry_description.get('1.0', 'end-1c'):
            self.text_entry_description.configure(text_color='gray')
            self.text_entry_description.insert('0.0', constants.DESCRIPTION)
        return None
    
    def on_click_question_list(self, e) -> None:
        current_selection = self.get_selected_question()
        if current_selection:
            self.selected_question = current_selection
            self.controller.update_chart_dimensions(current_selection, 'x')
        hue = self.cb_var_third.get()
        second = self.cb_var_second.get()
        if hue == 1 or second == 1:
            self.update_chart_options_list_advanced(hue, second)
        else:
            self.controller.set_current_simple_chart_question(self.selected_question)
            self.update_chart_options_list_simple(self.selected_question)
        chart_type = self.dropdown_charts.get()
        if chart_type not in self.charts_list:
            self.dropdown_charts.set('Choose Chart')
        else:
            self.action_create_chart(chart_type)
        return None
    
    def on_click_radiobutton(self) -> None:
        self.col_threshold = self.rb_var.get()
        self.controller.update_third_question_list()
        return None
    
    #endregion
    
    #region Update methods
    
    def get_questions_by_category(self, category) -> None:
        self.listbox_questions.delete(0, 'end')
        questions = self.controller.get_questions_by_category(category)
        for idx, question in enumerate(questions):
            self.listbox_questions.insert(idx, question)
        return None
    
    def get_questions_second_category(self, category) -> None:
        questions = self.controller.get_questions_by_category(category)
        self.dropdown_second_question.configure(values=questions)
        self.dropdown_second_question.set('Choose Second Question')
        self.cb_second_question.configure(state='disabled')
        return None
    
    def get_questions_hue_category(self, category) -> None:
        questions = self.controller.get_questions_by_category(category)
        self.dropdown_third_question.configure(values=questions)
        self.dropdown_third_question.set('Choose Color Question')
        self.cb_third_question.configure(state='diabled')
        return None
    
    def update_categories_list(self) -> None:
        self.categories_list = self.controller.get_categories()
        self.dropdown_categories.configure(values=self.categories_list)
        self.dropdown_second_category.configure(values=self.categories_list)
        return None
    
    def update_chart_options_list_simple(self, question) -> None:
        self.charts_list = self.controller.get_chart_options_by_question(question)
        self.dropdown_charts.configure(values=self.charts_list)
        return None
    
    def set_chart_dimension_second(self, question) -> None:
        self.cb_second_question.configure(state='normal')
        self.controller.update_chart_dimensions(question, 'y')
        third = self.cb_var_third.get()
        second = self.cb_var_second.get()
        if second == 1:
            self.update_chart_options_list_advanced(second, third)
        else:
            self.update_chart_options_list_simple(self.selected_question)
        self.dropdown_charts.set('Choose Chart')
        return None
    
    def set_chart_dimension_third(self, question) -> None:
        self.controller.update_chart_dimensions(question, 'z')
        second = self.cb_var_second.get()
        third = self.cb_var_third.get()
        if second == 1:
            self.cb_third_question.configure(state='normal')
            self.update_chart_options_list_advanced(second, third)
        else:
            self.update_chart_options_list_simple(self.selected_question)
        self.dropdown_charts.set('Choose Chart')
        return None
    
    def display_chart(self) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, self.display_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw()
        return None
    
    def update_chart_options_list_advanced(self, second_state: int, third_state: int) -> None:
        # third can only be 1 if second is 1
        if second_state == 0:
            self.update_chart_options_list_simple(self.selected_question)
            self.dropdown_charts.set('Choose Chart')
        elif second_state == 1 and third_state == 0:
            self.dropdown_charts.configure(values=constants.TWO_DIMENSIONS)
        elif second_state == 1 and third_state == 1:
            self.dropdown_charts.configure(values=constants.THREE_DIMENSIONS)
        return None
    
    def update_third_questions_list(self, questions: list) -> None:
        self.dropdown_third_question.configure(values=questions)
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
    
    def empty_analyze(self) -> None:
        self.dropdown_charts.set('Choose Chart')
        self.listbox_questions.delete(0, 'end')
        self.fig = None
        self.img = None
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        if self.more_options:
            self.action_show_more_options()
        return None
    
    #endregion
    
    #region Button commands
    
    def action_create_chart_button(self) -> None:
        CreateChart(self.master, self.controller)
        return None
    
    def action_show_more_options(self) -> None:
        if self.more_options:
            self.frame_more_options.grid_forget()
            self.button_more_options.configure(text='More Options')
            self.more_options = False
        else:
            self.frame_more_options.grid(row=7, column=0)
            self.button_more_options.configure(text='Less Options')
            self.more_options = True
        return None
    
    def action_create_chart(self, chart_type) -> None:
        self.fig = None
        if chart_type == 'bar':
            self.button_switch_axes.configure(state='normal')
        else:
            self.button_switch_axes.configure(state='disabled')
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
    
    def on_click_cb_second(self) -> None:
        if self.selected_question:
            second_state = self.cb_second_question.get()
            third_state= self.cb_third_question.get()
            if second_state == 1:
                self.update_chart_options_list_advanced(second_state, third_state)
                self.dropdown_charts.set('Choose Chart')
                if self.dropdown_third_question.get() == 'Choose Third Question':
                    self.cb_third_question.configure(state='disabled')
                else:
                    self.cb_third_question.configure(state='normal')
            else:
                self.update_chart_options_list_simple(self.selected_question)
                self.dropdown_charts.set('Choose Chart')
                self.cb_third_question.configure(state='disabled')
        else:
            self.cb_var_second.set(0)
            tk.messagebox.showerror(title='error', message='Please select a question from the list above first.')
        return None
    
    def on_click_cb_third(self) -> None:
        third_state= self.cb_third_question.get()
        second_state = self.cb_second_question.get()
        self.update_chart_options_list_advanced(second_state, third_state)
        return None
    
    #endregion