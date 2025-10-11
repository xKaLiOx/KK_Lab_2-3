#main packages
import tkinter as tk
import tkintermapview
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

#declaring my modules
import KK_Lab2_UART_TAB
import KK_Lab2_FUNCTIONS as Func
import KK_Lab2_GLOBALS as globals

MAIN_WINDOW_HEIGHT = 750
MAIN_WINDOW_WIDTH = 1150

WIDTH_RIGHT_GUI = 600
HEIGHT_RIGHT_GUI = 700

#main window
root = tk.Tk()
root.title("Kompiuterinės komunikacijos 2 laboratorinis darbas")
root.geometry("{}x{}+{}+{}".format(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, 200, 15))
root.iconbitmap("icon.ico")
root.resizable(False, False)

#graph matlab
px = 1/matplotlib.rcParams['figure.dpi']  # pixel in inches
myFigureMain = Figure(dpi=100,tight_layout=True,figsize=(WIDTH_RIGHT_GUI*px,HEIGHT_RIGHT_GUI/2*px))
myGraphPressureAx = myFigureMain.add_subplot(212)
myGraphTempAx = myFigureMain.add_subplot(211)

myGraphTemp, = myGraphTempAx.plot([],[])
myGraphPres, = myGraphPressureAx.plot([],[])

matplotlib.rcParams.update({'axes.titlesize':12, 'figure.titlesize':18})
myFigureMain.suptitle('LPS22HB data')
myGraphTempAx.set_title('Temperature graph')
myGraphPressureAx.set_title('Pressure graph')
myGraphTempAx.set_ylabel(r"Temperature, $\degree$C")
myGraphPressureAx.set_ylabel("Pressure, hPa")
myGraphPressureAx.set_xlabel("Samples")
myGraphTempAx.grid()
myGraphPressureAx.grid()
myGraphTempAx.set_xlabel("Samples")
myGraphPressureAx.ticklabel_format(style='plain',useOffset=False)

myGraphPressureAx.set_xlim(auto=True)
myGraphTempAx.set_xlim(auto=True)

myFrame_right_side = tk.Frame(root,height=HEIGHT_RIGHT_GUI,width=WIDTH_RIGHT_GUI)
myFrame_right_bottom = tk.Frame(myFrame_right_side,background='blue',bg='blue',height=HEIGHT_RIGHT_GUI/2,width=WIDTH_RIGHT_GUI)
myCanvas = FigureCanvasTkAgg(myFigureMain, master=myFrame_right_side)

myButton_exit = tk.Button(root, text="Exit", command=lambda :Func.GUI_Exit(root),width=8, height=1,font=globals.myFontMain)
myButton_port_settings = tk.Button(root, text="Serial Port Settings",font=("Times New Roman", 15,'bold'),width=20, height=2,
                                   command=lambda :KK_Lab2_UART_TAB.com_port_settings(root))
myButton_clear_Label = tk.Button(root, text="Clear data",width=8, height=1,
                                 command=lambda : Func.com_port_log_clear(myText_COM_logs,myGraphTemp,myGraphPres,myCanvas,myMapWidget),font=globals.myFontMain)

myText_COM_logs = tk.Text(root, height=10, width=53, font=globals.myFontMain, state='disabled')

myLabel_COM_status = tk.Label(root, background="red",padx=35, font=globals.myFontMid,width=9)
myLabel_FIX = tk.Label(root, text="GNSS FIX STATUS", font=globals.myFontBiggest)
myLabel_FIX_status = tk.Label(root, background="red",padx=5, font=globals.myFontMain,width=3)

myLabel_time = tk.Label(root, text="Time(EET):", font=globals.myFontBiggest)
myLabel_time_value = tk.Label(root, text="--:--:--", font=globals.myFontBiggest,anchor='w',justify="left")

myLabel_sattelites = tk.Label(root, text="Satellites:", font=globals.myFontMid)
myLabel_sattelites_value = tk.Label(root, text="--", font=globals.myFontMid,anchor='w',justify="left")

myLabel_HDOP = tk.Label(root, text="HDOP:", font=globals.myFontMid)
myLabel_HDOP_value = tk.Label(root, text="--", font=globals.myFontMid,anchor='w',justify="left")

myButton_open_port = tk.Button()

value_change = {"open_port":myButton_open_port,
                "com_status":myLabel_COM_status,
                "root":root,
                "com_logs":myText_COM_logs,
                "FIX":myLabel_FIX_status,
                "TIME":myLabel_time_value,
                "SATTELITES":myLabel_sattelites_value,
                "HDOP":myLabel_HDOP_value
                }


#right side gui
myToolbar = NavigationToolbar2Tk(myCanvas, myFrame_right_side,pack_toolbar=False)
myCanvas.draw()
myToolbar.update()

myMapWidget = tkintermapview.TkinterMapView(myFrame_right_bottom, width=WIDTH_RIGHT_GUI, height=HEIGHT_RIGHT_GUI/2,)
myMapWidget.set_position(54.90396923101469, 23.957806638243493) #KTU 11 rumai
myMapWidget.set_zoom(12)
tile_server_url = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
myMapWidget.set_tile_server(tile_server_url,max_zoom = 17)
#use light map for faster response and less max zoom

myButton_open_port = tk.Button(root, text="Open port",font=("Times New Roman", 13),padx=40,width=10, height=1,
                               command=lambda :Func.COM_port_Open_Close(myButton_open_port,
                                                                        myLabel_COM_status,
                                                                        root,myText_COM_logs,
                                                                        myLabel_FIX_status,
                                                                        myLabel_time_value,
                                                                        myLabel_sattelites_value,
                                                                        myLabel_HDOP_value,
                                                                        myGraphTemp,
                                                                        myGraphPres,
                                                                        myCanvas,
                                                                        myMapWidget))

#grid placements
tk.Label(root, text="").grid(row=0, column=0,columnspan=5)
tk.Label(root, text="").grid(row=4, column=0,columnspan=5)
tk.Label(root, text="").grid(row=6, column=0,columnspan=5)
tk.Label(root, text="").grid(row=8, column=0,columnspan=5,pady=15)
tk.Label(root, text="").grid(row=10, column=0,columnspan=5)
tk.Label(root, text="").grid(row=12, column=0,columnspan=5)

myButton_port_settings.grid(row=1, column=0,rowspan=3,padx=10)
myLabel_COM_status.grid(row=3, column=2,padx=10)
tk.Label(root, text="").grid(row=2, column=2)
myButton_open_port.grid(row=1, column=2)

myText_COM_logs.grid(row=5, column=0, columnspan=5,padx=10)
myButton_clear_Label.grid(row=7,column=0,columnspan=5)

myLabel_FIX.grid(row=9,column=0,padx=10,columnspan=2)
myLabel_FIX_status.grid(row=9,column=1,padx=10,sticky="w")
myLabel_time.grid(row=11,column=0,columnspan=2,padx=10)
myLabel_time_value.grid(row=11,column=2,sticky="w",columnspan=3)
myLabel_sattelites.grid(row=13,column=0,columnspan=2,padx=10)
myLabel_sattelites_value.grid(row=13,column=2,sticky="w",columnspan=3)
myLabel_HDOP.grid(row=14,column=0,columnspan=2,padx=10)
myLabel_HDOP_value.grid(row=14,column=2,sticky="w",columnspan=3)

#myButton_exit.grid(row=7, column=8)

#place frame on the right side for graphs
myFrame_right_side.grid(row = 0,rowspan=15,column=5,columnspan=1)
myCanvas.get_tk_widget().grid(row = 1,column=0)
myToolbar.grid(row=0, column=0,sticky='W')
myFrame_right_bottom.grid(row = 2,column=0)
myMapWidget.grid(row = 2,column=0)

tk.mainloop()