from tkinter import Tk, StringVar, Entry, Label, Button, Text, Frame, END, DISABLED, NORMAL
from math import sin, cos, tan, log, log10, pi
import sys
print(sys.executable)


class CalculatorLogic:
    def __init__(self):
        self.operand = ""
        self.operands = []
        self.z_error = False

    def search_char(self, char, lst):
        for element in lst:
            if type(element) != int and type(element) != float:
                if element in char:
                    return True
        return False

    def simplify_pow(self, expression_list):
        reverse_list = expression_list[::-1]
        while self.search_char("^", reverse_list):
            for element in reverse_list:
                if type(element) == int or type(element) == float:
                    continue
                elif element == "^":
                    index = reverse_list.index(element)
                    result = reverse_list[index+1] ** reverse_list[index-1]
                    del reverse_list[index-1], reverse_list[index-1]
                    reverse_list[index-1] = result
                    break
        return reverse_list[::-1]

    def simplify_mult_div(self, expression_list):
        while self.search_char("*/%", expression_list):
            for element in expression_list:
                if type(element) == int or type(element) == float:
                    continue
                elif element in "*/%":
                    index = expression_list.index(element)
                    if element == "*":
                        result = expression_list[index-1] * expression_list[index+1]
                    elif element == "/":
                        try:
                            result = expression_list[index-1] / expression_list[index+1]
                        except ZeroDivisionError:
                            self.z_error = True
                            return ()
                    elif element == "%":
                        result = expression_list[index-1] % expression_list[index+1]
                    del expression_list[index-1], expression_list[index-1]
                    expression_list[index-1] = result
                    break
        return expression_list

    def simplify_add_sub(self, expression_list):
        while self.search_char("+-", expression_list):
            for element in expression_list:
                if type(element) == int or type(element) == float:
                    continue
                elif element in "+-":
                    index = expression_list.index(element)
                    if element == "+":
                        result = expression_list[index-1] + expression_list[index+1]
                    elif element == "-":
                        result = expression_list[index-1] - expression_list[index+1]
                    del expression_list[index-1], expression_list[index-1]
                    expression_list[index-1] = result
                    break
        return expression_list

    def evaluate(self, expression):
        expression_list = list(expression)
        if expression_list[0] == "-":
            expression_list.insert(0, "0")
        self.operands = []
        self.operand = ""
        self.z_error = False

        for index in range(len(expression_list)):
            char = expression_list[index]
            try:
                if char == " ":
                    continue
                elif char == ".":
                    self.operand += char
                elif float(char) or char == "0":
                    self.operand += char
            except:
                if char not in "+-*^/%":
                    return "ERROR: INVALID FUNCTION USED"
                if char == "-" and expression_list[index-1] in "+-*/%^":
                    self.operand += char
                else:
                    self.operands += [float(self.operand), char]
                    self.operand = ""
        self.operands += [float(self.operand)]
        expression_list = self.operands
        expression_list = self.simplify_pow(expression_list)
        expression_list = self.simplify_mult_div(expression_list)
        expression_list = self.simplify_add_sub(expression_list)
        if self.z_error:
            return "ERROR: CANNOT DIVIDE BY ZERO"
        return expression_list[0]

    def calculator(self, expression, mode=0):
        try:
            while True:
                start_index = end_index = index = 0
                found_end = False
                for element in expression:
                    if element == ")":
                        end_index = index
                        found_end = True
                        found_start = False
                        reverse = expression[end_index::-1]
                        break
                    index += 1
                else:
                    if not found_end:
                        break

                index = 0
                for element in expression[:end_index]:
                    if element == "(":
                        start_index = index
                        found_start = True
                    index += 1
                else:
                    if not found_start:
                        return "Error: Unmatched Parenthesis"
                arg = self.evaluate(expression[start_index+1:end_index])
                if start_index >= 3:
                    funct_id = expression[start_index-3:start_index]
                    if funct_id in ["sin", "cos", "tan"]:
                        if mode == 1:
                            arg *= (pi/180)
                        if funct_id == "sin":
                            val = sin(arg)
                        elif funct_id == "cos":
                            val = cos(arg)
                        else:
                            val = tan(arg)
                    elif funct_id == "qrt":
                        val = (arg) ** 0.5
                        funct_id = "sqrt"
                    elif funct_id == "log":
                        val = log10(arg)
                    elif funct_id[1:] == "ln":
                        funct_id = funct_id[1:]
                        val = log(arg)
                    elif funct_id[2] in "+-/**(":
                        funct_id = ""
                        val = arg
                    else:
                        return "Error: Invalid Function Used"
                else:
                    if "ln" in expression:
                        expression = str(log(arg))
                        continue
                    else:
                        funct_id = ''
                        val = arg
                expression = expression.replace(funct_id + "("+ expression[start_index+1:end_index] + ")", str(val))
        except ZeroDivisionError:
            return("Error: Cannot Divide By Zero")
        except:
            return("Error: Unmatched Parenthesis")
        return self.evaluate(expression)

class CalculatorUI:
    def __init__(self):
        self.app_window = Tk()
        self.app_window.title("Calculator")
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
                                        fg="#FFFFFF", command=self.clear_history)
        self.clear_history_btn.grid(row=1, column=5, sticky="e", padx=0.5)

        self.history_text = Text(self.app_window, font=("Helvetica", 14), height=5, bg="#000000", fg="#FFFFFF",
                                 bd=0, highlightthickness=0)
        self.history_text.grid(row=2, column=0, columnspan=6, sticky="ew", padx=0.5, pady=5)
        self.history_text.config(state=DISABLED)

        self.mode_var = StringVar()
        self.mode_var.set("Mode: rad0")
        self.mode_box = Entry(self.app_window, textvariable=self.mode_var, font=("Helvetica", 10), justify="left",
                              bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)
        self.mode_box.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=0, pady=21)

        self.buttons = [
            ("(", 3, 0, "#3a3d42"), (")", 3, 1, "#3a3d42"), ("DEL", 3, 2, "#3a3d42"), ("AC", 3, 3, "#3a3d42"), ("rad", 3, 4, "#f2a33c"), ("deg", 3, 5, "#f2a33c"),
            ("7", 4, 0, "#5c5d5c"), ("8", 4, 1, "#5c5d5c"), ("9", 4, 2, "#5c5d5c"), ("/", 4, 3, "#3a3d42"), ("^", 4, 4, "#f2a33c"), ("%", 4, 5, "#f2a33c"),
            ("4", 5, 0, "#5c5d5c"), ("5", 5, 1, "#5c5d5c"), ("6", 5, 2, "#5c5d5c"), ("x", 5, 3, "#3a3d42"), ("sin", 5, 4, "#f2a33c"), ("log", 5, 5, "#f2a33c"),
            ("1", 6, 0, "#5c5d5c"), ("2", 6, 1, "#5c5d5c"), ("3", 6, 2, "#5c5d5c"), ("-", 6, 3, "#3a3d42"), ("cos", 6, 4, "#f2a33c"), ("ln", 6, 5, "#f2a33c"),
            ("0", 7, 0, "#5c5d5c"), (".", 7, 1, "#5c5d5c"), ("=", 7, 2, "#5c5d5c"), ("+", 7, 3, "#3a3d42"), ("tan", 7, 4, "#f2a33c"), ("sqrt", 7, 5, "#f2a33c"),
        ]

        for (text, row, col, backg) in self.buttons:
            btn = Button(self.app_window, text=text, font=("Helvetica", 16), width=10, height=2, bd=0,
                         bg=backg, activebackground="#000000", fg="#000000", command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=0, pady=0.5, sticky="nsew")

        for i in range(8):
            self.app_window.grid_rowconfigure(i, weight=1)
            self.app_window.grid_columnconfigure(i, weight=1)

        self.entry_box.bind("<Return>", self.on_return_pressed)
        self.app_window.mainloop()

    def on_button_click(self, text):
        if text == "=":
            expression = self.entry_var.get()
            mode = self.mode_var.get()[-3::]
            result = CalculatorLogic().calculator(expression, int(self.mode_var.get()[-1]))
            self.result_var.set(result)
            expression_no_space=""
            for char in expression:
                if char != " ": expression_no_space += char
            self.update_history(f"{expression_no_space} = {result}")
        elif text == "AC":
            self.entry_var.set("")
        elif text == "DEL":
            self.entry_var.set(self.entry_var.get()[:-1])
        elif text == "x":
            self.entry_var.set(self.entry_var.get()+"*")
        elif text == "rad":
            self.mode_var.set("Mode: rad0")
        elif text == "deg":
            self.mode_var.set("Mode: deg1")
        else:
            self.entry_var.set(self.entry_var.get() + text)

    def on_return_pressed(self, event):
        self.on_button_click("=")

    def update_history(self, text):
        self.history_text.config(state=NORMAL)
        self.history_text.insert(END, f"\n{text}")
        self.history_text.config(state=DISABLED)
        self.history_text.see(END)

    def clear_history(self):
        self.history_text.config(state=NORMAL)
        self.history_text.delete("1.0", END)
        self.history_text.config(state=DISABLED)

if __name__ == "__main__":
    CalculatorUI()
