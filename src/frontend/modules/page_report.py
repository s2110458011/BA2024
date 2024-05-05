import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller

class Report(ctk.CTkFrame):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, corner_radius=0, **kwargs)
        self.controller = controller
        self.labels_list_preview = []
        
        self.create_widgets()
        self.create_main_layout()
        
        return None
    
    #region Layout
    
    def create_widgets(self) -> None:
        # Settings and options
        self.left_side_frame = ctk.CTkFrame(self, corner_radius=0, width=500)
        self.create_options_widget()
        
        # Preview section (left side)
        self.right_side_frame = ctk.CTkFrame(self, corner_radius=0)
        self.create_preview_widget()
        
        return None
    
    def create_main_layout(self) -> None:
        self.left_side_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.right_side_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky='nsew')
        self.grid_columnconfigure(1, weight=1)
        
        return None
    
    def create_preview_widget(self) -> None:
        preview_frame = ctk.CTkScrollableFrame(self.right_side_frame, corner_radius=0, fg_color='transparent')
        preview_frame.grid(row=0, column=0, sticky='nsew')
        self.right_side_frame.grid_rowconfigure(0, weight=1)
        
        preview_buttons_frame = ctk.CTkFrame(self.right_side_frame, corner_radius=0, fg_color='transparent')
        preview_buttons_frame.grid(row=1, column=0, sticky='nsew')
        self.right_side_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons
        up_image = ctk.CTkImage(Image.open('src/assets/button_up.png'), size=(20,20))
        button_move_up = ctk.CTkButton(preview_buttons_frame, text='', image=up_image, width=30)
        button_move_up.grid(row=0, column=0, padx=(10,0), pady=10)
        down_image = ctk.CTkImage(Image.open('src/assets/button_down.png'), size=(20,20))
        button_move_down = ctk.CTkButton(preview_buttons_frame, text='', image=down_image, width=30)
        button_move_down.grid(row=0, column=1, padx=(10,0), pady=10)
        bin_image = ctk.CTkImage(Image.open('src/assets/button_bin.png'), size=(20,20))
        button_remove = ctk.CTkButton(preview_buttons_frame, text='', image=bin_image, width=30)
        button_remove.grid(row=0, column=2, padx=(10,0), pady=10)
        preview_image = ctk.CTkImage(Image.open('src/assets/button_preview.png'), size=(20,20))
        button_preview_pdf = ctk.CTkButton(preview_buttons_frame, text='', image=preview_image, width=30)
        button_preview_pdf.grid(row=0, column=3, padx=(10,0), pady=10)
        
        return None
    
    def create_options_widget(self) -> None:
        label_options = ctk.CTkLabel(self.left_side_frame, text='Add Header', anchor='w')
        label_options.grid(row=0, column=0, columnspan=2, padx=(20,0), pady=(20,0), sticky='ew')
        text_entry_header = ctk.CTkEntry(self.left_side_frame, width=400)
        text_entry_header.grid(row=1, column=0, padx=(20,0), pady=(10,0), sticky='w')
        button_add_header = ctk.CTkButton(self.left_side_frame, text='Add Header')
        button_add_header.grid(row=1, column=1, padx=(0,20), pady=(10,0), sticky='w')
        
        frame_items_list = ctk.CTkFrame(self.left_side_frame, corner_radius=0, fg_color='#1E1E1E')
        frame_items_list.grid(row=2, column=0, padx=20, pady=20, sticky='w')
        label_report_items = ctk.CTkLabel(frame_items_list, text='Report items', width=380, anchor='w')
        label_report_items.grid(row=0, column=0, padx=10, sticky='ew')
        report_items_list = tk.Listbox(frame_items_list, borderwidth=0)
        report_items_list.grid(row=1, column=0, padx=10, pady=10)
        button_add_item = ctk.CTkButton(self.left_side_frame, text='Add item')
        button_add_item.grid(row=2, column=1, pady=50, sticky='nw')
        
        return None
    
    #endregion
    
    #region Button commands
    
    def create_new_heading_label(self) -> ctk.CTkLabel:
        
        pass
    
    def create_new_report_item_label(self) -> ctk.CTkLabel:
        pass
    
    def add_label_to_list(self, preview_item: ctk.CTkLabel) -> None:
        self.labels_list_preview.append(preview_item)
        return None
    
    def preview_report(self) -> None:
        
        
        return None
    
    #endregion
    
    #region Helper functions
    
    
    #endregion