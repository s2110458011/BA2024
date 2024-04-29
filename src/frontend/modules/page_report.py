import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from typing import Type, TYPE_CHECKING

from frontend.modules.window_categorize import Categorize

if TYPE_CHECKING:
    from backend.controller import Controller

class Report(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        
        return None