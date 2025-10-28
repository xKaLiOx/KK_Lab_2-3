import tkinter as tk
import numpy as np
import numpy.lib.recfunctions as rfn
from tkinter import messagebox
import class_constants as consts

from openpyxl import load_workbook
from openpyxl import Workbook

import mysql.connector
from config import *


def Save_Buffer_Data(App):
    if len(App.Press_array) > 0 and len(App.Time_array) > 0:  # GPS and LPS data not empty
        try:
            # format a big array
            data1 = rfn.merge_arrays((np.array(App.myGraphIndexArraySensor), np.array(
                App.Temp_array), np.array(App.Press_array)))
            np.savetxt('KK_Lab2_Data_Sensor.txt', data1, fmt=[
                       "%d", "%.1f", "%.1f"], delimiter=',', header="Index,Temperature,Pressure")
            data2 = rfn.merge_arrays((np.array(App.myGraphIndexArrayGPS), np.array(
                App.Time_array), np.array(App.Lat_array), np.array(App.Lon_array)))
            np.savetxt('KK_Lab2_Data_GPS.txt', data2, fmt=[
                       "%d", "%s", "%.5f", "%.5f"], delimiter=',', header="Index,Time(EET),Latitude,Longitude")
            messagebox.showinfo(
                "INFO", "Data saved to KK_Lab2_Data_Sensor.txt and KK_Lab2_Data_GPS.txt")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error saving data: {e}")
    else:
        messagebox.showwarning("WARNING", "No data to save.")


def COM_PORT_DISPLAY_UPDATE_GPS(App, GNSS_fix=None, latitude=None, NS=None, longtitude=None, EW=None, EET_summer=None, satellite_count=None, HDOP_var=None):
    if App.Clearing_logs == False:
        marker = App.myMapWidget.set_marker(float(latitude), float(longtitude))
        App.markers.append(marker)
        if len(App.markers) > consts.GRAPH_SHIFT_SIZE:
            old_marker = App.markers.popleft()
            old_marker.delete()
        
        App.myLabel_FIX_status['background'] = "green" if int(
            GNSS_fix) == 1 else "red"
        App.myLabel_time_value['text'] = EET_summer[0:2] + \
            ':'+EET_summer[2:4]+':'+EET_summer[4:6]
        App.myLabel_sattelites_value['text'] = satellite_count
        App.myLabel_HDOP_value['text'] = HDOP_var
        App.myLabel_Lat_value['text'] = f"{float(latitude) if NS == 'N' else -float(latitude):.5f}"
        App.myLabel_Lon_value['text'] = f"{float(longtitude) if EW == 'E' else -float(longtitude):.5f}"


def SENSOR_DISPLAY_UPDATE(App, temperature=None, pressure=None):
    App.Temp_array.append(temperature)
    App.Press_array.append(pressure)
    App.myGraphIndexArraySensor.append(App.myGraphIndex)

    App.Temp_array = App.Temp_array[-(3*consts.GRAPH_SHIFT_SIZE):]
    App.Press_array = App.Press_array[-(3*consts.GRAPH_SHIFT_SIZE):]
    App.myGraphIndexArraySensor = App.myGraphIndexArraySensor[-(
        3*consts.GRAPH_SHIFT_SIZE):]

    App.myGraphTemp.set_data(App.myGraphIndexArraySensor, App.Temp_array)
    App.myGraphPres.set_data(App.myGraphIndexArraySensor, App.Press_array)

    App.myGraphTemp.axes.relim()
    App.myGraphTemp.axes.autoscale_view()
    App.myGraphPres.axes.relim()
    App.myGraphPres.axes.autoscale_view()
    App.myGraphIndex += 1
    App.myCanvas.draw_idle()


def DB_Tables_Check_Create():
    "Check and create tables for database"

    DB_connection = mysql.connector.connect(**config)
    cursor = DB_connection.cursor()
    # test if tables are available in DB
    cursor.execute("SHOW TABLES")
    received = cursor.fetchall()
    # getting list of tuples, convert to list for tables
    result = np.array(received).flatten().tolist()
    if (set(consts.table_names).issubset(result)) == False:
        if not consts.table_names[1] in result:
            table_query = f"""CREATE TABLE {consts.table_names[1]} (
  `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
  `FIX` bit(1) NOT NULL,
  `LATITUDE` double(8,5) NOT NULL,
  `NS` varchar(1) NOT NULL,
  `LONGTITUDE` double(8,5) NOT NULL,
  `EW` varchar(1) NOT NULL,
  `YR_MONTH_DAY` date DEFAULT NULL,
  `TIME` time DEFAULT NULL,
  `SATELL_CNT` tinyint(3) unsigned NOT NULL,
  `HDOP` float(3,1) unsigned NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
            cursor.execute(table_query)
            # set ID to 1
            increment_query = f"ALTER TABLE {consts.table_names[1]} AUTO_INCREMENT=1"
            cursor.execute(increment_query)
            
        if not consts.table_names[0] in result:
            table_query = f"""CREATE TABLE {consts.table_names[0]} (
 `GPS_ID` bigint(11) unsigned NOT NULL,
  `SUBINDEX_TIME` tinyint(3) unsigned NOT NULL,
  `TEMPERATURE` float(5,1) NOT NULL,
  `PRESSURE` float(6,1) unsigned NOT NULL,
  KEY `GPS_ID` (`GPS_ID`),
  CONSTRAINT `TIME_LINKING` FOREIGN KEY (`GPS_ID`) REFERENCES `gnss_module` (`ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci"""
            cursor.execute(table_query)
            # set ID to 1
            increment_query = f"ALTER TABLE {consts.table_names[0]} AUTO_INCREMENT=1"
            cursor.execute(increment_query)
    DB_connection.commit()
    cursor.close()
    DB_connection.close()


def DB_Create_Connection(App):
    try:
        DB_connection = mysql.connector.connect(**config)
        cursor = DB_connection.cursor()

        App.mySQL_open_status['background'] = "green"
        App.mySQL_open_status['text'] = "OK"
        DB_Tables_Check_Create()
    except mysql.connector.Error as err:
        App.mySQL_open_status['background'] = "red"
        App.mySQL_open_status['text'] = "ER"

        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror(
                "ERROR", "Something is wrong with your user name or password")
            App.mySQL_start_record['state'] = 'disabled'
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            if (messagebox.askyesno("ERROR", "Database does not exist, do you want to create it?", icon='warning') == True):
                temp_config = config.copy()
                temp_config.pop('database')
                DB_connection = mysql.connector.connect(**temp_config)
                cursor = DB_connection.cursor()
                cursor.execute(f"CREATE DATABASE {config['database']}")
                DB_connection.commit()
                App.mySQL_open_status['background'] = "green"
                App.mySQL_open_status['text'] = "OK"
                messagebox.showinfo(
                    "INFO", f"Database {config['database']} created successfully.")
                # create all tables needed
                DB_Tables_Check_Create()
        else:
            messagebox.showerror("ERROR", f"Database connection error: {err}")
            App.mySQL_start_record['state'] = 'disabled'


def DB_Add_Data(App, data: dict):  # brief data is dict
    """'ID' : LPS22HB,'temp'  temperature,'pressure'  pressure}
    'ID' : "GPS",'FIX'  GNSS_fix,'LAT'  latitude'NS' NS,'LONG'  longtitude,'EW'  EW,'TIME'  EET_summer,'SATELL'  satellite_count,'HDOP'  HDOP_var"""
    try:
        db_connect = mysql.connector.connect(**config)
        db_cursor = db_connect.cursor()

        if data['ID'] == consts.table_names[0]:  # LPS22HB
            insert_query = f"""INSERT INTO {data['ID']} (GPS_ID,SUBINDEX_TIME,TEMPERATURE, PRESSURE) VALUES(
'{data['GPS_ID']}',
'{data['subindex']}',
'{data['temp']}',
'{data['pressure']}')"""
            db_cursor.execute(insert_query)
            db_connect.commit()

        elif data['ID'] == consts.table_names[1]:  # GPS
            insert_query = f"""INSERT INTO {data['ID']} VALUES(
                '0',
                {data['FIX']},
                {data['LAT']},
                '{data['NS']}',
                {data['LONG']},
                '{data['EW']}',
                CURRENT_DATE,
                {data['TIME']},
                {data['SATELL']},
                {data['HDOP']}
            )"""
            #NS and EW need '', otherwise MySQL not match 0 for auto increment, date YYYYMMDD format for CURRENT_DATE function in MySQL
            db_cursor.execute(insert_query)
            db_connect.commit()
    except Exception as e:
        messagebox.showerror("ERROR", f"Error saving data to MySQL: {e}")
        # turn off saving to SQL
        App.var.set(0)

def saveExcel(Database_tab):
    try:
        workbook = Workbook()
        #GPS
        sheet = workbook.active
        sheet.title = "GPS"
        sheet.delete_rows(idx=2, amount=15)
        for row_id in Database_tab.myTreeViewGPS.get_children():
            row = Database_tab.myTreeViewGPS.item(row_id)['values']
            sheet.append(row)
        workbook.save(filename=f'EXPORTED_{Database_tab.myComboBox_Date_Select.get()}_F{Database_tab.myComboBox_Time_from.get()}-T{Database_tab.myComboBox_Time_to.get()}.xlsx')
        #SENSOR
        sheet=workbook.create_sheet('SENSOR')
        sheet.delete_rows(idx=2, amount=15)
        for row_id in Database_tab.myTreeViewSENSOR.get_children():
            row = Database_tab.myTreeViewSENSOR.item(row_id)['values']
            sheet.append(row)
        workbook.save(filename=f'EXPORTED_{Database_tab.myComboBox_Date_Select.get()}_F{Database_tab.myComboBox_Time_from.get()}-T{Database_tab.myComboBox_Time_to.get()}.xlsx')
        messagebox.showinfo("SUCCESS", "Data has been exported succefully to Exported_data.xlsx")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error saving data: {e}")
    Database_tab.lift()