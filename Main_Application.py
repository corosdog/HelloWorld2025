import subprocess, sys
from PIL import Image, ImageTk
from tkinter import Tk, StringVar, Entry, Label, Button, Text, Frame, Toplevel, END, DISABLED, NORMAL, TOP

class MainApp:
    def __init__(self):
        self.app_window = Tk()
        self.app_window.title("Main Application")
        self.app_window.geometry("617x660")
        self.create_widgets()
        self.app_window.mainloop()

    def create_widgets(self):
        check_budg_img = Image.open('Icon_Check_Budget.jpg').resize((300, 300))
        check_budg_icon = ImageTk.PhotoImage(check_budg_img)
        check_budg_button = Button(self.app_window, image=check_budg_icon, text="Budget Tracker", compound=TOP) #, command=self.open_budget)
        check_budg_button.image = check_budg_icon
        check_budg_button.grid(row=0, column=0, padx=0, pady=0)

        add_spending_img = Image.open('Icon_Spending_Type.png').resize((300, 300))
        add_spending_icon = ImageTk.PhotoImage(add_spending_img)
        add_spending_button = Button(self.app_window, image=add_spending_icon, text="Modify Categories", compound=TOP) #, command=self.open_spending)
        add_spending_button.image = add_spending_icon
        add_spending_button.grid(row=0, column=1, padx=0, pady=0)

        calc_icon_img = Image.open('Icon_Calculator.png').resize((300, 300))
        calc_icon = ImageTk.PhotoImage(calc_icon_img)
        calc_button = Button(self.app_window, image=calc_icon, text="Calculator App", compound=TOP) #, command=self.open_calculator)
        calc_button.image = calc_icon
        calc_button.grid(row=1, column=1, padx=0, pady=0)


        

if __name__ == "__main__":
    app = MainApp()
