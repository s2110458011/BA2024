from tkinter import *
import customtkinter as ctk

from frontend.navigation import Navigation
from frontend.homepage import HomePage
from frontend.modules.page_load import Load
from frontend.modules.page_prepare import Prepare
from frontend.modules.page_analyze import Analyze
from frontend.modules.page_print import Print
from frontend.modules.page_save import Save

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
        for F in (HomePage, Load, Prepare, Analyze, Print, Save):
            frame = F(self.container, controller=controller, width=800)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(HomePage)
        
    
    def create_layout(self) -> None:
        self.menu.grid(row=0, column=0, sticky='ns')
        self.container.grid(row=0, column=1, sticky='nsew')
        
    
    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()
    
    def get_page(self, page_class) -> ctk.CTkFrame:
        return self.frames[page_class]
    
    def exit(self) -> None:
        self.controller.exit()

