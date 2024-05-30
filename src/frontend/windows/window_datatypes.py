import tkinter as tk
import customtkinter as ctk
import backend.constants as constants

from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller

class AssignDatatypes(ctk.CTkToplevel):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.controller: Type['Controller'] = controller
        self.geometry('800x500')
        self.title('Prepare Data')
        self.datatypes_list = constants.DATATYPE_LIST
        
        self.create_main_widgets()
        self.create_main_layout()
        self.fill_questions()
        
        return None
    
    #region Layout
    
    def create_main_widgets(self) -> None:
        # left frame
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.label_questions = ctk.CTkLabel(self.left_frame, text='Questions')
        self.create_questions_list_widget()
        self.label_values = ctk.CTkLabel(self.left_frame, text='Responses')
        self.create_values_list_widget()
        self.infobox = ctk.CTkFrame(self.left_frame, corner_radius=0)
        self.label_infobox = ctk.CTkLabel(self.infobox, text='Infobox', width=300)
        self.label_infobox.cget('font').configure(underline=True)
        self.label_dtype = ctk.CTkLabel(self.infobox, text='Current datatype:')
        self.label_dtype_value = ctk.CTkLabel(self.infobox, text='')
        self.label_no_responses = ctk.CTkLabel(self.infobox, text='Number of repones:')
        self.label_no_responses_value = ctk.CTkLabel(self.infobox, text='')
        self.label_no_unique_responses = ctk.CTkLabel(self.infobox, text='Number of unique responses:')
        self.label_no_unique_responses_value = ctk.CTkLabel(self.infobox, text='')
        
        # rigth frame
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.dropdown_datatypes = ctk.CTkComboBox(self.right_frame, corner_radius=0, values=self.datatypes_list)
        self.dropdown_datatypes.set('Choose datatype')
        self.button_apply = ctk.CTkButton(self.right_frame, text='Apply', corner_radius=0, command=self.action_button_apply)
        self.button_drop_column = ctk.CTkButton(self.right_frame, text='Drop Column', corner_radius=0, command=self.action_drop_column)
        self.button_show_unique = ctk.CTkButton(self.right_frame, text='Unique Responses', corner_radius=0, command=self.action_show_unique)
        self.entry_remove = ctk.CTkEntry(self.right_frame, placeholder_text='Text to remove', corner_radius=0)
        self.button_remove = ctk.CTkButton(self.right_frame, text='Remove', corner_radius=0, command=self.action_remove_text)
        self.button_close = ctk.CTkButton(self.right_frame, text='Close', corner_radius=0, command=self.action_close)
        
        return None
    
    def create_main_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        
        # left frame
        self.left_frame.grid_columnconfigure(0, weight=3)
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid(row=0, column=0, sticky='nsew')
        self.label_questions.grid(row=0, column=0, padx=20, pady=(20,0), sticky='w')
        self.label_values.grid(row=0, column=1, padx=10, pady=(20,0), sticky='w')
        self.infobox.grid(row=2, column=0, padx=(20,10), pady=(0,10), sticky='ew')
        self.infobox.grid_columnconfigure(1, weight=1)
        self.label_infobox.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        self.label_dtype.grid(row=1, column=0, padx=10, pady=0, sticky='w')
        self.label_dtype_value.grid(row=1, column=1, padx=10, pady=0, sticky='w')
        self.label_no_responses.grid(row=2, column=0, padx=10, pady=0, sticky='w')
        self.label_no_responses_value.grid(row=2, column=1, padx=10, pady=0, sticky='w')
        self.label_no_unique_responses.grid(row=3, column=0, padx=10, pady=0, sticky='w')
        self.label_no_unique_responses_value.grid(row=3, column=1, padx=10, pady=0, sticky='w')
        
        
        # right frame
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.dropdown_datatypes.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.button_apply.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.button_drop_column.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.button_show_unique.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.entry_remove.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.button_remove.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.button_close.grid(row=6, column=0, padx=10, pady=10, sticky='w')
        
        return None
    
    def create_questions_list_widget(self) -> None:
        frame_listbox_questions = ctk.CTkFrame(self.left_frame, corner_radius=0, fg_color='gray20')
        frame_listbox_questions.grid_columnconfigure(0, weight=1)
        frame_listbox_questions.grid_rowconfigure(0, weight=1)
        self.listbox_questions = tk.Listbox(frame_listbox_questions, background='gray20', border=None, borderwidth=0)
        scroll_Y = ttk.Scrollbar(frame_listbox_questions, orient='vertical', command=self.listbox_questions.yview)
        scroll_X = ttk.Scrollbar(frame_listbox_questions, orient='horizontal', command=self.listbox_questions.xview)
        self.listbox_questions.config(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        self.listbox_questions.bind('<ButtonRelease-1>', self.on_item_click)
        
        # Layout
        frame_listbox_questions.grid(row=1, column=0, sticky='nsew', pady=(0,20), padx=(20,10))
        self.listbox_questions.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        scroll_Y.grid(row=0, column=1, sticky='ns')
        scroll_X.grid(row=1, column=0, sticky='ew')
        return None
    
    def create_values_list_widget(self) -> None:
        frame_listbox_values = ctk.CTkFrame(self.left_frame, corner_radius=0, fg_color='gray20')
        frame_listbox_values.grid_columnconfigure(0, weight=1)
        frame_listbox_values.grid_rowconfigure(0, weight=1)
        self.listbox_values = tk.Listbox(frame_listbox_values, background='gray20', border=None, borderwidth=0)
        scroll_Y = ttk.Scrollbar(frame_listbox_values, orient='vertical', command=self.listbox_values.yview)
        scroll_X = ttk.Scrollbar(frame_listbox_values, orient='horizontal', command=self.listbox_values.xview)
        self.listbox_values.config(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        
        # Layout
        frame_listbox_values.grid(row=1, column=1, rowspan=2, sticky='nsew', pady=(0,10), padx=(10,10))
        self.listbox_values.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        scroll_Y.grid(row=0, column=1, sticky='ns')
        scroll_X.grid(row=1, column=0, sticky='ew')
        return None
    
    #endregion
    
    #region Action commands
    
    def on_item_click(self, event) -> None:
        self.dropdown_datatypes.set('Choose datatype')
        question = self.get_selected_question()
        self.controller.set_selected_question(question)
        if question is not None:
            self.fill_with_response_values(question)
            self.update_infobox(question)
        return None
    
    def action_button_apply(self) -> None:
        selected_datatype = self.dropdown_datatypes.get()
        question = self.get_selected_question()
        msg = self.controller.set_datatype_by_question(question, selected_datatype)
        if msg:
            response = tk.messagebox.askyesno(title='Convertion error', message=msg)
            if response:
                self.controller.set_datatype_by_question(question, 'float')
        self.fill_with_response_values(question)
        self.update_infobox(question)
        return None
    
    def action_drop_column(self) -> None:
        question = self.get_selected_question()
        if question:
            response = tk.messagebox.askyesno(title='Drop Column', message='Are you sure you want to drop the column?')
            if not response:
                return None
            self.controller.drop_column(question)
            self.listbox_values.delete(0, 'end')
            self.fill_questions()
        else:
            tk.messagebox.showerror(title='error', message='Please select a question to drop its column.')
        return None
    
    def action_show_unique(self) -> None:
        question = self.get_selected_question()
        unique_responses = self.controller.get_unique_responses(question)
        self.fill_listbox_responses(unique_responses)
        return None
    
    def action_remove_text(self) -> None:
        question = self.get_selected_question()
        text = self.entry_remove.get()
        self.entry_remove.delete(0, 'end')
        responses = self.controller.remove_text_in_column(question, text)
        self.fill_listbox_responses(responses)
        self.update_infobox(question)
        return None
    
    def action_close(self) -> None:
        self.destroy()
        return None
    
    #endregion
    
    
    #region Helper functions
    
    def fill_questions(self) -> None:
        questions = self.controller.get_questions_to_categorize()
        for idx, row in enumerate(questions):
            self.listbox_questions.insert(idx, row)
        return None
    
    def fill_with_response_values(self, question) -> None:
        responses = self.controller.get_responses_to_question(question)
        self.fill_listbox_responses(responses)
        return None
    
    def fill_listbox_responses(self, values) -> None:
        self.listbox_values.delete(0, 'end')
        for idx, row in enumerate(values):
            self.listbox_values.insert(idx, row)
        return None
    
    def get_selected_question(self) -> str | None:
        current_index = self.listbox_questions.curselection()
        if current_index:
            question = self.listbox_questions.get(current_index)
            return question
        else:
            return self.controller.get_selected_preparation_question()
        
    def update_infobox(self, question) -> None:
        info = self.controller.get_prepare_infobox(question)
        self.label_dtype_value.configure(text=info[constants.InfoBoxItem.CURRENT_DATATYPE])
        self.label_no_responses_value.configure(text=info[constants.InfoBoxItem.COUNT_RESPONSES])
        self.label_no_unique_responses_value.configure(text=info[constants.InfoBoxItem.NO_UNIQUE_RESPONES])
        return None
    
    #endregion