import tkinter as tk
import customtkinter as ctk

from tkinter import ttk
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.controller import Controller


class Categorize(ctk.CTkToplevel):
    def __init__(self, master, controller: Type['Controller'], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.controller = controller
        self.geometry('800x500')
        self.title('Categorize Questions')
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.create_layout()
        self.fill_listbox_with_questions()
        
        return None
    
    def create_widgets(self) -> None:
        self.frame_listbox_questions = ctk.CTkFrame(self, fg_color='gray20')
        self.frame_listbox_questions.grid_columnconfigure(0, weight=1)
        self.listbox_questions = tk.Listbox(self.frame_listbox_questions, background='gray20', border=None, borderwidth=0)
        self.label_new_category = ctk.CTkLabel(self, text='New Category', anchor='w')
        self.textentry_new_category = ctk.CTkEntry(self)
        self.button_new_category = ctk.CTkButton(self, text='New', command=self.action_add_new_category)
        self.button_add_to_category = ctk.CTkButton(self, text='Add')
        self.button_remove_from_category = ctk.CTkButton(self, text='Remove')
        
        self.treeview_categories = ttk.Treeview(self)
        
        return None
    
    def create_layout(self) -> None:
        self.frame_listbox_questions.grid(row=0, column=0, rowspan=2, sticky='nsew', pady=20, padx=20)
        self.listbox_questions.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.label_new_category.grid(row=0, column=1, pady=20, sticky='w')
        self.textentry_new_category.grid(row=0, column=2, pady=20, padx=20)
        self.button_new_category.grid(row=0, column=3, padx=(0,20))
        self.button_add_to_category.grid(row=1, column=1)
        self.button_remove_from_category.grid(row=1, column=2)
        
        self.treeview_categories.grid(row=2, column=0, columnspan=5, sticky='nsew', padx=20)
        
        return None
    
    def fill_listbox_with_questions(self) -> None:
        questions = self.controller.get_questions()
        for idx, row in enumerate(questions):
            self.listbox_questions.insert(idx, row)
        
        return None
    
    def action_add_new_category(self) -> None:
        category = self.textentry_new_category.get()
        self.controller.add_new_category(category)
        return None