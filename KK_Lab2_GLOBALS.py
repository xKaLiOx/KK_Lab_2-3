# Default settings and global variables
import serial

Port_connected = False
serialPort  = serial.Serial()

myFontMain = ("Times New Roman", 12)


selected_port = " "
selected_baud_rate = 9600
selected_parity = "None"
selected_stop_bits = 1
selected_data_bits = 8

parity_option_dict = {"None": serial.PARITY_NONE,"Even": serial.PARITY_EVEN,"Odd": serial.PARITY_ODD,"Mark": serial.PARITY_MARK,"Space": serial.PARITY_SPACE}
