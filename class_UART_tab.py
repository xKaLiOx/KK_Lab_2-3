import tkinter as tk
from tkinter import ttk
import class_constants as consts
import serial
import serial.tools.list_ports

class Application_UART_Settings(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.resizable(False, False)
        self.title("UART settings")
        self.iconbitmap("icon.ico")
        self.root = root
        
        
        #UART settings options
        self.port_options = []
        self.stop_bits_options = [1, 2]
        self.baud_rate_options = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
        self.data_bits_options = [5, 6, 7, 8]
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (consts.UART_WINDOW_WIDTH/2))
        y_cordinate = int((screen_height/2) - (consts.UART_WINDOW_HEIGHT/2))
        self.geometry("{}x{}+{}+{}".format(consts.UART_WINDOW_WIDTH, consts.UART_WINDOW_HEIGHT, x_cordinate, y_cordinate))
    
    def create_widgets(self):
        self.myLabel_port_name = tk.Label(self, text="Port name", font=consts.MYFONTMAIN,justify="center",padx=50)
        self.myComboBox_port_name = ttk.Combobox(self, state='readonly',font=consts.MYFONTMAIN,width=15)
        self.myLabel_port_rate = tk.Label(self, text="Baud rate", font=consts.MYFONTMAIN,justify="center",padx=50)
        self.myComboBox_port_rate = ttk.Combobox(self, state='readonly',font=consts.MYFONTMAIN,width=15)
        self.myLabel_port_parity = tk.Label(self, text="Parity", font=consts.MYFONTMAIN,justify="center",padx=50)
        self.myComboBox_port_parity = ttk.Combobox(self, state='readonly',font=consts.MYFONTMAIN,width=15)
        self.myLabel_port_stop_bits = tk.Label(self, text="Stop bits", font=consts.MYFONTMAIN,justify="center",padx=50)
        self.myComboBox_port_stop_bits = ttk.Combobox(self, state='readonly',font=consts.MYFONTMAIN,width=15)
        self.myLabel_port_data_bits = tk.Label(self, text="Data bits", font=consts.MYFONTMAIN,justify="center",padx=50)
        self.myComboBox_port_data_bits = ttk.Combobox(self, state='readonly',font=consts.MYFONTMAIN,width=15)
        
        self.myButton_port_settings_apply = tk.Button(self, text="Apply",width=4, height=1,font=consts.MYFONTMAIN
                                                      ,command = lambda: self.Update_Settings_COM(self.myComboBox_port_name.get()
                                                                                                  ,self.myComboBox_port_rate.get()
                                                                                                  ,self.myComboBox_port_parity.get()
                                                                                                  ,self.myComboBox_port_stop_bits.get()))
        self.myButton_port_settings_cancel = tk.Button(self, text="Cancel", command=self.destroy,width=4, height=1,font=consts.MYFONTMAIN)
    
    def create_values(self):
        self.myComboBox_port_name['values'] = [port.device for port in serial.tools.list_ports.comports()]
        self.myComboBox_port_name.set("Select COM port")
        self.myComboBox_port_rate['values'] = self.baud_rate_options
        self.myComboBox_port_rate.set(self.root.selected_baud_rate)
        self.myComboBox_port_parity['values'] = list(consts.parity_option_dict.keys())
        self.myComboBox_port_parity.set(self.root.selected_parity)
        self.myComboBox_port_stop_bits['values'] = self.stop_bits_options
        self.myComboBox_port_stop_bits.set(self.root.selected_stop_bits)
        self.myComboBox_port_data_bits['values'] = self.data_bits_options
        self.myComboBox_port_data_bits.set(self.root.selected_data_bits)
    
    def Update_Settings_COM(self, port, baud, parity, stop):
        #update globals for main GUI
        self.root.selected_baud_rate = baud
        self.root.selected_port = port
        self.root.selected_parity = parity
        self.root.selected_stop_bits = stop
        self.destroy()
    
    def create_layout(self):
        self.myLabel_port_name.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=1, column=0,columnspan=2)
        self.myComboBox_port_name.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=2, column=0,columnspan=2)
        self.myLabel_port_rate.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=4, column=0,columnspan=2)
        self.myComboBox_port_rate.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=5, column=0,columnspan=2)
        self.myLabel_port_parity.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=7, column=0,columnspan=2)
        self.myComboBox_port_parity.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=8, column=0,columnspan=2)
        self.myLabel_port_stop_bits.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=10, column=0,columnspan=2)
        self.myComboBox_port_stop_bits.grid(padx=consts.UART_WINDOW_WIDTH/2-75, row=11, column=0,columnspan=2)

        #add spacing between comboboxes and buttons
        tk.Label(self, text="",justify="center").grid(row=3, column=0)
        tk.Label(self, text="",justify="center").grid(row=6, column=0)
        tk.Label(self, text="",justify="center").grid(row=9, column=0)
        tk.Label(self, text="",justify="center").grid(row=12, column=0)
        
        self.myButton_port_settings_apply.grid(row=13, column=0,ipadx=20)
        self.myButton_port_settings_cancel.grid(row=13, column=1,ipadx=20)