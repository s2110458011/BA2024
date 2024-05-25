from tkinter import *
import customtkinter as ctk

from frontend.pages.navigation import Navigation
from frontend.pages.homepage import HomePage
from frontend.pages.page_load import Load
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_report import Report
from frontend.pages.page_print import Print
from frontend.pages.page_save import Save

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class MainWindow(ctk.CTk):
    def __init__(self, controller, title: str, size: tuple[int, int]) -> None:
        # main setup
        super().__init__()
        self.controller = controller
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # navigation and content container
        self.menu = Navigation(master=self, navigation=self, controller=self.controller, width=200)
        self.container = ctk.CTkFrame(self, width=800)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.create_layout()
        
        self.frames = {}
        for F in (HomePage, Load, Prepare, Analyze, Report, Print, Save):
            frame = F(self.container, controller=controller, width=800)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(HomePage)
        return None
        
    
    def create_layout(self) -> None:
        self.menu.grid(row=0, column=0, sticky='ns')
        self.container.grid(row=0, column=1, sticky='nsew')
        return None
        
    
    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()
        return None
    
    def get_page(self, page_class) -> HomePage | Load | Prepare | Analyze | Report | Print | Save:
        return self.frames[page_class]
    
    def get_navigation(self) -> Navigation:
        return self.menu
    
    def exit(self) -> None:
        self.destroy()
        return None

