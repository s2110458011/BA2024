from tkinter import *
import customtkinter

class Load(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
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
        self.lbl_filename = customtkinter.CTkLabel(frame_openfile, text='Choose File', width=700)
        self.lbl_filename.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        
        # button open file dialog
        btn_open = customtkinter.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.selectfile)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        return frame_openfile
    
    def selectfile(self):
        filename = customtkinter.filedialog.askopenfilename()
        self.lbl_filename.configure(text=filename, anchor='w', padx=5)
        