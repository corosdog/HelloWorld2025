from tkinter import Tk, StringVar, Entry, Label, Button, Text, Frame, END, DISABLED, NORMAL
from math import sin, cos, tan, log, log10, pi

class Configure:
    def __init__(self):
        self.app_window = Tk()
        self.app_window.title("Configure Budget")
        self.app_window.geometry("600x600")

        self.result_var = StringVar()

        self.result_frame = Frame(self.app_window, bg="#000000")
        self.result_frame.grid(row=0, column=0, columnspan=6, sticky="ew")
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)

        
        self.result_label = Label(self.result_frame, textvariable=self.result_var, font=("Helvetica", 24),
                                  anchor="e", bg="#000000", fg="#FFFFFF")
        self.result_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        

        self.entry_var = StringVar()
        self.entry_var.set("")
        self.entry_box = Entry(self.app_window, textvariable=self.entry_var, font=("Helvetica", 36), justify="right",
                               bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)
        self.entry_box.grid(row=0, column=1, columnspan=6, sticky="ew", padx=0, pady=10)
        self.entry_box.focus_set()

        self.history_label = Label(self.app_window, text="History:", font=("Helvetica", 16), bg="#000000",
                                   fg="#FFFFFF")
        self.history_label.grid(row=1, column=0, columnspan=5, sticky="w", padx=0.5)

        self.clear_history_btn = Button(self.app_window, text="Clear History", font=("Helvetica", 10), bg="#FF0000",
                                        fg="#FFFFFF")
        self.clear_history_btn.grid(row=1, column=5, sticky="e", padx=0.5)

        self.history_text = Text(self.app_window, font=("Helvetica", 14), height=5, bg="#000000", fg="#FFFFFF",
                                 bd=0, highlightthickness=0)
        self.history_text.grid(row=2, column=0, columnspan=6, sticky="ew", padx=0.5, pady=5)
        self.history_text.config(state=DISABLED)

        self.mode_var = StringVar()
        self.mode_var.set("Enter Category Name: ")
        self.mode_box = Entry(self.app_window, textvariable=self.mode_var, font=("Helvetica", 20), justify="left",
                              bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)
        self.mode_box.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=0, pady=21)

        self.app_window.mainloop()

if __name__ == "__main__":
    Configure()
