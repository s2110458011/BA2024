import customtkinter as ctk
import tkinter as ttk
from typing import Type, TYPE_CHECKING

from backend.data_processor.toolparser import *
from backend.analysis.survey import Survey

if TYPE_CHECKING:
    from backend.controller import Controller

class Load(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self) -> None:
        self.openfile = self.filedialog_frame()
        self.treeview = self.surveylist_widget()
        self.preview = self.survey_preview_frame()
    
    def create_layout(self) -> None:
        self.openfile.grid(row=0, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
        self.treeview.grid(row=2, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
        self.preview.grid(row=3, column=0, pady=(10,0), padx=(10,0), sticky='nsew')
    
    def filedialog_frame(self) -> ctk.CTkFrame:
        frame_openfile = ctk.CTkFrame(self, width=800, corner_radius=0)
        
        # filename label
        self.lbl_filepath = ctk.CTkLabel(frame_openfile, text='Choose File', width=600)
        self.lbl_filepath.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.txt_filename = ctk.CTkEntry(frame_openfile, placeholder_text='Survey name', width=600)
        self.txt_filename.grid(row=1, column=0, padx=(10,10), pady=(0,10))
        
        # button open file dialog
        btn_open = ctk.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.select_file)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        btn_load = ctk.CTkButton(frame_openfile, text='Load', width=80, corner_radius=0, command=self.open_file)
        btn_load.grid(row=1, column=1, padx=(0,10), pady=(0,10))
        return frame_openfile
    
    def surveylist_widget(self) -> ctk.CTkFrame:
        frame_treeview = ctk.CTkFrame(self, corner_radius=0)
        self.survey_list = ttk.ttk.Treeview(frame_treeview)
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
        return frame_treeview
    
    def survey_preview_frame(self) -> ctk.CTkFrame:
        frame_preview = ctk.CTkFrame(self, corner_radius=0)
        self.tb_preview = ctk.CTkTextbox(frame_preview, width=800, height=225, corner_radius=0)
        self.tb_preview.grid(row=0, column=0, padx=10, pady=10)
        return frame_preview
    
    def select_file(self) -> None:
        file_path = ctk.filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        self.lbl_filepath.configure(text=file_path, anchor='w', padx=5)
    
    def open_file(self) -> None:
        file_path = self.lbl_filepath.cget('text')
        survey_name = self.txt_filename.get()
        self.txt_filename.delete(0, ttk.END)
        self.lbl_filepath.configure(text='Choose File')
        if file_path:
            #TODO check if file to open is not empty? was sucessful to read, etc.
            data = load_data_from_csv(file_path)
            survey = Survey(data)
            self.controller.add_survey_to_library(name=survey_name, survey=survey)
            id = self.controller.get_id()
            self.survey_list.insert(parent='', index='end', iid=id, text='', values=(survey_name, file_path))    