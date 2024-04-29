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
        self.button_add_to_category = ctk.CTkButton(self, text='Add', command=self.action_add_question_to_category)
        self.button_remove_from_category = ctk.CTkButton(self, text='Remove')
        
        self.treeview_categories = ttk.Treeview(self)
        self.initialize_treeview_categories()
        
        self.button_save_categories = ctk.CTkButton(self, text='Save', command=self.action_save_categories)
        
        return None
    
    def initialize_treeview_categories(self) -> None:
        self.treeview_categories['columns'] = ['Question']
        self.treeview_categories.column('#0', width=10)
        self.treeview_categories.heading('#0', text='Category')
        self.treeview_categories.heading('Question', text='Question')
        
        if not self.controller.check_categorized_questions_empty():
            categorized_questions = self.controller.get_categorized_questions()
            for key, value in categorized_questions.items():
                self.treeview_categories.insert('', 'end', text=key)
                id = self.treeview_categories.get_children()[-1]
                for item in value:
                    self.treeview_categories.insert(id, 'end', values=[item])
        
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
        self.button_save_categories.grid(row=3, column=3, pady=20, padx=20)
        
        return None
    
    def fill_listbox_with_questions(self) -> None:
        questions = self.controller.get_questions_to_categorize()
        for idx, row in enumerate(questions):
            self.listbox_questions.insert(idx, row)
        return None
    
    def action_add_new_category(self) -> None:
        category = self.textentry_new_category.get()
        self.textentry_new_category.delete(0, 'end')
        self.controller.add_new_category(category)
        self.treeview_categories.insert('', 'end', text=category)
        return None
    
    def action_add_question_to_category(self) -> None:
        question_id = self.listbox_questions.curselection()
        question = self.listbox_questions.get(question_id)
        self.listbox_questions.delete(question_id)
        selected_category_id = self.treeview_categories.focus()
        selected_category = self.treeview_categories.item(selected_category_id, 'text')
        self.treeview_categories.insert(selected_category_id, 'end', values=[question])
        self.controller.add_question_to_category(selected_category, question)
        return None
    
    def action_save_categories(self) -> None:
        free_questions = [self.listbox_questions.get(i) for i in range(self.listbox_questions.size())]
        self.controller.save_not_categorized_questions(free_questions)
        self.destroy()
        return None