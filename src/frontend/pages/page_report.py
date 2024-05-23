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
        self.preview_labels: list[ctk.CTkLabel] = []
        self.current_item: ctk.CTkLabel = None
        
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
        self.preview_frame = ctk.CTkScrollableFrame(self.right_side_frame, corner_radius=0, fg_color='transparent')
        self.preview_frame.grid(row=0, column=0, sticky='nsew')
        self.right_side_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        
        # Place preview labels
        
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
        self.left_side_frame.grid_columnconfigure(1, weight=1)
        label_report_title = ctk.CTkLabel(self.left_side_frame, text='Report Title', anchor='w')
        label_report_title.grid(row=0, column=0, padx=(20,0), pady=(20,0), sticky='w')
        self.text_entry_title = ctk.CTkEntry(self.left_side_frame, corner_radius=0)
        self.text_entry_title.grid(row=0, column=1, padx=(10,20), pady=(20,0), sticky='ew')
        self.button_add_title = ctk.CTkButton(self.left_side_frame, text='Add Title', corner_radius=0, command=self.create_new_report)
        self.button_add_title.grid(row=0, column=2, padx=(0,20), pady=(20,0), sticky='w')
        
        label_header = ctk.CTkLabel(self.left_side_frame, text='Add Header', anchor='w')
        label_header.grid(row=1, column=0, padx=(20,0), pady=(20,0), sticky='w')
        self.text_entry_header = ctk.CTkEntry(self.left_side_frame, corner_radius=0)
        self.text_entry_header.grid(row=1, column=1, padx=(10,20), pady=(20,0), sticky='ew')
        button_add_header = ctk.CTkButton(self.left_side_frame, text='Add Header', corner_radius=0, command=self.create_new_heading_label)
        button_add_header.grid(row=1, column=2, padx=(0,20), pady=(20,0), sticky='w')
        
        frame_items_list = ctk.CTkFrame(self.left_side_frame, corner_radius=0, fg_color='#1E1E1E')
        frame_items_list.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky='w')
        label_report_items = ctk.CTkLabel(frame_items_list, text='Report items', width=400, anchor='w')
        label_report_items.cget('font').configure(underline=True)
        label_report_items.grid(row=0, column=0, padx=10, sticky='ew')
        self.report_items_list = tk.Listbox(frame_items_list, borderwidth=0)
        self.report_items_list.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        button_add_item = ctk.CTkButton(self.left_side_frame, text='Add item', corner_radius=0, command=self.add_item_to_report)
        button_add_item.grid(row=3, column=2, pady=50, sticky='nw')
        
        return None
    
    #endregion
    
    #region Button commands
    
    def create_new_heading_label(self) -> None:
        label_text = self.text_entry_header.get()
        self.text_entry_header.delete(0, 'end')
        self.add_label_to_list(label_text, '#228B22')
        self.controller.update_final_report_items_list(label_text, 'heading')
        return None
    
    def add_item_to_report(self) -> None:
        selected_idx = self.report_items_list.curselection()
        if selected_idx:
            item = self.report_items_list.get(selected_idx)
            self.add_label_to_list(item, '#6E8B3D')
            self.controller.update_final_report_items_list(item, 'plot')
        return None
    
    def preview_report(self) -> None:
        
        
        return None
    
    def create_new_report(self) -> None:
        title = self.text_entry_title.get()
        self.text_entry_title.delete(0, 'end')
        self.controller.create_new_report(title)
        self.add_title_to_preview(title)
        
        self.button_add_title.grid_forget()
        change_title = ctk.CTkButton(self.left_side_frame, text='Change Title', corner_radius=0, command=self.update_report_title)
        change_title.grid(row=0, column=2, padx=(0,20), pady=(20,0), sticky='w')
        return None
    
    def update_report_title(self) -> None:
        new_title = self.text_entry_title.get()
        self.text_entry_title.delete(0, 'end')
        if self.controller.update_report_title(new_title):
            self.preview_label_title.configure(text=new_title)
        return None
    
    def add_title_to_preview(self, title) -> None:
        self.preview_label_title = ctk.CTkLabel(self.preview_frame, text=title, fg_color='#006400')
        self.preview_label_title.grid(row=0, column=0, padx=10, pady=20, sticky='ew')
        return None
    
    #endregion
    
    #region Helper functions
    
    def add_label_to_list(self, preview_item: str, label_color: str) -> None:
        preview_label = ctk.CTkLabel(self.preview_frame, text=preview_item, fg_color=label_color)
        preview_label.bind('<Button-1>', self.on_label_click)
        self.preview_labels.append(preview_label)
        self.place_preview_labels()
        return None
    
    def remove_preview_labels(self) -> None:
        for item in self.preview_frame.winfo_children():
            item.grid_forget
        return None
    
    def place_preview_labels(self) -> None:
        for idx, item in enumerate(self.preview_labels):
            idx+=1 # add one because title label is in row=0
            item.grid(row=idx, column=0, padx=10, pady=5, sticky='ew')
        
        return None
    
    def on_label_click(self, e) -> None:
        clicked_label = e.widget
        self.current_item = clicked_label
        return None
    
    def update_report_items_list(self, items_list: list) -> None:
        self.report_items_list.delete(0, 'end')
        for idx, report_item in enumerate(items_list):
            self.report_items_list.insert(idx, report_item)
        return None
    
    #endregion