import tkinter as tk
import tkinter.messagebox as messagebox
import tkintermapview
import matplotlib
import numpy as np
from numpy.lib import recfunctions as rfn

import KK_Lab2_GLOBALS as globals


def COM_port_Open_Close(button,label,root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH,MAP,LAT_VALUE,LON_VALUE):
    if globals.Port_connected == False:
        try:
            globals.serialPort.baudrate = globals.selected_baud_rate
            globals.serialPort.port = globals.selected_port
            globals.serialPort.parity = globals.parity_option_dict.get(globals.selected_parity)
            globals.serialPort.stopbits = int(globals.selected_stop_bits)
            globals.serialPort.bytesize = int(globals.selected_data_bits)
            globals.serialPort.timeout = 0.01 #10 ms
            
            globals.serialPort.close()
            globals.serialPort.open()
            button['text'] = "Close port"
            label['background'] = "green"
            label['text'] = "OPEN"
            globals.Port_connected = True
            root.after(10, lambda:COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH,MAP,LAT_VALUE,LON_VALUE))#start reading
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
            LAT_VALUE['text'] = "--"
            LON_VALUE['text'] = "--"
            globals.Port_connected = False
        except Exception as e:
            messagebox.showerror("ERROR", f"Port can't be closed: {e}")
            

def GUI_Exit(root):
    exit_msg = messagebox.askyesno("WARNING", "Are you sure you want to exit?",icon='warning')
    if exit_msg:
        root.destroy()
        
def COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH,MAP,LAT_VALUE,LON_VALUE):
    if globals.Port_connected:
        if globals.serialPort.in_waiting:
            try:
                data = globals.serialPort.readline()
                if data:
                    string_data = data.decode('ascii')
                    com_port_log_data(string_data,textbox)
                    com_port_display_data(string_data,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH,MAP,LAT_VALUE,LON_VALUE)
            except Exception as e:
                log_msg = f"Error reading data: {e}\n"
                com_port_log_data(log_msg,textbox)
        root.after(10, lambda: COM_port_read_data(root,textbox,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,GRAPH,MAP,LAT_VALUE,LON_VALUE))#blocking every 10 ms while port open
    else: root.after_cancel(COM_port_read_data)
      
def com_port_log_clear(textbox,temp_graph,press_graph,canvas,map):#clear logs,graph and index
    
    textbox['state'] = 'normal'
    textbox.delete(1.0, tk.END)
    textbox['state'] = 'disabled'
    globals.Clearing_logs = True
    globals.myGraphIndex = 0
    globals.Index_gps = 0
    globals.Press_array = []
    globals.Temp_array = []
    globals.myGraphIndexArraySensor = []
    globals.myGraphIndexArrayGPS = []
    globals.Lat_array = []
    globals.Lon_array = []
    globals.Time_array = []
    map.delete_all_marker()
    globals.Clearing_logs = False
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
    
def com_port_display_data(data,fix,time,satellites,HDOP,TEMP_AXIS,PRESS_AXIS,CANVAS,MAP,LAT_VALUE,LON_VALUE):
    if data.startswith("$PNLBLPS"):
        #command, pressure 1.1f, tempeature 1.1f, checksum
        splitted_data = data.split(',')
        pressure = float(splitted_data[1])
        temperature = float(splitted_data[2])
        checksum = splitted_data[3].strip() #remove \r\n end
        
        globals.Temp_array.append(temperature)
        globals.Press_array.append(pressure)
        globals.myGraphIndexArraySensor.append(globals.myGraphIndex)
        
        globals.Temp_array = globals.Temp_array[-(3*globals.GRAPH_SHIFT_SIZE):]
        globals.Press_array = globals.Press_array[-(3*globals.GRAPH_SHIFT_SIZE):]
        globals.myGraphIndexArraySensor = globals.myGraphIndexArraySensor[-(3*globals.GRAPH_SHIFT_SIZE):]
        
        TEMP_AXIS.set_data(globals.myGraphIndexArraySensor,globals.Temp_array)
        PRESS_AXIS.set_data(globals.myGraphIndexArraySensor,globals.Press_array)
        
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
        
        globals.Lat_array.append(float(latitude) if NS == 'N' else -float(latitude))
        globals.Lon_array.append(float(longtitude) if EW == 'E' else -float(longtitude))
        globals.Time_array.append(EET_summer)
        globals.myGraphIndexArrayGPS.append(globals.Index_gps)
        
        globals.Time_array = globals.Time_array[-globals.GRAPH_SHIFT_SIZE:]
        globals.Lat_array = globals.Lat_array[-globals.GRAPH_SHIFT_SIZE:]
        globals.Lon_array = globals.Lon_array[-globals.GRAPH_SHIFT_SIZE:]
        globals.myGraphIndexArrayGPS = globals.myGraphIndexArrayGPS[-globals.GRAPH_SHIFT_SIZE:]
        
        if globals.Clearing_logs == False:
            MAP.set_marker(float(latitude),float(longtitude))
        fix['background'] = "green" if int(GNSS_fix) == 1 else "red"
        time['text'] = EET_summer[0:2]+':'+EET_summer[2:4]+':'+EET_summer[4:6]
        satellites['text'] = satellite_count
        HDOP['text'] = HDOP_var
        LAT_VALUE['text'] = f"{float(latitude) if NS == 'N' else -float(latitude):.5f}"
        LON_VALUE['text'] = f"{float(longtitude) if EW == 'E' else -float(longtitude):.5f}"
        globals.Index_gps +=1
        
        
def Save_plot_data():
    if len(globals.Press_array) > 0 and len(globals.Time_array) > 0:# GPS and LPS data not empty
        try:
            #format a big array
            data1 = rfn.merge_arrays((np.array(globals.myGraphIndexArraySensor), np.array(globals.Temp_array), np.array(globals.Press_array)))
            np.savetxt('KK_Lab2_Data_Sensor.txt', data1, fmt=["%d","%.1f","%.1f"], delimiter=',',header="Index,Temperature,Pressure")
            data2 = rfn.merge_arrays((np.array(globals.myGraphIndexArrayGPS),np.array(globals.Time_array), np.array(globals.Lat_array), np.array(globals.Lon_array)))
            np.savetxt('KK_Lab2_Data_GPS.txt', data2, fmt=["%d","%s","%.5f","%.5f"], delimiter=',',header="Index,Time(EET),Latitude,Longitude")
            messagebox.showinfo("INFO", "Data saved to KK_Lab2_Data_Sensor.txt and KK_Lab2_Data_GPS.txt")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error saving data: {e}")
    else:
        messagebox.showwarning("WARNING", "No data to save.")