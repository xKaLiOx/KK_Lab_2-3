import tkinter as tk
import tkinter.messagebox as messagebox

import KK_Lab2_GLOBALS as globals

def COM_port_Open_Close(button,label,root,textbox):
    if globals.Port_connected == False:
        try:
            globals.serialPort.baudrate = globals.selected_baud_rate
            globals.serialPort.port = globals.selected_port
            globals.serialPort.parity = globals.parity_option_dict.get(globals.selected_parity)
            globals.serialPort.stopbits = int(globals.selected_stop_bits)
            globals.serialPort.bytesize = int(globals.selected_data_bits)
            globals.serialPort.timeout = 0.01 #in seconds
            
            globals.serialPort.close()
            globals.serialPort.open()
            button['text'] = "Close port"
            label['background'] = "green"
            globals.Port_connected = True
            root.after(10, lambda:COM_port_parse_data(root,textbox))#start reading
        except Exception as e:
            tk.messagebox.showerror("ERROR", f"Port can't be opened: {e}")
            label['background'] = "red"
    else:
        try:
            globals.serialPort.close()
            button['text'] = "Open port"
            label['background'] = "red"
            globals.Port_connected = False
        except Exception as e:
            messagebox.showerror("ERROR", f"Port can't be closed: {e}")
            

def GUI_Exit(root):
    exit_msg = messagebox.askyesno("WARNING", "Are you sure you want to exit?",icon='warning')
    if exit_msg:
        root.destroy()
        
def COM_port_parse_data(root,textbox):
    if globals.serialPort.in_waiting:
        try:
            data = globals.serialPort.readline()
            if data:
                com_port_log_data(data,textbox)
        except Exception as e:
            log_msg = f"Error reading data: {e}\n"
            com_port_log_data(log_msg,textbox)
    
    
    if globals.Port_connected:
        root.after(10, lambda: COM_port_parse_data(root,textbox))#blocking every 10 ms while port open
        
def GUI_log_clear(textbox):
    textbox['state'] = 'normal'
    textbox.delete(1.0, tk.END)
    textbox['state'] = 'disabled'
    
def com_port_log_data(data,textbox):
    textbox['state'] = 'normal'
    try:
        textbox.insert(tk.END, data.decode('utf-8'))
    except:
        textbox.insert(tk.END, data)
    textbox.see(tk.END)
    textbox['state'] = 'disabled'