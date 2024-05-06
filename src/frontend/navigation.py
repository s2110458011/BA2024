import tkinter as ttk
import customtkinter as ctk
from frontend.pages.page_load import Load
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_print import Print
from frontend.pages.page_save import Save
from frontend.pages.page_report import Report

class Navigation(ctk.CTkFrame):
    def __init__(self, master, navigation, controller, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.main_window = navigation
        self.controller = controller
        
        self.create_widgets()
        self.create_layout()
    
    def create_menu_button(self, name, btn_height, btn_corner_radius, action=None, **kwargs):
        return ctk.CTkButton(
            self,
            text=name,
            height=btn_height,
            corner_radius=btn_corner_radius,
            command=action,
            **kwargs
        )
    
    def create_widgets(self):
        self.lbl_menu = ctk.CTkLabel(self, text='Menu', height=20)
        self.btn_load = self.create_menu_button('Load', 30, 0, action=self.load_click)
        self.btn_prepare = self.create_menu_button('Prepare', 30, 0, action=self.prepare_click)
        self.btn_analyze = self.create_menu_button('Analyze', 30, 0, action=self.analyze_click)
        self.btn_report = self.create_menu_button('Report', 30, 0, action=self.report_click)
        self.btn_print = self.create_menu_button('Print', 30, 0, action=self.print_click, state='disabled', fg_color='gray30')
        self.btn_save = self.create_menu_button('Save', 30, 0, action=self.save_click, state='disabled', fg_color='gray30')
        self.btn_exit = self.create_menu_button('Exit', 30, 0, action=self.exit_click, fg_color='darkred')
        
    
    def create_layout(self):
        # place the widgets
        self.lbl_menu.grid(row=0, pady=20)
        self.btn_load.grid(row=1)
        self.btn_prepare.grid(row=2, pady=10)
        self.btn_analyze.grid(row=3)
        self.btn_report.grid(row=4, pady=10)
        self.btn_print.grid(row=5)
        self.btn_save.grid(row=6, pady=10)
        self.btn_exit.grid(row=7)
        
    def load_click(self):
        self.main_window.show_frame(Load)
    
    def prepare_click(self):
        self.main_window.show_frame(Prepare)
        
    def analyze_click(self):
        self.main_window.show_frame(Analyze)
    
    def report_click(self):
        self.main_window.show_frame(Report)
    
    def print_click(self):
        self.main_window.show_frame(Print)
    
    def save_click(self):
        self.main_window.show_frame(Save)
    
    def exit_click(self):
        self.main_window.exit()