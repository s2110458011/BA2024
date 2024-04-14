from tkinter import *
import customtkinter
import menu
from homepage import *
from load import *

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self, title, size):
        
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.menu = menu.Menu(master=self, width=200)
        self.container = customtkinter.CTkFrame(self, width=800)
        #self.container.grid_rowconfigure(0, weight=1)
        #self.container.grid_columnconfigure(0, weight=1)
        
        self.create_layout()
        
        # self.frames = {}
        # for F in (HomePage, Load):
        #     frame = F(self.container, width=800)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky='nsew')
        # self.show_frame(HomePage)
        
        # run
        self.mainloop()
    
    def create_layout(self):
        self.menu.grid(row=0, column=0, sticky='ns')
        self.container.grid(row=0, column=1, sticky='nsew')
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    App('Survey Analyzing', (1000,600))