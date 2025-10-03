import tkinter as tk
import serial
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 250

myFontMain = ("Helvetica", 15)

root = tk.Tk()
root.title("Kompiuterinės komunikacijos 2 laboratorinis darbas")
root.geometry("1000x600")
root.iconbitmap("icon.ico")

def com_port_settings():
    
    myWindow_uart_settings = tk.Toplevel(root)
    myWindow_uart_settings.geometry("200x600")
    myWindow_uart_settings.resizable(False, False)
    myWindow_uart_settings.title("UART settings")

    screen_width = myWindow_uart_settings.winfo_screenwidth()
    screen_height = myWindow_uart_settings.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (WINDOW_WIDTH/2))
    y_cordinate = int((screen_height/2) - (WINDOW_HEIGHT/2))
    myWindow_uart_settings.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
    myWindow_uart_settings.iconbitmap("icon.ico")


myButton_quit = tk.Button(root, text="Exit", command=root.destroy,width=4, height=1,font=myFontMain)
myButton_port_settings = tk.Button(root, text="Serial Port Settings", command=lambda :com_port_settings(),padx=80,pady=10,width=4, height=1,font=myFontMain)





myButton_quit.grid(row=3, column=3)
myButton_port_settings.grid(row=3, column=0)

tk.mainloop()