import subprocess, sys
from PIL import Image, ImageTk
from tkinter import Tk, StringVar, Entry, Label, Button, Text, Frame, Toplevel, END, DISABLED, NORMAL, TOP

class MainApp:
    def __init__(self):
        self.app_window = Tk()
        self.app_window.title("Main Application")
        self.app_window.geometry("800x600")

        self.app_window.mainloop()
    

if __name__ == "__main__":
    app = MainApp()