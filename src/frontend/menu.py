from tkinter import *
import customtkinter

class Menu(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
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