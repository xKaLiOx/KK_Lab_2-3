import tkinter as tk
from tkinter import ttk, NS, Canvas, Scrollbar, messagebox
import mysql.connector
import numpy as np

import class_constants as consts
from class_data_logging import saveExcel
from config import config


class SQL_TAB(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Database Viewer")
        self.root = root
        self.resizable(False, False)
        self.iconbitmap("icon.ico")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (consts.SQL_WINDOW_WIDTH/2))
        y_cordinate = int((screen_height/2) - (consts.SQL_WINDOW_HEIGHT/2))
        self.geometry("{}x{}+{}+{}".format(consts.SQL_WINDOW_WIDTH,
                      consts.SQL_WINDOW_HEIGHT, x_cordinate, y_cordinate))

        self.create_widgets()
        self.Database_get_date_values()
        self.Database_get_hour_values()
        self.Database_set_headers()
        self.create_layout()

    def create_widgets(self):

        self.myLabel_Date_select = ttk.Label(
            self, text="Select date", font=consts.MYFONTMID)
        self.myComboBox_Date_Select = ttk.Combobox(
            self, state='readonly', font=consts.MYFONTMAIN, width=15)
        self.myComboBox_Date_Select.bind("<<ComboboxSelected>>", self.Database_get_hour_values)
        
        self.myLabel_Time_from = ttk.Label(
            self, text="From(hour)", font=consts.MYFONTMID)
        self.myLabel_Time_to = ttk.Label(
            self, text="To(hour)", font=consts.MYFONTMID)
        self.myComboBox_Time_from = ttk.Combobox(
            self, state='readonly', font=consts.MYFONTMAIN, width=15)
        self.myComboBox_Time_to = ttk.Combobox(
            self, state='readonly', font=consts.MYFONTMAIN, width=15)
        
        self.myButton_Data_get = tk.Button(
            self, text="Select", font=consts.MYFONTBIGGEST, command=lambda: self.Database_GPS_get_values())
        self.myButton_Save_data = tk.Button(self,text="Save",font=consts.MYFONTBIGGEST,command=lambda:saveExcel(self))

        self.myCanvasGPS = tk.Canvas(self, width=600)
        self.frame_GPS = ttk.Frame(self.myCanvasGPS)
        self.frame_GPS.grid_rowconfigure(0, weight=1)
        self.frame_GPS.grid_columnconfigure(0, weight=1)
        
        self.myCanvasSENSOR = tk.Canvas(self, width=600)
        self.frame_SENSOR = ttk.Frame(self.myCanvasSENSOR)
        self.frame_SENSOR.grid_rowconfigure(0, weight=1)
        self.frame_SENSOR.grid_columnconfigure(0, weight=1)

        self.myTreeViewGPS = ttk.Treeview(
            self.frame_GPS, selectmode="browse")
        self.y_scrollbarGPS = ttk.Scrollbar(
            self.frame_GPS, orient='vertical', command=self.myTreeViewGPS.yview)
    
        self.myTreeViewSENSOR = ttk.Treeview(
            self.frame_SENSOR, selectmode="browse")
        self.y_scrollbarSENSOR = ttk.Scrollbar(
            self.frame_SENSOR, orient='vertical', command=self.myTreeViewSENSOR.yview)

    def create_layout(self):
        self.grid_columnconfigure(0, minsize=20)
        self.grid_rowconfigure(0, minsize=20)
        self.grid_columnconfigure(2, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(4, minsize=20)

        self.myLabel_Date_select.grid(row=1, column=1)
        self.myComboBox_Date_Select.grid(row=1, column=3)
        self.myButton_Data_get.grid(row=1, rowspan=5, column=5)
        self.myButton_Save_data.grid(row=1,rowspan=5,column=6)

        self.myLabel_Time_from.grid(row=3, column=1)
        self.myComboBox_Time_from.grid(row=3,column=3)
        
        self.myLabel_Time_to.grid(row=5, column=1)
        self.myComboBox_Time_to.grid(row=5,column=3)
        
        
        # draw on canvas
        self.myCanvasGPS.grid(row=7, column=1,columnspan=10,sticky="nw")
        self.grid_rowconfigure(6, minsize=20)
        self.grid_rowconfigure(8, minsize=20)
        self.myCanvasSENSOR.grid(row=9, column=1,columnspan=10,sticky="nw")

        self.frame_GPS.grid(row=0, column=0, sticky="nsew")
        self.frame_SENSOR.grid(row=0, column=0, sticky="nsew")
        
        self.myTreeViewGPS.grid(row=0, column=0, sticky="nsew")
        self.y_scrollbarGPS.grid(row=0, column=1, sticky="ns")
        self.myTreeViewSENSOR.grid(row=0, column=0, sticky="ew")
        self.y_scrollbarSENSOR.grid(row=0, column=1, sticky="ns")

    def Database_get_date_values(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        # get all time values and list in the combobox also show all the column names
        data_query = f"""SELECT DISTINCT YR_MONTH_DAY from {consts.table_names[1]}
WHERE YR_MONTH_DAY IS NOT NULL"""
        cursor.execute(data_query)
        # its a list of tuples, convert to list and get values
        Values = cursor.fetchall()
        Values_date = np.array(Values).flatten().tolist()
        if (len(Values_date) > 0):
            self.myComboBox_Date_Select.set(Values_date[-1])
            self.myComboBox_Date_Select['values'] = Values_date
        
        cursor.close()
        connection.close()

    def Database_set_headers(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        #set sensor headers
        data_query = f"DESC {consts.table_names[1]}"
        cursor.execute(data_query)
        # its a list of tuples, convert to list and get values
        Values = cursor.fetchall()
        Header_list = []
        for x in Values:
            Header_list.append(x[0])
        self.myTreeViewGPS['columns'] = Header_list
        self.myTreeViewGPS.column("#0", width=0, stretch=tk.NO)
        for x in Header_list:
            self.myTreeViewGPS.column(x, width=100)
            self.myTreeViewGPS.heading(column=x, text=x)
        self.myTreeViewGPS.column(1, width=35)
        self.myTreeViewGPS.column(3, width=35)
        self.myTreeViewGPS.column(5, width=35)
        self.myTreeViewGPS.column(8, width=35)
        self.myTreeViewGPS.column(9, width=45)
        
        "---------------------"
        #set sensor headers
        data_query = f"DESC {consts.table_names[0]}"
        cursor.execute(data_query)
        # its a list of tuples, convert to list and get values
        Values = cursor.fetchall()
        Header_list = []
        for x in Values:
            Header_list.append(x[0])
        self.myTreeViewSENSOR['columns'] = Header_list
        self.myTreeViewSENSOR.column("#0", width=0, stretch=tk.NO)
        for x in Header_list:
            self.myTreeViewSENSOR.column(x, width=100)
            self.myTreeViewSENSOR.heading(column=x, text=x)
        
        cursor.close()
        connection.close()

    def Database_GPS_get_values(self):
        # clear before values
        self.myTreeViewGPS.delete(*self.myTreeViewGPS.get_children())

        "data from GPS table"
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        if int(self.myComboBox_Time_from.get()) <= int(self.myComboBox_Time_to.get()):
            data_query = f"""
    SELECT * FROM {consts.table_names[1]}
    WHERE YR_MONTH_DAY = "{self.myComboBox_Date_Select.get()}" AND HOUR(TIME) BETWEEN {int(self.myComboBox_Time_from.get())} AND {int(self.myComboBox_Time_to.get())}
    ORDER BY ID ASC
            """
            cursor.execute(data_query)
            values = cursor.fetchall()
            for x in values:
                self.myTreeViewGPS.insert(
                    '', 'end', iid=x[0], text=x[0], values=list(x))
            cursor.close()
            connection.close()
            #link GPS values to sensor
            self.Database_SENSOR_get_values()
        else:
            messagebox.showerror("ERROR","Incorrect hour range")
            self.lift()
            
    def Database_SENSOR_get_values(self):
        try:
            self.myTreeViewSENSOR.delete(*self.myTreeViewSENSOR.get_children())

            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            
            data_query = f"""
    SELECT {consts.table_names[0]}.*
    FROM {consts.table_names[0]}
    INNER JOIN {consts.table_names[1]} ON {consts.table_names[0]}.GPS_ID = {consts.table_names[1]}.ID
    WHERE {consts.table_names[1]}.YR_MONTH_DAY = "{self.myComboBox_Date_Select.get()}"
    ORDER BY {consts.table_names[0]}.GPS_ID ASC
            """
            cursor.execute(data_query)
            sensor_values = cursor.fetchall()
            
            for x in sensor_values:
                self.myTreeViewSENSOR.insert('', 'end', text=x[0], values=list(x))
            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("ERROR", f"Error saving data: {e}")
        
        
    def Database_get_hour_values(self,event=None):
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            data_query = f"""SELECT DISTINCT HOUR({consts.table_names[1]}.TIME) FROM {consts.table_names[1]}
    WHERE {consts.table_names[1]}.YR_MONTH_DAY = "{self.myComboBox_Date_Select.get()}" """
            cursor.execute(data_query)
            # its a list of tuples, convert to list and get values
            Values = cursor.fetchall()
            Values_date = np.array(Values).flatten().tolist()
            if (len(Values_date) > 0):
                self.myComboBox_Time_from.set(Values_date[0])
                self.myComboBox_Time_from['values'] = Values_date
                self.myComboBox_Time_to.set(Values_date[-1])
                self.myComboBox_Time_to['values'] = Values_date
                
            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("ERROR", f"Error saving data: {e}")