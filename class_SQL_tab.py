import tkinter as tk
from tkinter import ttk

import class_constants as consts

class SQL_TAB(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("SQL Configuration")
        self.geometry("400x300")
        self.root = root
        self.resizable(False, False)
        self.iconbitmap("icon.ico")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (consts.UART_WINDOW_WIDTH/2))
        y_cordinate = int((screen_height/2) - (consts.UART_WINDOW_HEIGHT/2))
        self.geometry("{}x{}+{}+{}".format(consts.UART_WINDOW_WIDTH, consts.UART_WINDOW_HEIGHT, x_cordinate, y_cordinate))
        
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.label_name = ttk.Label(self, text="SQL Configuration Settings")
        self.label_name.pack(pady=10)
        
        
        self.button_apply = ttk.Button(self, text="Apply", command=self.apply_settings)
        self.button_apply.pack(pady=10)
    
    
    def apply_settings(self):
        print("Applying SQL settings...")
        
    def create_layout(self):
        pass