import serial
import numpy as np

#constants
MAIN_WINDOW_HEIGHT = 750
MAIN_WINDOW_WIDTH = 1150

UART_WINDOW_HEIGHT = 350
UART_WINDOW_WIDTH = 250

WIDTH_RIGHT_FRAME = 600
HEIGHT_RIGHT_FRAME = 700

MYFONTMAIN = ("Times New Roman", 12)
MYFONTBIGGEST = ("Times New Roman", 18,'bold')
MYFONTMID = ("Times New Roman", 15,'bold')

GRAPH_SHIFT_SIZE = 60 # 60 latest values

parity_option_dict = {"None": serial.PARITY_NONE,"Even": serial.PARITY_EVEN,"Odd": serial.PARITY_ODD,"Mark": serial.PARITY_MARK,"Space": serial.PARITY_SPACE}

table_names = ["lps22hb","gnss_module"]

