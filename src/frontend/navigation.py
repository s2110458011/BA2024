import tkinter as ttk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from frontend.pages.homepage import HomePage
from frontend.pages.page_load import Load
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_print import Print
from frontend.pages.page_save import Save
from frontend.pages.page_report import Report
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller
    from frontend.main_window import MainWindow

class Navigation(ctk.CTkFrame):
    def __init__(self, master: Type['MainWindow'], controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.main_window = master
        self.controller = controller
        
        self.create_widgets()
        self.create_layout()
        self.current_page = 'HomePage'
        return None
    
    #region Widgets & Layout
    
    def create_menu_button(self, name, btn_height, btn_corner_radius, action=None, **kwargs) -> ctk.CTkButton:
        return ctk.CTkButton(
            self,
            text=name,
            height=btn_height,
            corner_radius=btn_corner_radius,
            command=action,
            **kwargs
        )
    
    def create_widgets(self) -> None:
        self.lbl_menu = ctk.CTkLabel(self, text='Menu', height=20)
        self.btn_load = self.create_menu_button('Load', 30, 0, action=self.load_click)
        self.btn_prepare = self.create_menu_button('Prepare', 30, 0, action=self.prepare_click)
        self.btn_analyze = self.create_menu_button('Analyze', 30, 0, action=self.analyze_click)
        self.btn_report = self.create_menu_button('Report', 30, 0, action=self.report_click)
        #self.btn_print = self.create_menu_button('Print', 30, 0, action=self.print_click, state='disabled', fg_color='gray30')
        self.btn_save = self.create_menu_button('Save', 30, 0, action=self.save_click, state='disabled', fg_color='gray30')
        self.btn_exit = self.create_menu_button('Exit', 30, 0, action=self.exit_click, fg_color='darkred')
        return None
    
    def create_layout(self) -> None:
        # place the widgets
        self.lbl_menu.grid(row=0, pady=20)
        self.btn_load.grid(row=1)
        self.btn_prepare.grid(row=2, pady=10)
        self.btn_analyze.grid(row=3)
        self.btn_report.grid(row=4, pady=10)
        #self.btn_print.grid(row=5)
        self.btn_save.grid(row=6, pady=10)
        self.btn_exit.grid(row=7)
        return None
    
    #endregion
    
    #region Button Commands
        
    def load_click(self) -> None:
        self.main_window.show_frame(Load)
        #self.set_print_button_state('disabled')
        self.set_save_button_state('disabled')
        self.current_page = 'Load'
        return None
    
    def prepare_click(self) -> None:
        self.main_window.show_frame(Prepare)
        #self.set_print_button_state('disabled')
        self.set_save_button_state('disabled')
        self.current_page = 'Prepare'
        return None
        
    def analyze_click(self) -> None:
        self.main_window.show_frame(Analyze)
        #self.set_print_button_state('normal')
        self.set_save_button_state('normal')
        self.current_page = 'Analyze'
        return None
    
    def report_click(self) -> None:
        self.main_window.show_frame(Report)
        #self.set_print_button_state('normal')
        self.set_save_button_state('normal')
        self.current_page = 'Report'
        return None
    
    def print_click(self) -> None:
        # maybe remove
        self.main_window.show_frame(Print)
        return None
    
    def save_click(self) -> None:
        #self.main_window.show_frame(Save)
        if self.current_page == 'Analyze':
            if self.controller.valid_to_save():
                response = messagebox.askyesno("Confirmation", "Do you want to save the plot with the description text?")
            else:
                messagebox.showerror('Error', 'Please select a chart to save.')
                return None
            
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('JPG files', '*.jpg'), ('All files' ,'*.*')])
            if file_path:
                self.controller.save_chart_to_image(file_path, response)
        else:
            file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF files', '*.pdf')])
            self.controller.save_report_to_pdf(file_path)
        return None
    
    def exit_click(self) -> None:
        self.main_window.quit()
        self.main_window.destroy()
        return None
    
    #endregion
    
    #region Utils
    
    def set_save_button_state(self, state: str) -> None:
        self.btn_save.configure(state=state)
        if state == 'normal':
            self.btn_save.configure(fg_color=['#2CC985', '#2FA572'])
        else:
            self.btn_save.configure(fg_color='gray30')
        return None
    
    def set_print_button_state(self, state: str) -> None:
        self.btn_print.configure(state=state)
        if state == 'normal':
            self.btn_print.configure(fg_color=['#2CC985', '#2FA572'])
        else:
            self.btn_print.configure(fg_color='gray30')
        return None
    
    #endregion