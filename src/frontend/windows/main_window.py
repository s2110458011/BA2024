import customtkinter as ctk
from frontend.pages.navigation import Navigation
from frontend.pages.page_load import Load
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_report import Report
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class MainWindow(ctk.CTk):
    def __init__(self, controller: Type['Controller'], title: str, size: tuple[int, int]) -> None:
        # main setup
        super().__init__()
        self.controller: Type['Controller'] = controller
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # navigation and content container
        self.menu: Type['Navigation'] = Navigation(master=self, controller=self.controller, width=200)
        self.container: ctk.CTkFrame = ctk.CTkFrame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.create_layout()
        
        self.frames = {}
        for F in (Load, Prepare, Analyze, Report):
            frame = F(self.container, controller=controller)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(Load)
        return None
        
    def create_layout(self) -> None:
        self.menu.grid(row=0, column=0, sticky='ns')
        self.container.grid(row=0, column=1, sticky='nsew')
        return None
        
    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()
        return None
    
    def get_page(self, page_class) -> Load | Prepare | Analyze | Report:
        return self.frames[page_class]
    
    def get_navigation(self) -> Navigation:
        return self.menu
    
    def exit(self) -> None:
        self.destroy()
        return None

