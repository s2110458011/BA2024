import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller

class Report(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        
        self.create_widgets()
        self.create_layout()
        
        return None
    
    def create_widgets(self) -> None:
        # Settings and options
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, width=300)
        
        
        # Preview
        self.preview_frame = ctk.CTkFrame(self, corner_radius=0)
        
        return None
    
    def create_layout(self) -> None:
        self.settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        
        self.preview_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky='nsew')
        self.grid_columnconfigure(1, weight=1)
        
        return None