from tkinter import *
import customtkinter

class Print(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller