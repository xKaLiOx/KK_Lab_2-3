from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import serial as sr
import serial.tools.list_ports

# Konstantos
DISPLAY_CHART_AMOUNT = 10
DEFAULT_BAUDRATE = 921600

# Kintamieji
UART_Started = False # Apsauga, kad duomenys nebūtų nuskaitomi, kol COM PORT uždarytas
COM_Port_Selected = None
COM_Port = None

# Kintamieji grafiko duomenims saugoti
chart_x_data = []
chart_y_data = []

# Funkcijos
# COM PORT aptarnavimo funkcija
def Display_UART_Data():
    global COM_Port_Selected, UART_Started, chart_x_data, chart_y_data
    if UART_Started and COM_Port_Selected.in_waiting > 0:
        # Nuskaitoma viena duomenų eilutė
        COM_Port_Data = COM_Port_Selected.readline().decode('ascii').strip()

        # Tolesnis kodas skirtas pavyzdinės UART žinutės - "SR vertė:-55" apdoroti
        # Duomenys atskiriami pagal ":" ženklą ir išsaugomi į masyvą
        data_parts = COM_Port_Data.split(":")
        # Kintamojo vertė bus visada antroje masyvo vietoje
        value = int(data_parts[1])

        # Atnaujinami priimtų duomenų masyvai
        chart_x_data.append(len(chart_x_data) + 1)
        chart_y_data.append(value)

        # Update the chart
        Chart_Line.set_data(chart_x_data, chart_y_data)
        Chart_Plot.set_xlim(max(1, len(chart_x_data) - DISPLAY_CHART_AMOUNT), len(chart_x_data))
        Chart_Plot.set_ylim(min(chart_y_data) - 10, max(chart_y_data) + 10)
        Chart_Canvas.draw()

        # Atvaizduoti neapdorotus duomenis tekstiniame laukelyje
        COM_Port_UART_Data_Display.config(state='normal')
        COM_Port_UART_Data_Display.insert(tk.END, COM_Port_Data + '\n')
        COM_Port_UART_Data_Display.config(state='disabled')
        COM_Port_UART_Data_Display.yview(tk.END)

    # Iškviečiama ta pati funkcija iš naujo, sudaromas begalinis ciklas
    Application_window.after(1, Display_UART_Data)

# Atnaujina visus aktyvius COM PORT rodomus išskleidžiame sąraše `COM_Port_Selection`
def update_serial_port_values(event):
    COM_Port_Selection['values'] = serial.tools.list_ports.comports()

# COM PORT pasirinkimo funkcija
# Aktyvuojama pasirinkus COM PORT iš sąrašo
def Get_COM_Port(event):
    global COM_Port_Selected, COM_Port
    # Pasirinkto COM PORT numerio atrinkimas
    COM_Port_Full_Name = COM_Port_Selection.get().split()
    COM_Port = COM_Port_Full_Name[0]
    # Aktyvuojami COM PORT valdymo mygtukai
    Start_Stop_Button["state"] = "normal"
    Start_Stop_Button["text"] = "Atidaryti COM PORT"

# COM PORT atidarymo/uždarymo funkcija
# Aktyvuojama paspaudus `Start_Stop_Button` mygtuką
def Start_Stop_COM_Port():
    global UART_Started, COM_Port, COM_Port_Selected
    if UART_Started:
        # Sustabdyti COM PORT
        COM_Port_Selected.close()
        Start_Stop_Button["text"] = "Atidaryti COM PORT"
        UART_Started = False
    else:
        # Atidaryti COM PORT
        Baud_Rate = int(Baud_Rate_Selection.get())
        COM_Port_Selected = sr.Serial(COM_Port, Baud_Rate, timeout=0.3)
        COM_Port_Selected.close()
        COM_Port_Selected.open()
        Start_Stop_Button["text"] = "Uždaryti COM PORT"
        UART_Started = True

# Tekstinio laukelio išvalymo funkcija
# Aktyvuojama paspaudus `Clear_Button` mygtuką
def Clear_All():
    COM_Port_UART_Data_Display["state"] = "normal"
    COM_Port_UART_Data_Display.delete('1.0', tk.END)
    COM_Port_UART_Data_Display["state"] = "disable"

# Grafinės vartotojo sąsajos kūrimas
# Pagrindinės aplikacijos langas
Application_window = tk.Tk()
Application_window.title('Kompiuterinės Komunikacijos 2 Lab. Darbas')
Application_window.geometry("1200x700")
for i in range(4, 5):
    Application_window.grid_rowconfigure(i, weight=1)
for i in range(5):
    Application_window.grid_columnconfigure(i, weight=1)

# COM PORT valdymo elementai
UART_Label = tk.Label(Application_window, text = "COM PORT Valdymas")
UART_COM_Port_Label = tk.Label(Application_window, text = "PORT pasirinkimas:")
UART_COM_Baud_Rate_Label = tk.Label(Application_window, text = "Baud Rate pasirinkimas:")
# COM PORT pasirinkimo sąrašo laukas
COM_Port_Selection = ttk.Combobox(Application_window, state='readonly')
COM_Port_Selection.set("Pasirinkti COM port")
COM_Port_Selection.bind('<Button-1>', update_serial_port_values)
available_ports = serial.tools.list_ports.comports()
Start_Stop_Button = tk.Button(Application_window, text = "Atidaryti COM PORT", command = lambda: Start_Stop_COM_Port(), state = "disabled")
if available_ports:
    COM_Port_Selection.set(available_ports[0])
    Get_COM_Port(None)
COM_Port_Selection.bind('<<ComboboxSelected>>', Get_COM_Port)

# COM PORT duomenų atvaizdavimo tekstinis laukelis
COM_Port_UART_Data_Display = tk.Text(Application_window, width=50, height=26, bg="light grey", state='disabled')
Clear_Button = tk.Button(Application_window, text = "Išvalyti duomenis",  command = lambda: Clear_All())

# Baud rate pasirinkimo sąrašo laukas
Baud_Rate_Selection = ttk.Combobox(Application_window, state='readonly')
Baud_Rate_Selection['values'] = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
Baud_Rate_Selection.set(DEFAULT_BAUDRATE)

# GPS koordinačių tekstiniai laukeliai
GPS_Coordinates_Label = tk.Label(Application_window, text = "GPS Koordinatės:")
GPS_Coordinates_Value = tk.Label(Application_window, text="-----")
# GPS laiko tekstiniai laukeliai
GPS_Time_Label = tk.Label(Application_window, text="EET Laikas:")
GPS_Time_Value = tk.Label(Application_window, text="-----")
# GPS palydovų skaičiaus tekstiniai laukeliai
GPS_Satellites_Label = tk.Label(Application_window, text="Palydovų skaičius:")
GPS_Satellites_Value = tk.Label(Application_window, text="-----")

# Grafikas
Chart_Figure = Figure()
Chart_Plot = Chart_Figure.add_subplot(111)
Chart_Plot.set_title('Duomenų grafikas')
Chart_Plot.set_xlabel('Atskaitos, n')
Chart_Plot.set_ylabel('Amplitudė')
Chart_Plot.grid()
Chart_Line = Chart_Plot.plot([],[])[0]
Chart_Canvas = FigureCanvasTkAgg(Chart_Figure, master=Application_window)

# Grafinės vartotojo sąsajos elementų išdėstymas lentelės principu
UART_Label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
UART_COM_Port_Label.grid(row=1, column=0, padx=10, pady=10)
COM_Port_Selection.grid(row=1, column=1, padx=10, pady=10)
UART_COM_Baud_Rate_Label.grid(row=2, column=0, padx=10, pady=10)
Baud_Rate_Selection.grid(row=2, column=1, padx=10, pady=10)
Start_Stop_Button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
COM_Port_UART_Data_Display.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
Clear_Button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

GPS_Coordinates_Label.grid(row=0, column=2, padx=10, pady=10)
GPS_Coordinates_Value.grid(row=1, column=2, padx=10, pady=10)

GPS_Time_Label.grid(row=0, column=3, padx=10, pady=10)
GPS_Time_Value.grid(row=1, column=3, padx=10, pady=10)

GPS_Satellites_Label.grid(row=0, column=4, padx=10, pady=10)
GPS_Satellites_Value.grid(row=1, column=4, padx=10, pady=10)

Chart_Canvas.get_tk_widget().grid(row=4, column=2, columnspan=3, padx=0, pady=10, sticky="nsew")

# Aplikacijos atidarymas ir pagrindinės funkcijos iškvietimas
Application_window.after(1,Display_UART_Data)
Application_window.mainloop()