from tkinter import *
import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        