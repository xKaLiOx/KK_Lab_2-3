import tkinter as tk
import tkinter.messagebox as messagebox

import KK_Lab2_GLOBALS as globals
#import KK_Lab2_GUI

def COM_port_Open_Close(button):
    if globals.Port_connected == False:
        try:
            globals.serialPort.baudrate = globals.selected_baud_rate
            globals.serialPort.port = globals.selected_port
            globals.serialPort.parity = globals.parity_option_dict.get(globals.selected_parity)
            globals.serialPort.stopbits = int(globals.selected_stop_bits)
            globals.serialPort.bytesize = int(globals.selected_data_bits)
            globals.serialPort.open()
            button['text'] = "Close port"
            globals.Port_connected = True
        except Exception as e:
            tk.messagebox.showerror("Error", f"Port can't be opened: {e}")
    else:
        try:
            globals.serialPort.close()
            button['text'] = "Open port"
            globals.Port_connected = False
        except Exception as e:
            messagebox.showerror("Error", f"Port can't be closed: {e}")
def GUI_Exit(root):
    exit_msg = messagebox.askyesno("Exit", "Are you sure you want to exit?",icon='warning')
    if exit_msg:
        root.destroy()