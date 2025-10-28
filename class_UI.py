#main packages
import tkinter as tk
import tkintermapview
import tkinter.messagebox as messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

import serial
import serial.tools.list_ports
from collections import deque

import numpy as np
from numpy.lib import recfunctions as rfn

import mysql.connector
#my packages
from class_data_logging import *
import class_constants as consts
import class_UART_tab
import class_SQL_tab

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        print("Init App")
        self.title("KK lab sensor data logger")
        self.geometry("{}x{}+{}+{}".format(consts.MAIN_WINDOW_WIDTH, consts.MAIN_WINDOW_HEIGHT, 200, 15))
        self.iconbitmap("icon.ico")
        self.resizable(False, False)
        self.attributes("-topmost", False)
        #global variables
        self.Port_connected = False
        self.Clearing_logs = False
        self.serialPort  = serial.Serial()
        #global for UART settings
        self.selected_port = " "
        self.selected_baud_rate = 9600
        self.selected_parity = "None"
        self.selected_stop_bits = 1
        self.selected_data_bits = 8

        self.myGraphIndex = 0 #index for graph values
        self.Index_gps = 0
        self.subindex_time = 0#for linking MySQL values of sensors and GNSS module
        self.myGraphIndexArraySensor = []
        self.myGraphIndexArrayGPS = []
        self.markers = deque()#for popping, it is a FIFO register

        self.Temp_array = []
        self.Press_array = []
        self.Time_array = []
        self.Lat_array = []
        self.Lon_array = []
        
        self.BEFORE_ID_VALUE = 0
        self.LAST_ID_VALUE = 0
    
    def create_widgets(self):        
        #graph matlab
        px = 1/matplotlib.rcParams['figure.dpi']  # pixel in inches
        self.matlab_figure = Figure(dpi=100,tight_layout=True,figsize=(consts.WIDTH_RIGHT_FRAME*px,consts.HEIGHT_RIGHT_FRAME/2*px))
        
        self.myFrame_right_side = tk.Frame(self,height=consts.HEIGHT_RIGHT_FRAME,width=consts.WIDTH_RIGHT_FRAME)
        self.myFrame_right_bottom = tk.Frame(self.myFrame_right_side,background='blue',bg='blue',height=consts.HEIGHT_RIGHT_FRAME/2,width=consts.WIDTH_RIGHT_FRAME)
        self.myCanvas = FigureCanvasTkAgg(self.matlab_figure, master=self.myFrame_right_side)

        self.myButton_exit = tk.Button(self, text="Exit",width=8,command = lambda : self.App_exit(), height=1,font=consts.MYFONTMAIN)
        self.myButton_port_settings = tk.Button(self, text="Serial Port Settings",font=consts.MYFONTMID
                                                ,command=lambda :self.Open_UART_Settings(),width=20, height=2,)
        self.myButton_clear_logs = tk.Button(self, text="Clear data",width=8, height=1,
                                        font=consts.MYFONTMAIN,command= lambda : self.COM_Port_Clear_Logs())
        self.myButton_save_data = tk.Button(self, text="Save data",width=8, height=1,
                                        font=consts.MYFONTMAIN, command=lambda : Save_Buffer_Data(self))
        self.myText_COM_logs = tk.Text(self, height=10, width=53, font=consts.MYFONTMAIN, state='disabled')

        self.myLabel_COM_status = tk.Label(self, background="red",padx=35, font=consts.MYFONTMID,width=9)
        self.myLabel_FIX = tk.Label(self, text="GNSS FIX STATUS", font=consts.MYFONTBIGGEST)
        self.myLabel_FIX_status = tk.Label(self, background="red",padx=5, font=consts.MYFONTMAIN,width=3)

        self.myLabel_time = tk.Label(self, text="Time(EET):", font=consts.MYFONTBIGGEST)
        self.myLabel_time_value = tk.Label(self, text="--:--:--", font=consts.MYFONTBIGGEST,anchor='w',justify="left")

        self.myLabel_Lat = tk.Label(self, text="Latitude:", font=consts.MYFONTMID)
        self.myLabel_Lat_value = tk.Label(self, text="--", font=consts.MYFONTMID,anchor='w',justify="left")

        self.myLabel_Lon = tk.Label(self, text="Longitude:", font=consts.MYFONTMID)
        self.myLabel_Lon_value = tk.Label(self, text="--", font=consts.MYFONTMID,anchor='w',justify="left")

        self.myLabel_sattelites = tk.Label(self, text="Satellites:", font=consts.MYFONTMID)
        self.myLabel_sattelites_value = tk.Label(self, text="--", font=consts.MYFONTMID,anchor='w',justify="left")

        self.myLabel_HDOP = tk.Label(self, text="HDOP:", font=consts.MYFONTMID)
        self.myLabel_HDOP_value = tk.Label(self, text="--", font=consts.MYFONTMID,anchor='w',justify="left")
        
        #right side gui
        self.myToolbar = NavigationToolbar2Tk(self.myCanvas, self.myFrame_right_side,pack_toolbar=False)
        self.myCanvas.draw()
        self.myToolbar.update()

        self.myMapWidget = tkintermapview.TkinterMapView(self.myFrame_right_bottom, width=consts.WIDTH_RIGHT_FRAME, height=consts.HEIGHT_RIGHT_FRAME/2,)
        self.myMapWidget.set_position(54.90396923101469, 23.957806638243493) #KTU 11 rumai
        self.myMapWidget.set_zoom(12)
        tile_server_url = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        self.myMapWidget.set_tile_server(tile_server_url,max_zoom = 17)
        #light map for faster response and less max zoom

        self.myButton_open_port = tk.Button(self, text="Open port",font=("Times New Roman", 13),padx=40,width=10, height=1
                                            ,command=lambda : self.COM_Port_Open_Close())
        
        #widget for SQL settings
        self.myButton_SQL_settings = tk.Button(self, text="Database Viewer",font=consts.MYFONTMID, command = lambda : self.Open_SQL_Settings(),padx=45)
        self.mySQL_open_status = tk.Label(self, background="red", font=consts.MYFONTMID,padx=8)
        
        self.var = tk.IntVar()
        self.mySQL_start_record = tk.Checkbutton(self, text="Record to MySQL", font=consts.MYFONTMID,variable=self.var)
      
      
    def Open_UART_Settings(self):
        uart_settings_window = class_UART_tab.Application_UART_Settings(self)

        
    def Open_SQL_Settings(self):
        #test if it was able to connect to DB at start
        if(self.mySQL_open_status['background'] == "red"):
            messagebox.showerror("ERROR","DB wasn't accesed at the start of the program, restart the program and check the warnings")
        else:
            SQL_window = class_SQL_tab.SQL_TAB(self)

    def create_layout(self):
        print("Creating layout")
        self.myButton_port_settings.grid(row=0, column=0,rowspan=3,padx=10)
        self.myLabel_COM_status.grid(row=3, column=2,padx=10)
        tk.Label(self, text="").grid(row=2, column=2)
        self.myButton_open_port.grid(row=1, column=2)
        #sql button
        self.myButton_SQL_settings.grid(row=2, column=0,rowspan=3,padx=10)
        self.mySQL_open_status.grid(row=2, column=1,rowspan=3,sticky="w",padx=10)
        self.mySQL_start_record.grid(row=9, column=2,sticky="w")
        
        self.myText_COM_logs.grid(row=5, column=0, columnspan=5,padx=10)
        self.myButton_clear_logs.grid(row=7,column=0,columnspan=2)
        self.myButton_save_data.grid(row=7,column=2,columnspan=2)
        
        self.myLabel_FIX.grid(row=9,column=0,padx=10,columnspan=2)
        self.myLabel_FIX_status.grid(row=9,column=1,padx=10,sticky="w")
        self.myLabel_time.grid(row=10,column=0,columnspan=2,padx=10)
        self.myLabel_time_value.grid(row=10,column=2,sticky="w",columnspan=3)
        self.myLabel_sattelites.grid(row=13,column=0,columnspan=2,padx=10)
        self.myLabel_sattelites_value.grid(row=13,column=2,sticky="w",columnspan=3)
        self.myLabel_HDOP.grid(row=14,column=0,columnspan=2,padx=10)
        self.myLabel_HDOP_value.grid(row=14,column=2,sticky="w",columnspan=3)
        self.myLabel_Lat.grid(row=12,column=0,padx=10,columnspan=2)
        self.myLabel_Lat_value.grid(row=12,column=2,sticky="w",columnspan=3)
        self.myLabel_Lon.grid(row=11,column=0,padx=10,columnspan=2)
        self.myLabel_Lon_value.grid(row=11,column=2,sticky="w",columnspan=3)
        
        #place frame on the right side for graphs
        self.myFrame_right_side.grid(row = 0,rowspan=15,column=5,columnspan=1)
        self.myCanvas.get_tk_widget().grid(row = 1,column=0)
        self.myToolbar.grid(row=0, column=0,sticky='W')
        self.myFrame_right_bottom.grid(row = 2,column=0)
        self.myMapWidget.grid(row = 2,column=0)
        
        #self.myButton_exit.grid(row=0,column=5,pady=10)
        
        #spacing
        tk.Label(self, text="").grid(row=0, column=0,columnspan=5)
        tk.Label(self, text="").grid(row=4, column=0,columnspan=5)
        tk.Label(self, text="").grid(row=6, column=0,columnspan=5)
        tk.Label(self, text="").grid(row=8, column=0,columnspan=5,pady=5)
        tk.Label(self, text="").grid(row=10, column=0,columnspan=5)
        tk.Label(self, text="").grid(row=12, column=0,columnspan=5)
        
    def App_exit(self):
            exit_msg = messagebox.askyesno("WARNING", "Are you sure you want to exit?",icon='warning')
            if exit_msg:
                self.destroy()
                 
    def COM_Port_Clear_Logs(self):
        self.myText_COM_logs['state'] = 'normal'
        self.myText_COM_logs.delete(1.0, tk.END)
        self.myText_COM_logs['state'] = 'disabled'
        self.Clearing_logs = True
        self.myGraphIndex = 0
        self.Index_gps = 0
        self.Press_array = []
        self.Temp_array = []
        self.myGraphIndexArraySensor = []
        self.myGraphIndexArrayGPS = []
        self.Lat_array = []
        self.Lon_array = []
        self.Time_array = []
        self.myMapWidget.delete_all_marker()
        self.Clearing_logs = False
        self.myCanvas.draw()
        if self.Port_connected:
            self.serialPort.reset_input_buffer()

    def COM_Port_Log_Data(self,data):
        self.myText_COM_logs['state'] = 'normal'
        try:
            self.myText_COM_logs.insert(tk.END, data)
        except:
            self.myText_COM_logs.insert(tk.END, data)
        self.myText_COM_logs.see(tk.END)
        self.myText_COM_logs['state'] = 'disabled'
      
    def COM_Port_Open_Close(self):
        if self.Port_connected == False:
            try:
                self.serialPort.baudrate = self.selected_baud_rate
                self.serialPort.port = self.selected_port
                self.serialPort.parity = consts.parity_option_dict.get(self.selected_parity)
                self.serialPort.stopbits = int(self.selected_stop_bits)
                self.serialPort.bytesize = int(self.selected_data_bits)
                self.serialPort.timeout = 0.01 #10 ms
                
                self.serialPort.close()
                self.serialPort.open()
                self.myButton_open_port['text'] = "Close port"
                self.myLabel_COM_status['background'] = "green"
                self.myLabel_COM_status['text'] = "OPEN"
                self.Port_connected = True
                self.after(10, lambda:self.COM_Port_Read_Raw_Data())#start reading
            except Exception as e:
                tk.messagebox.showerror("ERROR", f"Port can't be opened: {e}")
                self.myLabel_COM_status['background'] = "red"
                self.myLabel_COM_status['text'] = "CLOSED"
        else:
            try:
                self.after_cancel(self.COM_Port_Read_Raw_Data)
                self.serialPort.close()
                self.myButton_open_port['text'] = "Open port"
                self.myLabel_COM_status['background'] = "red"
                self.myLabel_COM_status['text'] = "CLOSED"
                self.myLabel_FIX_status['background'] = "red"
                self.myLabel_time_value['text'] = "--:--:--"
                self.myLabel_sattelites_value['text'] = "--"
                self.myLabel_HDOP_value['text'] = "--"
                self.myLabel_Lat_value['text'] = "--"
                self.myLabel_Lon_value['text'] = "--"
                self.Port_connected = False
            except Exception as e:
                messagebox.showerror("ERROR", f"Port can't be closed: {e}")
      
    def COM_Port_Parse_LPS22HB(self,data):
        #command, pressure 1.1f, tempeature 1.1f, checksum
        splitted_data = data.split(',')
        pressure = float(splitted_data[1])
        temperature = float(splitted_data[2])
        checksum = splitted_data[3].strip() #remove \r\n end
        
        SENSOR_DISPLAY_UPDATE(self,temperature,pressure)
        if self.var.get() == 1:#check button for recording to MySQL ID is foreign key of GNSS module (need to take last value of it)
            
            query = f"""SELECT ID FROM {consts.table_names[1]}
ORDER BY ID DESC
LIMIT 1"""
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute(query)
            self.LAST_ID_VALUE = list(cursor.fetchone())[0]#convert from tuple to list to first index value
            if(self.BEFORE_ID_VALUE != self.LAST_ID_VALUE):
                self.subindex_time=0
            
            SQL_data = {'ID' : consts.table_names[0],
                        'GPS_ID' : self.LAST_ID_VALUE,
                        'subindex' : self.subindex_time,
                        'temp' : temperature,
                        'pressure' : pressure}
            DB_Add_Data(self,SQL_data)
            
        self.subindex_time +=1
        self.subindex_time %=3
        #self.subindex_time %=3#0th is same time as GNSS, otherwise 0.33 0.66 seconds
        self.BEFORE_ID_VALUE = self.LAST_ID_VALUE
        
    def COM_Port_Parse_GPS(self,data):
        #fix,latitude(DMS),NS,longtitude(DMS),EW,UTC+3,satellites,HDOP,checksum
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
        
        self.Lat_array.append(float(latitude) if NS == 'N' else -float(latitude))
        self.Lon_array.append(float(longtitude) if EW == 'E' else -float(longtitude))
        self.Time_array.append(EET_summer)
        self.myGraphIndexArrayGPS.append(self.Index_gps)
        
        self.Time_array = self.Time_array[-consts.GRAPH_SHIFT_SIZE:]
        self.Lat_array = self.Lat_array[-consts.GRAPH_SHIFT_SIZE:]
        self.Lon_array = self.Lon_array[-consts.GRAPH_SHIFT_SIZE:]
        self.myGraphIndexArrayGPS = self.myGraphIndexArrayGPS[-consts.GRAPH_SHIFT_SIZE:]
        
        COM_PORT_DISPLAY_UPDATE_GPS(self,GNSS_fix,latitude,NS,longtitude,EW,EET_summer,satellite_count,HDOP_var)
        if self.var.get() == 1:#check button for recording to MySQL
            SQL_data = {'ID' : consts.table_names[1],
                    'FIX' : GNSS_fix,
                    'LAT' : latitude,
                    'NS' : NS,
                    'LONG' : longtitude,
                    'EW' : EW,
                    'TIME' : EET_summer,
                    'SATELL' : satellite_count,
                    'HDOP' : HDOP_var}
            DB_Add_Data(self,SQL_data)
        
        self.Index_gps +=1
      
      
    def COM_Port_Parse(self,data):
        if data.startswith("$PNLBLPS"):
            self.COM_Port_Parse_LPS22HB(data)
        elif data.startswith("$PNLBGPS"):
            self.COM_Port_Parse_GPS(data)
      
    def COM_Port_Read_Raw_Data(self):
            if self.Port_connected:
                if self.serialPort.in_waiting:
                    try:
                        data = self.serialPort.readline()
                        if data:
                            string_data = data.decode('ascii')
                            self.COM_Port_Log_Data(string_data)
                            self.COM_Port_Parse(string_data)
                    except Exception as e:
                        log_msg = f"Error reading data: {e}\n"
                        self.COM_Port_Log_Data(log_msg)
                self.after_id = self.after(10,self.COM_Port_Read_Raw_Data)#blocking every 10 ms while port open
            else: self.after_cancel(self.after_id)
      
    def configure_matlab(self):
        self.myGraphPressureAx = self.matlab_figure.add_subplot(212)
        self.myGraphTempAx = self.matlab_figure.add_subplot(211)

        self.myGraphTemp, = self.myGraphTempAx.plot([],[])
        self.myGraphPres, = self.myGraphPressureAx.plot([],[])
        
        matplotlib.rcParams.update({'axes.titlesize':12, 'figure.titlesize':18})
        self.matlab_figure.suptitle('LPS22HB data')
        self.myGraphTempAx.set_title('Temperature graph')
        self.myGraphPressureAx.set_title('Pressure graph')
        self.myGraphTempAx.set_ylabel(r"Temperature, $\degree$C")
        self.myGraphPressureAx.set_ylabel("Pressure, hPa")
        self.myGraphTempAx.set_xlabel("Samples")
        self.myGraphTempAx.grid()
        self.myGraphPressureAx.grid()
        self.myGraphPressureAx.set_xlabel("Samples")
        self.myGraphTempAx.ticklabel_format(style='plain',useOffset=False)
        self.myGraphPressureAx.ticklabel_format(style='plain',useOffset=False)
        self.myGraphPressureAx.set_xlim(auto=True)
        self.myGraphTempAx.set_xlim(auto=True)