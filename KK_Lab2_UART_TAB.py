import tkinter as tk
from tkinter import ttk


import KK_Lab2_GLOBALS
import serial
import serial.tools.list_ports

WINDOW_HEIGHT = 350
WINDOW_WIDTH = 250

#UART settings options

port_options = []
stop_bits_options = [1, 2]
baud_rate_options = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
data_bits_options = [5, 6, 7, 8]


#function definitions

def com_port_update_settings(window,port, baud, parity, stop):

    #update globals for main GUI
    KK_Lab2_GLOBALS.selected_baud_rate = baud
    KK_Lab2_GLOBALS.selected_port = port
    KK_Lab2_GLOBALS.selected_parity = parity
    KK_Lab2_GLOBALS.selected_stop_bits = stop
    
    window.destroy()

def com_port_list_update(port_options):
    port_options = serial.tools.list_ports.comports()

def com_port_settings(root):
    
    myWindow_uart_settings = tk.Toplevel(root)
    #myWindow_uart_settings.geometry("200x600")
    myWindow_uart_settings.resizable(False, False)
    myWindow_uart_settings.title("UART settings")
    myWindow_uart_settings.iconbitmap("icon.ico")

    screen_width = myWindow_uart_settings.winfo_screenwidth()
    screen_height = myWindow_uart_settings.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (WINDOW_WIDTH/2))
    y_cordinate = int((screen_height/2) - (WINDOW_HEIGHT/2))
    myWindow_uart_settings.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
    
    #update port list
    com_port_list_update(port_options)
    
    myLabel_port_name = tk.Label(myWindow_uart_settings, text="Port name", font=KK_Lab2_GLOBALS.myFontMain,justify="center",padx=50)
    myComboBox_port_name = ttk.Combobox(myWindow_uart_settings, state='readonly',font=KK_Lab2_GLOBALS.myFontMain,width=15)
    myLabel_port_rate = tk.Label(myWindow_uart_settings, text="Baud rate", font=KK_Lab2_GLOBALS.myFontMain,justify="center",padx=50)
    myComboBox_port_rate = ttk.Combobox(myWindow_uart_settings, state='readonly',font=KK_Lab2_GLOBALS.myFontMain,width=15)
    myLabel_port_parity = tk.Label(myWindow_uart_settings, text="Parity", font=KK_Lab2_GLOBALS.myFontMain,justify="center",padx=50)
    myComboBox_port_parity = ttk.Combobox(myWindow_uart_settings, state='readonly',font=KK_Lab2_GLOBALS.myFontMain,width=15)
    myLabel_port_stop_bits = tk.Label(myWindow_uart_settings, text="Stop bits", font=KK_Lab2_GLOBALS.myFontMain,justify="center",padx=50)
    myComboBox_port_stop_bits = ttk.Combobox(myWindow_uart_settings, state='readonly',font=KK_Lab2_GLOBALS.myFontMain,width=15)
    myLabel_port_data_bits = tk.Label(myWindow_uart_settings, text="Data bits", font=KK_Lab2_GLOBALS.myFontMain,justify="center",padx=50)
    myComboBox_port_data_bits = ttk.Combobox(myWindow_uart_settings, state='readonly',font=KK_Lab2_GLOBALS.myFontMain,width=15)
    
    myButton_port_settings_apply = tk.Button(myWindow_uart_settings, text="Apply", command=lambda :com_port_update_settings(myWindow_uart_settings,myComboBox_port_name.get(),myComboBox_port_rate.get(),myComboBox_port_parity.get(),myComboBox_port_stop_bits.get()),width=4, height=1,font=KK_Lab2_GLOBALS.myFontMain)
    myButton_port_settings_cancel = tk.Button(myWindow_uart_settings, text="Cancel", command=myWindow_uart_settings.destroy,width=4, height=1,font=KK_Lab2_GLOBALS.myFontMain)
    

    myComboBox_port_name['values'] = [port.device for port in serial.tools.list_ports.comports()]
    myComboBox_port_name.set("Select COM port")
    myComboBox_port_rate['values'] = baud_rate_options
    myComboBox_port_rate.set(KK_Lab2_GLOBALS.selected_baud_rate)
    myComboBox_port_parity['values'] = list(KK_Lab2_GLOBALS.parity_option_dict.keys())
    myComboBox_port_parity.set(KK_Lab2_GLOBALS.selected_parity)
    myComboBox_port_stop_bits['values'] = stop_bits_options
    myComboBox_port_stop_bits.set(KK_Lab2_GLOBALS.selected_stop_bits)
    myComboBox_port_data_bits['values'] = data_bits_options
    myComboBox_port_data_bits.set(KK_Lab2_GLOBALS.selected_data_bits)
    
    
    myLabel_port_name.grid(padx=WINDOW_WIDTH/2-75, row=1, column=0,columnspan=2)
    myComboBox_port_name.grid(padx=WINDOW_WIDTH/2-75, row=2, column=0,columnspan=2)
    myLabel_port_rate.grid(padx=WINDOW_WIDTH/2-75, row=4, column=0,columnspan=2)
    myComboBox_port_rate.grid(padx=WINDOW_WIDTH/2-75, row=5, column=0,columnspan=2)
    myLabel_port_parity.grid(padx=WINDOW_WIDTH/2-75, row=7, column=0,columnspan=2)
    myComboBox_port_parity.grid(padx=WINDOW_WIDTH/2-75, row=8, column=0,columnspan=2)
    myLabel_port_stop_bits.grid(padx=WINDOW_WIDTH/2-75, row=10, column=0,columnspan=2)
    myComboBox_port_stop_bits.grid(padx=WINDOW_WIDTH/2-75, row=11, column=0,columnspan=2)

    #add spacing between comboboxes and buttons
    tk.Label(myWindow_uart_settings, text="",justify="center").grid(row=3, column=0)
    tk.Label(myWindow_uart_settings, text="",justify="center").grid(row=6, column=0)
    tk.Label(myWindow_uart_settings, text="",justify="center").grid(row=9, column=0)
    tk.Label(myWindow_uart_settings, text="",justify="center").grid(row=12, column=0)
    
    myButton_port_settings_apply.grid(row=13, column=0,ipadx=20)
    myButton_port_settings_cancel.grid(row=13, column=1,ipadx=20)