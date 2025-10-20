import tkinter
from class_UI import Application
from config import *
from class_data_logging import DB_Create_Connection

def main():
    App = Application()
    App.create_widgets()
    DB_Create_Connection(App)
    App.configure_matlab()
    App.create_layout()
    App.mainloop()
    

if __name__ == "__main__":
    main()