#main packages
import tkinter as tk

#declaring my modules
import KK_Lab2_UART_TAB
import KK_Lab2_FUNCTIONS as Func
import KK_Lab2_GLOBALS as globals

#main window
root = tk.Tk()
root.title("Kompiuterinės komunikacijos 2 laboratorinis darbas")
root.geometry("1000x600")
root.iconbitmap("icon.ico")

myButton_quit = tk.Button(root, text="Exit", command=lambda : Func.GUI_Exit(root),width=4, height=1,font=globals.myFontMain)
myButton_port_settings = tk.Button(root, text="Serial Port Settings", command=lambda :KK_Lab2_UART_TAB.com_port_settings(root),padx=80,pady=10,width=4, height=1,font=globals.myFontMain)
myButton_open_port = tk.Button(root, text="Open port", command=lambda :Func.COM_port_Open_Close(myButton_open_port))

myButton_quit.grid(row=3, column=3)
myButton_port_settings.grid(row=3, column=0)
myButton_open_port.grid(row=3, column=1)


tk.mainloop()
        