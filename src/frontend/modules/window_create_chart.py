import tkinter as tk
import customtkinter as ctk

from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller
    

class CreateChart(ctk.CTkToplevel):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.geometry('800x500')
        self.title('Create New Charts')
        
        
        return None