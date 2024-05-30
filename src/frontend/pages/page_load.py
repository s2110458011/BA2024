import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Type, TYPE_CHECKING

from backend.data_processor.toolparser import *

if TYPE_CHECKING:
    from backend.controller import Controller

class Load(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.create_widgets()
        self.create_layout()
        return None
        
    #region Widgets & Layout
    
    def create_widgets(self) -> None:
        self.openfile = self.filedialog_frame()
        self.treeview = self.surveylist_widget()
        self.preview = self.survey_preview_frame()
        return None
    
    def create_layout(self) -> None:
        self.openfile.grid(row=0, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
        self.treeview.grid(row=2, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
        self.preview.grid(row=3, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
        return None
    
    def filedialog_frame(self) -> ctk.CTkFrame:
        frame_openfile = ctk.CTkFrame(self, width=800, corner_radius=0)
        
        # filename label
        self.lbl_filepath = ctk.CTkLabel(frame_openfile, text='Choose File', width=600)
        self.lbl_filepath.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.txt_filename = ctk.CTkEntry(frame_openfile, placeholder_text='Survey name', width=600, corner_radius=0)
        self.txt_filename.grid(row=1, column=0, padx=(10,10), pady=(0,10))
        
        # button open file dialog
        btn_open = ctk.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.select_file)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        btn_load = ctk.CTkButton(frame_openfile, text='Load', width=80, corner_radius=0, command=self.check_path_and_entry)
        btn_load.grid(row=1, column=1, padx=(0,10), pady=(0,10))
        return frame_openfile
    
    def surveylist_widget(self) -> ctk.CTkFrame:
        frame_surveylist = ctk.CTkFrame(self, corner_radius=0)
        frame_surveylist.grid_columnconfigure(1, weight=1)
        self.survey_list = ttk.Treeview(frame_surveylist)
        self.survey_list.bind('<ButtonRelease-1>', self.display_preview)
        self.survey_list.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        
        # Define columns
        self.survey_list['columns'] = ('Name', 'Path')
        self.survey_list.column("#0", width=0)
        self.survey_list.column('Name', anchor='w', width=150)
        self.survey_list.column('Path', anchor='w', width=540)
        
        # Create headings
        self.survey_list.heading('#0')
        self.survey_list.heading('Name', text='Survey name', anchor='w')
        self.survey_list.heading('Path', text='File Path', anchor='w')
        description_frame = ctk.CTkFrame(frame_surveylist, corner_radius=0)
        description_frame.grid(row=0, column=1, sticky='nsew', padx=(0,10), pady=10)
        
        # Labels survey description
        self.label_responses = ctk.CTkLabel(description_frame, text='Response count:')
        self.label_responses.pack()
        self.label_number_responses = ctk.CTkLabel(description_frame, text='')
        self.label_number_responses.pack()
        self.label_questions = ctk.CTkLabel(description_frame, text='Question count:')
        self.label_questions.pack()
        self.label_number_questions = ctk.CTkLabel(description_frame, text='')
        self.label_number_questions.pack()
        self.cb_var = tk.IntVar()
        self.cb_exclude_columns = ctk.CTkCheckBox(description_frame, text='Exclude', state='disabled',
                                                  corner_radius=0, checkbox_width=16, checkbox_height=16, border_width=2, 
                                                  variable=self.cb_var, onvalue=1, offvalue=0, command=self.cb_calculate)
        self.cb_exclude_columns.pack(pady_=(10,0))
        self.spinbox_number_cols = tk.Spinbox(description_frame, from_=0, to=20)
        self.spinbox_number_cols.pack(pady=10)
        return frame_surveylist
    
    def survey_preview_frame(self) -> ctk.CTkFrame:
        frame_preview = ctk.CTkFrame(self, corner_radius=0)
        frame_preview.grid_columnconfigure(0, weight=1)
        frame_preview.grid_rowconfigure(0, weight=1)
        self.data_table = ttk.Treeview(frame_preview)
        self.data_table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        scroll_Y = ttk.Scrollbar(self.data_table, orient='vertical', command=self.data_table.yview)
        scroll_X = ttk.Scrollbar(self.data_table, orient='horizontal', command=self.data_table.xview)
        self.data_table.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side='right', fill='y')
        scroll_X.pack(side='bottom', fill='x')
        return frame_preview
    
    #endregion
    
    #region Commands
    
    def select_file(self) -> None:
        file_path = ctk.filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        self.lbl_filepath.configure(text=file_path, anchor='w', padx=5)
        return None
    
    def check_path_and_entry(self) -> None:
        if self.lbl_filepath.cget(attribute_name='text') == 'Choose File':
            tk.messagebox.showerror(title='error', message='Please open a file to load.')
        elif self.txt_filename.get():
            self.open_file()
        else:
            tk.messagebox.showerror(title='error', message='Please enter a survey name.')
        return None
    
    def display_preview(self, e) -> None:
        self.cb_exclude_columns.configure(state='normal')
        selected_id = self.survey_list.focus()
        data = self.controller.get_survey_data_raw(selected_id)
        self.controller.set_current_survey_selection(selected_id)
        self.controller.activate_categorize_button()
        self.draw_table(data)
        self.controller.set_cb_survey_list_to_selected_survey()
        return None
    
    def cb_calculate(self) -> None:
        if self.cb_var.get() == 1:
            self.spinbox_number_cols.configure(state='disabled')
            questions = self.label_number_questions.cget('text')
            exclude = int(self.spinbox_number_cols.get())
            num = questions - exclude
            self.label_number_questions.configure(text=num)
        elif self.cb_var.get() == 0:
            questions = self.label_number_questions.cget('text')
            exclude = int(self.spinbox_number_cols.get())
            num = questions + exclude
            self.label_number_questions.configure(text=num)
            self.spinbox_number_cols.configure(state='normal')
        return None
    
    #endregion
    
    #region Utils
    
    def open_file(self) -> None:
        file_path = self.lbl_filepath.cget('text')
        survey_name = self.txt_filename.get()
        self.txt_filename.delete(0, tk.END)
        self.lbl_filepath.configure(text='Choose File')
        if file_path:
            #TODO check if file to open is not empty? was sucessful to read, etc.
            data = self.controller.load_data_from_file(file_path)
            id = self.controller.add_survey_to_library(survey_name, data)
            self.survey_list.insert(parent='', index='end', iid=id, text='', values=(survey_name, file_path))
            self.controller.update_survey_list()
        return None
    
    def draw_table(self, dataframe: pd.DataFrame):
        self.data_table.delete(*self.data_table.get_children())
        columns = list(dataframe.columns)
        
        self.data_table['columns'] = columns
        self.data_table.column('#0', width=0)
        self.data_table.heading('#0', text='')
        
        for col in columns:
            self.data_table.heading(col, text=col)
        self.data_table['show'] = 'headings'
            
        df_rows= dataframe.to_numpy().tolist()
        for row in df_rows:
            self.data_table.insert('', 'end', values=row)
        
        questions = self.calculate_number_of_questions()
        self.label_number_responses.configure(text=len(dataframe))
        self.label_number_questions.configure(text=len(dataframe.columns) - questions)
        return None
    
    def calculate_number_of_questions(self) -> int:
        if self.cb_var.get() == 1:
            return self.spinbox_number_cols.get()
        else:
            return 0
    
    #endregion
