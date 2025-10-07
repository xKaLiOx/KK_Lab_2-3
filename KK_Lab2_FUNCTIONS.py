import tkinter as tk
import tkinter.messagebox as messagebox
import matplotlib
import numpy as np

import KK_Lab2_GLOBALS as globals


def COM_port_Open_Close(button,label,root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH):
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
            label['text'] = "OPEN"
            globals.Port_connected = True
            root.after(10, lambda:COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH))#start reading
        except Exception as e:
            tk.messagebox.showerror("ERROR", f"Port can't be opened: {e}")
            label['background'] = "red"
            label['text'] = "CLOSED"
    else:
        try:
            root.after_cancel(COM_port_read_data)
            globals.serialPort.close()
            button['text'] = "Open port"
            label['background'] = "red"
            label['text'] = "CLOSED"
            fix['background'] = "red"
            time['text'] = "--:--:--"
            satellites['text'] = "--"
            HDOP['text'] = "--"
            globals.Port_connected = False
        except Exception as e:
            messagebox.showerror("ERROR", f"Port can't be closed: {e}")
            

def GUI_Exit(root):
    exit_msg = messagebox.askyesno("WARNING", "Are you sure you want to exit?",icon='warning')
    if exit_msg:
        root.destroy()
        
def COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH):
    if globals.Port_connected:
        if globals.serialPort.in_waiting:
            try:
                data = globals.serialPort.readline()
                if data:
                    string_data = data.decode('ascii')
                    com_port_log_data(string_data,textbox)
                    com_port_display_data(string_data,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH)
            except Exception as e:
                log_msg = f"Error reading data: {e}\n"
                com_port_log_data(log_msg,textbox)
        root.after(10, lambda: COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH))#blocking every 10 ms while port open
    else: root.after_cancel(COM_port_read_data)
      
def com_port_log_clear(textbox,temp_graph,press_graph,canvas):#clear logs,graph and index
    textbox['state'] = 'normal'
    textbox.delete(1.0, tk.END)
    textbox['state'] = 'disabled'
    globals.myGraphIndex = 0
    globals.Press_array = []
    globals.Temp_array = []
    globals.myGraphIndexArray = []
    temp_graph.clear()
    press_graph.clear()
    canvas.draw()
    globals.serialPort.reset_input_buffer()
    
    
def com_port_log_data(data,textbox):
    textbox['state'] = 'normal'
    try:
        textbox.insert(tk.END, data)
    except:
        textbox.insert(tk.END, data)
    textbox.see(tk.END)
    textbox['state'] = 'disabled'
    
def com_port_display_data(data,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,CANVAS):
    if data.startswith("$PNLBLPS"):
        #command, pressure 1.1f, tempeature 1.1f, checksum
        splitted_data = data.split(',')
        pressure = float(splitted_data[1])
        temperature = float(splitted_data[2])
        checksum = splitted_data[3].strip() #remove \r\n end
        
        globals.Temp_array.append(temperature)
        globals.Press_array.append(pressure)
        globals.myGraphIndexArray.append(globals.myGraphIndex)
        
        globals.Temp_array = globals.Temp_array[-globals.Graph_shift_size:]
        globals.Press_array = globals.Press_array[-globals.Graph_shift_size:]
        globals.myGraphIndexArray = globals.myGraphIndexArray[-globals.Graph_shift_size:]
        
        TEMP_AXIS.set_data(globals.myGraphIndexArray,globals.Temp_array)
        PRESS_AXIS.set_data(globals.myGraphIndexArray,globals.Press_array)
        
        TEMP_AXIS.axes.relim(); TEMP_AXIS.axes.autoscale_view()
        PRESS_AXIS.axes.relim(); PRESS_AXIS.axes.autoscale_view()
        globals.myGraphIndex +=1
        CANVAS.draw_idle()
        
        
    #fix,latitude(DMS),NS,longtitude(DMS),EW,UTC+3,satellites,HDOP,checksum
    elif data.startswith("$PNLBGPS"):
        splitted_data = data.split(',')
        GNSS_fix = splitted_data[1]
        latitude = splitted_data[2]
        NS = splitted_data[3]
        longtitude = splitted_data[4]
        EW = splitted_data[5]
        EET_summer = splitted_data[6]
        satellite_count = splitted_data[7]
        HDOP_var = splitted_data[8]
        checksum = splitted_data[9].split()#remove \r\n end
        
        fix['background'] = "green" if int(GNSS_fix) == 1 else "red"
        time['text'] = EET_summer[0:2]+':'+EET_summer[2:4]+':'+EET_summer[4:6]
        satellites['text'] = satellite_count
        HDOP['text'] = HDOP_var