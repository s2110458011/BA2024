from tkinter import *
import customtkinter
from frontend.page_load import *
from frontend.page_prepare import *
from frontend.page_analyze import *
from frontend.page_print import *
from frontend.page_save import *

class Menu(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
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
        self.btn_load = self.create_menu_button('Load', 30, 0, action=self.load_click)
        self.btn_prepare = self.create_menu_button('Prepare', 30, 0, action=self.prepare_click)
        self.btn_analyze = self.create_menu_button('Analyze', 30, 0, action=self.analyze_click)
        self.btn_print = self.create_menu_button('Print', 30, 0, action=self.print_click)
        self.btn_save = self.create_menu_button('Save', 30, 0, action=self.save_click)
    
    def create_layout(self):
        # place the widgets
        self.lbl_menu.grid(row=0, pady=20)
        self.btn_load.grid(row=1)
        self.btn_prepare.grid(row=2, pady=10)
        self.btn_analyze.grid(row=3)
        self.btn_print.grid(row=4, pady=10)
        self.btn_save.grid(row=5)
        
    def load_click(self):
        self.controller.show_frame(Load)
    
    def prepare_click(self):
        self.controller.show_frame(Prepare)
        
    def analyze_click(self):
        self.controller.show_frame(Analyze)
    
    def print_click(self):
        self.controller.show_frame(Print)
    
    def save_click(self):
        self.controller.show_frame(Save)