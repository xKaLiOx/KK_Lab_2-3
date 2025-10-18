import tkinter
from class_UI import Application


def main():
    App = Application()
    App.create_widgets()
    App.configure_matlab()
    App.create_layout()
    
    App.mainloop()
    

if __name__ == "__main__":
    main()