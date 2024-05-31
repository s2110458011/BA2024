import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from frontend.pages.page_load import Load
from frontend.pages.page_prepare import Prepare
from frontend.pages.page_analyze import Analyze
from frontend.pages.page_report import Report
from PIL import Image
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller
    from frontend.windows.main_window import MainWindow

class Navigation(ctk.CTkFrame):
    def __init__(self, master: Type['MainWindow'], controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.main_window: Type['MainWindow'] = master
        self.controller: Type['Controller'] = controller
        
        self.create_widgets()
        self.create_layout()
        self.current_page = 'Load'
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
        try:
            img_path = self.get_image_path('fulllogo_transparent.png')
            image = Image.open(img_path)
            photo = ctk.CTkImage(image, size=(160,120))
            self.lbl_menu = ctk.CTkLabel(self, text='', image=photo, height=60, width=30)
        except:
            self.lbl_menu = ctk.CTkLabel(self, text='Menu', height=20)
        self.lbl_menu._image = photo
        self.btn_load = self.create_menu_button('Load', 30, 0, action=self.load_click)
        self.btn_prepare = self.create_menu_button('Prepare', 30, 0, action=self.prepare_click)
        self.btn_analyze = self.create_menu_button('Analyze', 30, 0, action=self.analyze_click)
        self.btn_report = self.create_menu_button('Report', 30, 0, action=self.report_click)
        self.btn_save = self.create_menu_button('Save', 30, 0, action=self.save_click, state='disabled', fg_color='gray30')
        self.btn_exit = self.create_menu_button('Exit', 30, 0, action=self.exit_click, fg_color='darkred')
        return None
    
    def create_layout(self) -> None:
        # place the widgets
        self.lbl_menu.grid(row=0, sticky='nsew')
        self.btn_load.grid(row=1, sticky='nsew')
        self.btn_prepare.grid(row=2, pady=10, sticky='nsew')
        self.btn_analyze.grid(row=3, sticky='nsew')
        self.btn_report.grid(row=4, pady=10, sticky='nsew')
        self.btn_save.grid(row=6, pady=10, sticky='nsew')
        self.btn_exit.grid(row=7, sticky='nsew')
        return None
    
    #endregion
    
    #region Button Commands
        
    def load_click(self) -> None:
        self.main_window.show_frame(Load)
        self.set_save_button_state('disabled')
        self.current_page = 'Load'
        return None
    
    def prepare_click(self) -> None:
        self.main_window.show_frame(Prepare)
        self.set_save_button_state('disabled')
        self.current_page = 'Prepare'
        return None
        
    def analyze_click(self) -> None:
        self.main_window.show_frame(Analyze)
        self.set_save_button_state('normal')
        self.current_page = 'Analyze'
        return None
    
    def report_click(self) -> None:
        self.main_window.show_frame(Report)
        self.set_save_button_state('normal')
        self.current_page = 'Report'
        return None
    
    def save_click(self) -> None:
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
        self.main_window.destroy()
        self.main_window.quit()
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
    
    def get_image_path(self, image_name) -> os.path:
        base_dir = os.path.dirname(__file__)
        src_dir = os.path.abspath(os.path.join(base_dir, '..'))
        image_dir = os.path.join(src_dir, 'assets')
        image_path = os.path.join(image_dir, image_name)
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return image_path
    
    #endregion