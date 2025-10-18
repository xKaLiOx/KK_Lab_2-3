import tkinter as tk
import numpy as np
import numpy.lib.recfunctions as rfn
from tkinter import messagebox
import class_constants as consts

def Save_Buffer_Data(self):
    if len(self.Press_array) > 0 and len(self.Time_array) > 0:# GPS and LPS data not empty
        try:
            #format a big array
            data1 = rfn.merge_arrays((np.array(self.myGraphIndexArraySensor), np.array(self.Temp_array), np.array(self.Press_array)))
            np.savetxt('KK_Lab2_Data_Sensor.txt', data1, fmt=["%d","%.1f","%.1f"], delimiter=',',header="Index,Temperature,Pressure")
            data2 = rfn.merge_arrays((np.array(self.myGraphIndexArrayGPS),np.array(self.Time_array), np.array(self.Lat_array), np.array(self.Lon_array)))
            np.savetxt('KK_Lab2_Data_GPS.txt', data2, fmt=["%d","%s","%.5f","%.5f"], delimiter=',',header="Index,Time(EET),Latitude,Longitude")
            messagebox.showinfo("INFO", "Data saved to KK_Lab2_Data_Sensor.txt and KK_Lab2_Data_GPS.txt")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error saving data: {e}")
    else:
        messagebox.showwarning("WARNING", "No data to save.")
        
def COM_PORT_DISPLAY_UPDATE_GPS(self,GNSS_fix=None,latitude=None,NS=None,longtitude=None,EW=None,EET_summer=None,satellite_count=None,HDOP_var=None):
    if self.Clearing_logs == False:
        self.myMapWidget.set_marker(float(latitude),float(longtitude))
        self.myLabel_FIX_status['background'] = "green" if int(GNSS_fix) == 1 else "red"
        self.myLabel_time_value['text'] = EET_summer[0:2]+':'+EET_summer[2:4]+':'+EET_summer[4:6]
        self.myLabel_sattelites_value['text'] = satellite_count
        self.myLabel_HDOP_value['text'] = HDOP_var
        self.myLabel_Lat_value['text'] = f"{float(latitude) if NS == 'N' else -float(latitude):.5f}"
        self.myLabel_Lon_value['text'] = f"{float(longtitude) if EW == 'E' else -float(longtitude):.5f}"
        
def SENSOR_DISPLAY_UPDATE(self,temperature=None,pressure=None):
    self.Temp_array.append(temperature)
    self.Press_array.append(pressure)
    self.myGraphIndexArraySensor.append(self.myGraphIndex)
    
    self.Temp_array = self.Temp_array[-(3*consts.GRAPH_SHIFT_SIZE):]
    self.Press_array = self.Press_array[-(3*consts.GRAPH_SHIFT_SIZE):]
    self.myGraphIndexArraySensor = self.myGraphIndexArraySensor[-(3*consts.GRAPH_SHIFT_SIZE):]
    
    self.myGraphTemp.set_data(self.myGraphIndexArraySensor,self.Temp_array)
    self.myGraphPres.set_data(self.myGraphIndexArraySensor,self.Press_array)
    
    self.myGraphTemp.axes.relim(); self.myGraphTemp.axes.autoscale_view()
    self.myGraphPres.axes.relim(); self.myGraphPres.axes.autoscale_view()
    self.myGraphIndex +=1
    self.myCanvas.draw_idle()