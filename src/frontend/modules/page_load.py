import customtkinter
from tkinter import ttk
from tkinter import *
from typing import Type, TYPE_CHECKING

from backend.data_processor.toolparser import *
from backend.analysis.survey import Survey

if TYPE_CHECKING:
    from backend.controller import Controller

class Load(customtkinter.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.openfile = self.filedialog_frame()
        self.treeview = self.surveylist_widget()
    
    def create_layout(self):
        self.openfile.grid(row=0, column=0, pady=(10,0), padx=(10,0))
        self.treeview.grid(row=2, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
    
    def filedialog_frame(self) -> customtkinter.CTkFrame:
        frame_openfile = customtkinter.CTkFrame(self, corner_radius=0)
        
        # filename label
        self.lbl_filepath = customtkinter.CTkLabel(frame_openfile, text='Choose File', width=600)
        self.lbl_filepath.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.txt_filename = customtkinter.CTkEntry(frame_openfile, placeholder_text='Survey name', width=600)
        self.txt_filename.grid(row=1, column=0, padx=(10,10), pady=(0,10))
        
        # button open file dialog
        btn_open = customtkinter.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.select_file)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        btn_load = customtkinter.CTkButton(frame_openfile, text='Load', width=80, corner_radius=0, command=self.open_file)
        btn_load.grid(row=1, column=1, padx=(0,10), pady=(0,10))
        return frame_openfile
    
    def surveylist_widget(self) -> customtkinter.CTkFrame:
        frame_treeview = customtkinter.CTkFrame(self, corner_radius=0)
        self.survey_list = ttk.Treeview(frame_treeview)
        self.survey_list.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        
        # Define columns
        self.survey_list['columns'] = ('Name', 'Path')
        self.survey_list.column("#0", width=0)
        self.survey_list.column('Name', anchor='w', width=100)
        self.survey_list.column('Path', anchor='w', width=580)
        
        # Create headings
        self.survey_list.heading('#0')
        self.survey_list.heading('Name', text='Survey name', anchor='w')
        self.survey_list.heading('Path', text='File Path', anchor='w')
        return frame_treeview
    
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        self.lbl_filepath.configure(text=file_path, anchor='w', padx=5)
    
    def open_file(self):
        file_path = self.lbl_filepath.cget('text')
        survey_name = self.txt_filename.get()
        self.txt_filename.delete(0, END)
        self.lbl_filepath.configure(text='Choose File')
        if file_path:
            data = load_data_from_csv(file_path)
            survey = Survey(data)
            self.controller.add_survey_to_library(name=survey_name, survey=survey)
            id = self.controller.get_id()
            self.survey_list.insert(parent='', index='end', iid=id, text='', values=(survey_name, file_path))
        