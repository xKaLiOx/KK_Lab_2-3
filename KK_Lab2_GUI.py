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

myButton_quit = tk.Button(root, text="Exit", command=lambda : Func.GUI_Exit(root),width=8, height=1,font=globals.myFontMain)
myButton_port_settings = tk.Button(root, text="Serial Port Settings",width=15, height=1, command=lambda :KK_Lab2_UART_TAB.com_port_settings(root),font=globals.myFontMain)
myButton_open_port = tk.Button(root, text="Open port",width=10, height=1, command=lambda :Func.COM_port_Open_Close(myButton_open_port,myLabel_COM_status,root,myText_COM_logs))

myText_COM_logs = tk.Text(root, height=20, width=60, font=globals.myFontMain, state='disabled')
myLabel_COM_status = tk.Label(root, background="red")
myButton_clear_Label = tk.Button(root, text="Clear data",width=8, height=1, command=lambda : Func.GUI_log_clear(myText_COM_logs),font=globals.myFontMain)

tk.Label(root, text="").grid(row=0, column=0, sticky="n",columnspan=10)
tk.Label(root, text="").grid(row=3, column=0, sticky="n",columnspan=5)
tk.Label(root, text="").grid(row=5, column=0, sticky="n",columnspan=5)

myButton_port_settings.grid(row=1, column=0)
myButton_open_port.grid(row=1, column=1,columnspan=3)

myButton_quit.grid(row=6, column=8)

myLabel_COM_status.grid(row=2, column=2, sticky="ew")
myText_COM_logs.grid(row=4, column=0, columnspan=5,padx=10)
myButton_clear_Label.grid(row=6,column=0,columnspan=5)

tk.mainloop()
        