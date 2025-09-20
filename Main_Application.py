import subprocess, sys
from PIL import Image, ImageTk
from tkinter import Tk, StringVar, Entry, Label, Button, Text, Frame, Toplevel, END, DISABLED, NORMAL, TOP

class MainApp:
    def __init__(self):
        self.app_window = Tk()
        self.app_window.title("Main Application")
        self.app_window.geometry("800x600")
        self.create_widgets()
        self.app_window.mainloop()

    def create_widgets(self):
        calc_icon_img = Image.open('Calculator_Icon.jpeg').resize((100, 100))
        calc_icon = ImageTk.PhotoImage(calc_icon_img)
        calc_button = Button(self.app_window, image=calc_icon, text="Calculator App", compound=TOP) #, command=self.open_calculator)
        calc_button.image = calc_icon
        calc_button.grid(row=0, column=1, padx=0, pady=0)
        

if __name__ == "__main__":
    app = MainApp()