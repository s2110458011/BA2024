from tkinter import *
from typing import Any, Tuple
import customtkinter

# set the theme and color options
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self, title, size):
        
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # widgets
        self.menu = Menu(master=self, width=200)
        self.content = ContentFrame(master=self, width=800)
        
        # layout
        self.create_layout()
        
        # run
        self.mainloop()
    
    def create_layout(self):
        self.menu.grid(column=0, sticky='ns')
        self.content.grid(column=1, sticky='nsew')


class Menu(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.grid(column=0, sticky='ns')
        
        self.create_widgets()
        self.create_layout()
    
    def create_menu_button(self, name, btn_height, btn_corner_radius, action=None):
        return customtkinter.CTkButton(
            self,
            text=name,
            height=btn_height,
            corner_radius=btn_corner_radius,
            command=action
        )
    
    def create_widgets(self):
        self.lbl_menu = customtkinter.CTkLabel(self, text='Menu', height=20)
        self.btn_load = self.create_menu_button('Load', 30, 0)
        self.btn_prepare = self.create_menu_button('Prepare', 30, 0)
        self.btn_analyze = self.create_menu_button('Analyze', 30, 0)
        self.btn_print = self.create_menu_button('Print', 30, 0)
        self.btn_save = self.create_menu_button('Save', 30, 0)
    
    def create_layout(self):
        # place the widgets
        self.lbl_menu.grid(row=0, pady=20)
        self.btn_load.grid(row=1)
        self.btn_prepare.grid(row=2, pady=10)
        self.btn_analyze.grid(row=3)
        self.btn_print.grid(row=4, pady=10)
        self.btn_save.grid(row=5)
    

class ContentFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.grid(row=0, column=1, padx=(15,0), sticky='nsew')
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure(0, weight=1)
        
    def open_load(self):
        self.load = Load(master=self, width=800)
        
class Load(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.grid(row=0, column=0, sticky='nsew')
        
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.openfile = self.filedialog_frame()
    
    def create_layout(self):
        self.openfile.grid(row=0, column=0, pady=(10,0), padx=(10,0))
    
    def filedialog_frame(self):
        frame_openfile = customtkinter.CTkFrame(self, corner_radius=0)
        # filename label
        self.lbl_filename = customtkinter.CTkLabel(frame_openfile, text='Choose File', bg_color='grey', width=700)
        self.lbl_filename.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        
        # button open file dialog
        btn_open = customtkinter.CTkButton(frame_openfile, text='Open', width=80, corner_radius=0, command=self.selectfile)
        btn_open.grid(row=0, column=1, padx=(0,10), pady=(10,10))
        return frame_openfile
    
    def selectfile(self):
        filename = customtkinter.filedialog.askopenfilename()
        self.lbl_filename.configure(text=filename, anchor='w', padx=5)

App('Class based app', (1000,600))