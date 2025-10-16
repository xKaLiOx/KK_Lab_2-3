# Default settings and global variables
import serial
import numpy as np

Port_connected = False
Clearing_logs = False
serialPort  = serial.Serial()

MYFONTMAIN = ("Times New Roman", 12)
MYFONTBIGGEST = ("Times New Roman", 18,'bold')
MYFONTMID = ("Times New Roman", 15,'bold')

myGraphIndex = 0 #index for graph values
Index_gps = 0
myGraphIndexArraySensor = []
myGraphIndexArrayGPS = []
GRAPH_SHIFT_SIZE = 60 # 60 latest values

Temp_array = []
Press_array = []
Time_array = []
Lat_array = []
Lon_array = []

selected_port = " "
selected_baud_rate = 9600
selected_parity = "None"
selected_stop_bits = 1
selected_data_bits = 8

parity_option_dict = {"None": serial.PARITY_NONE,"Even": serial.PARITY_EVEN,"Odd": serial.PARITY_ODD,"Mark": serial.PARITY_MARK,"Space": serial.PARITY_SPACE}
