import customtkinter
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
    
    def create_layout(self):
        self.openfile.grid(row=0, column=0, pady=(10,0), padx=(10,0))
    
    def filedialog_frame(self):
        frame_openfile = customtkinter.CTkFrame(self, corner_radius=0)
        
        # filename label
        self.lbl_filename = customtkinter.CTkLabel(frame_openfile, text='Choose File', width=600)
        self.lbl_filename.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        
        # button open file dialog
        btn_open = customtkinter.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.select_file)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        btn_load = customtkinter.CTkButton(frame_openfile, text='Load', width=80, corner_radius=0)
        btn_load.grid(row=0, column=2, padx=(0,10), pady=(10,10))
        return frame_openfile
    
    def select_file(self):
        file_path = customtkinter.filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        self.lbl_filename.configure(text=file_path, anchor='w', padx=5)
    
    def open_file(self):
        file_path = self.lbl_filename.getvar
        if file_path:
            data = load_data_from_csv(file_path)
            survey = Survey(data)
            self.controller.add_survey_to_library(survey)
        