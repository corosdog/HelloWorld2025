# budget_app.py
# A simple two-screen budget app with a setup form and a dashboard UI.
# Built with Tkinter/ttk; no external dependencies.

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, field
from typing import List, Dict
import math


BG_APP = "#f6f5ff"         # app background (very light purple)
BG_CARD = "#ffffff"        # card background
BG_MUTED = "#f1f3f5"       # muted row background
FG_TEXT = "#1f2937"        # slate-800
FG_SUBTLE = "#6b7280"      # slate-500
FG_SUCCESS = "#16a34a"     # green-600
FG_ACCENT = "#2563eb"      # blue-600
BORDER = "#e5e7eb"         # gray-200

DOT_COLORS = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

def money(n: float) -> str:
    return f"${n:,.2f}"

def pct(n: float) -> str:
    return f"{n:.0f}%"

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


class Category:
    name: str
    limit: float
    color: str = "#22c55e"
    spent: float = 0.0

@dataclass
class AppState:
    income: float = 0.0
    categories: List[Category] = field(default_factory=list)
    # transactions: list of dicts {cat, desc, amount}
    transactions: List[Dict] = field(default_factory=list)


class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Tracker")
        self.geometry("1100x740")
        self.configure(bg=BG_APP)
        self.state = AppState(
            income=0.0,
            categories=[
                Category("Food", 500, DOT_COLORS[0]),
                Category("Rent", 1200, DOT_COLORS[1]),
                Category("Savings", 300, DOT_COLORS[2]),
            ],
        )

        # ttk theme setup
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TLabel", background=BG_APP, foreground=FG_TEXT, font=("Segoe UI", 11))
        style.configure("Subtle.TLabel", foreground=FG_SUBTLE)
        style.configure("H1.TLabel", font=("Segoe UI", 26, "bold"))
        style.configure("H2.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Card.TFrame", background=BG_CARD, bordercolor=BORDER, relief="solid", borderwidth=1)
        style.configure("Muted.TFrame", background=BG_MUTED)
        style.configure("TButton", padding=8, font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", background=FG_ACCENT, foreground="white")
        style.map("Accent.TButton",
                  foreground=[("active", "white")],
                  background=[("active", "#1d4ed8")])
        style.configure("Success.TButton", background=FG_SUCCESS, foreground="white")
        style.map("Success.TButton",
                  foreground=[("active", "white")],
                  background=[("active", "#15803d")])
        style.configure("Thin.Horizontal.TProgressbar", thickness=8)
        style.configure("Summary.TLabel", font=("Segoe UI", 11, "bold"))

        # container
        self.container = tk.Frame(self, bg=BG_APP)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (SetupPage, DashboardPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show("SetupPage")

    def show(self, name: str):
        self.frames[name].tkraise()

    # ---------- state operations ----------
    def set_income(self, value: float):
        self.state.income = max(0.0, value)

    def add_category(self, name="Category", limit=0.0):
        color = DOT_COLORS[len(self.state.categories) % len(DOT_COLORS)]
        self.state.categories.append(Category(name, limit, color))

    def delete_category(self, cat: Category):
        self.state.categories = [c for c in self.state.categories if c is not cat]

    def save_setup(self, cats_data: List[Dict], income: float):
        self.state.income = income
        # rebuild categories preserving spent if same name
        spent_map = {c.name: c.spent for c in self.state.categories}
        self.state.categories = []
        for d in cats_data:
            c = Category(d["name"].strip() or "Category", max(0.0, d["limit"]), d["color"])
            c.spent = spent_map.get(c.name, 0.0)
            self.state.categories.append(c)
        messagebox.showinfo("Saved", "Budget setup saved.")
        self.show("DashboardPage")
        self.frames["DashboardPage"].refresh()

    def add_transaction(self, cat_name: str, desc: str, amount: float):
        cat = next((c for c in self.state.categories if c.name == cat_name), None)
        if not cat:
            messagebox.showerror("Error", "Category not found.")
            return
        amount = max(0.0, amount)
        cat.spent += amount
        self.state.transactions.insert(0, {"category": cat_name, "desc": desc.strip() or "(no description)", "amount": amount})
        self.frames["DashboardPage"].refresh()


class SetupPage(tk.Frame):
    def __init__(self, parent, controller: BudgetApp):
        super().__init__(parent, bg=BG_APP)
        self.controller = controller

        header = ttk.Label(self, text="Budget Setup", style="H1.TLabel")
        header.pack(anchor="w", padx=28, pady=(24, 6))

        # Income
        sec = tk.Frame(self, bg=BG_APP)
        sec.pack(fill="x", padx=28)
        ttk.Label(sec, text="Monthly Income").grid(row=0, column=0, sticky="w")
        self.income_var = tk.StringVar(value="0")
        self.income_entry = ttk.Entry(sec, textvariable=self.income_var, width=40)
        self.income_entry.grid(row=1, column=0, sticky="we", pady=8)
        sec.columnconfigure(0, weight=1)

        # Categories header row
        cat_header = tk.Frame(self, bg=BG_APP)
        cat_header.pack(fill="x", padx=28, pady=(16, 6))
        ttk.Label(cat_header, text="Budget Categories").pack(side="left")
        ttk.Button(cat_header, text="+  Add Category", command=self.add_row).pack(side="right")

        # Category rows container
        self.rows_frame = tk.Frame(self, bg=BG_APP)
        self.rows_frame.pack(fill="x", padx=28)

        # Summary bar
        self.summary = ttk.Label(self, text="", style="Summary.TLabel")
        self.summary.pack(fill="x", padx=28, pady=(16, 0))

        # Save button
        btns = tk.Frame(self, bg=BG_APP)
        btns.pack(fill="x", padx=28, pady=18)
        save = ttk.Button(btns, text="Save Budget Setup", style="Success.TButton", command=self.on_save)
        save.pack(fill="x")

        self.rows: List[CatRow] = []
        for c in self.controller.state.categories:
            self.add_row(prefill=c)
        self.recompute_summary()

    def add_row(self, prefill: Category | None = None):
        row = CatRow(self.rows_frame, on_change=self.recompute_summary, on_delete=self.delete_row)
        if prefill:
            row.set_values(prefill.name, prefill.limit, prefill.color)
        self.rows.append(row)
        row.pack(fill="x", pady=6)

    def delete_row(self, row: "CatRow"):
        self.rows.remove(row)
        row.destroy()
        self.recompute_summary()

    def recompute_summary(self, *_):
        total = 0.0
        for r in self.rows:
            try:
                total += float(r.limit_var.get() or 0)
            except ValueError:
                pass
        try:
            income = float(self.income_var.get() or 0)
        except ValueError:
            income = 0
        if income <= 0:
            pct_txt = "(Infinity% of income)"
        else:
            p = (total / income) * 100.0 if income > 0 else math.inf
            pct_txt = f"({p:.0f}% of income)"
        self.summary.configure(text=f"Total Budget: {money(total)}  {pct_txt}")

    def on_save(self):
        try:
            income = float(self.income_var.get() or 0)
        except ValueError:
            messagebox.showerror("Invalid income", "Income must be a number.")
            return
        cats = []
        seen = set()
        for r in self.rows:
            name = r.name_var.get().strip() or "Category"
            if name in seen:
                messagebox.showerror("Duplicate name", f"Category '{name}' appears more than once.")
                return
            seen.add(name)
            try:
                limit = float(r.limit_var.get() or 0)
            except ValueError:
                messagebox.showerror("Invalid amount", f"Limit for '{name}' must be a number.")
                return
            cats.append({"name": name, "limit": max(0.0, limit), "color": r.color})
        if not cats:
            messagebox.showerror("No categories", "Add at least one category.")
            return
        self.controller.save_setup(cats, max(0.0, income))

class CatRow(tk.Frame):
    def __init__(self, parent, on_change, on_delete):
        super().__init__(parent, bg=BG_APP)
        self.on_change = on_change
        self.on_delete = on_delete
        self.color = DOT_COLORS[0]

        # color dot
        self.dot = tk.Canvas(self, width=20, height=20, bg=BG_APP, highlightthickness=0)
        self.dot.grid(row=0, column=0, padx=(0, 10))
        self._dot_id = self.dot.create_oval(4, 4, 16, 16, fill=self.color, outline=self.color)
        self.dot.bind("<Button-1>", self.cycle_color)

        self.name_var = tk.StringVar(value="Category")
        self.limit_var = tk.StringVar(value="0")

        self.name_entry = ttk.Entry(self, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, sticky="we")
        self.limit_entry = ttk.Entry(self, textvariable=self.limit_var, width=14, justify="right")
        self.limit_entry.grid(row=0, column=2, padx=(10, 0))
        self.name_entry.bind("<KeyRelease>", self.on_change)
        self.limit_entry.bind("<KeyRelease>", self.on_change)

        del_btn = ttk.Button(self, text="🗑", width=3, command=lambda: self.on_delete(self))
        del_btn.grid(row=0, column=3, padx=6)

        self.columnconfigure(1, weight=1)

    def set_values(self, name: str, limit: float, color: str):
        self.name_var.set(name)
        self.limit_var.set(str(limit))
        self.color = color
        self.dot.itemconfigure(self._dot_id, fill=self.color, outline=self.color)

    def cycle_color(self, *_):
        i = (DOT_COLORS.index(self.color) + 1) % len(DOT_COLORS)
        self.color = DOT_COLORS[i]
        self.dot.itemconfigure(self._dot_id, fill=self.color, outline=self.color)
        self.on_change()


class DashboardPage(tk.Frame):
    def __init__(self, parent, controller: BudgetApp):
        super().__init__(parent, bg=BG_APP)
        self.controller = controller

        topbar = tk.Frame(self, bg=BG_APP)
        topbar.pack(fill="x", padx=28, pady=(20, 8))

        self.title_lbl = ttk.Label(topbar, text="Budget Tracker", style="H1.TLabel")
        self.title_lbl.pack(side="left")

        btns = tk.Frame(topbar, bg=BG_APP)
        btns.pack(side="right")
        ttk.Button(btns, text="Settings", command=lambda: controller.show("SetupPage")).pack(side="left", padx=6)
        ttk.Button(btns, text="+  Add Expense", style="Accent.TButton",
                   command=self.open_add_expense).pack(side="left", padx=6)

        # Monthly income line
        self.income_line = ttk.Label(self, text="", style="Subtle.TLabel")
        self.income_line.pack(anchor="w", padx=28, pady=(0, 8))

        # cards container
        self.cards_frame = tk.Frame(self, bg=BG_APP)
        self.cards_frame.pack(fill="x", padx=28)

        # recent transactions
        trans_card = ttk.Frame(self, style="Card.TFrame")
        trans_card.pack(fill="both", expand=True, padx=28, pady=(18, 26))
        tk.Frame(trans_card, height=16, bg=BG_CARD).pack()  # top spacing
        ttk.Label(trans_card, text="Recent Transactions", style="H2.TLabel").pack(anchor="w", padx=18)
        tk.Frame(trans_card, height=8, bg=BG_CARD).pack()

        self.trans_container = tk.Frame(trans_card, bg=BG_CARD)
        self.trans_container.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.refresh()

    def refresh(self):
        # income line
        inc = self.controller.state.income
        self.income_line.configure(text=f"Monthly Income: {money(inc)}")

        # rebuild cards
        for child in self.cards_frame.winfo_children():
            child.destroy()

        cats = self.controller.state.categories
        if not cats:
            ttk.Label(self.cards_frame, text="No categories. Add them in Settings.").pack()
            return

        # grid: 3 columns
        cols = 3
        for i, c in enumerate(cats):
            card = self._category_card(self.cards_frame, c)
            r, col = divmod(i, cols)
            card.grid(row=r, column=col, sticky="nsew", padx=14, pady=10)
        for j in range(cols):
            self.cards_frame.columnconfigure(j, weight=1)

        # transactions
        for child in self.trans_container.winfo_children():
            child.destroy()
        txs = self.controller.state.transactions[:10]
        if not txs:
            ttk.Label(self.trans_container, text="No transactions yet. Add your first expense!",
                      style="Subtle.TLabel").pack(anchor="w")
        else:
            for t in txs:
                row = tk.Frame(self.trans_container, bg=BG_CARD)
                row.pack(fill="x", pady=4)
                left = tk.Frame(row, bg=BG_CARD)
                left.pack(side="left", fill="x", expand=True)
                ttk.Label(left, text=t["desc"]).pack(anchor="w")
                ttk.Label(left, text=t["category"], style="Subtle.TLabel").pack(anchor="w")
                ttk.Label(row, text=money(t["amount"]), style="Summary.TLabel").pack(side="right")

    def _category_card(self, parent, cat: Category) -> ttk.Frame:
        card = ttk.Frame(parent, style="Card.TFrame")
        # internal padding wrapper to get a “rounded” feel via spacing
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # Title with colored dot
        top = tk.Frame(inner, bg=BG_CARD)
        top.pack(fill="x")
        dot = tk.Canvas(top, width=14, height=14, bg=BG_CARD, highlightthickness=0)
        dot.create_oval(2, 2, 12, 12, fill=cat.color, outline=cat.color)
        dot.pack(side="right")
        ttk.Label(top, text=cat.name, font=("Segoe UI", 14, "bold")).pack(side="left")

        # Spent line
        spent_line = ttk.Label(inner, text=f"Spent   {money(cat.spent)} / {money(cat.limit)}",
                               style="Subtle.TLabel")
        spent_line.pack(anchor="w", pady=(8, 6))

        # progress bar
        progress = ttk.Progressbar(inner, style="Thin.Horizontal.TProgressbar",
                                   orient="horizontal", mode="determinate", length=300)
        ratio = 0.0 if cat.limit <= 0 else clamp01(cat.spent / cat.limit)
        progress["value"] = ratio * 100
        progress.pack(fill="x")

        # footer: % used and left
        footer = tk.Frame(inner, bg=BG_CARD)
        footer.pack(fill="x", pady=(6, 0))
        used_pct = 0.0 if cat.limit <= 0 else (cat.spent / cat.limit * 100.0)
        used_lbl = ttk.Label(footer, text=f"{used_pct:.0f}% used", foreground=FG_SUCCESS)
        used_lbl.pack(side="left")

        left_amt = max(0.0, cat.limit - cat.spent)
        ttk.Label(footer, text=f"{money(left_amt)} left", style="Subtle.TLabel").pack(side="right")
        return card

    def open_add_expense(self):
        cats = [c.name for c in self.controller.state.categories]
        if not cats:
            messagebox.showerror("No categories", "Create categories in Settings first.")
            return

        dlg = tk.Toplevel(self)
        dlg.title("Add Expense")
        dlg.configure(bg=BG_APP)
        dlg.geometry("420x280")
        dlg.resizable(False, False)

        ttk.Label(dlg, text="Add Expense", style="H2.TLabel").pack(anchor="w", padx=20, pady=(16, 8))

        form = tk.Frame(dlg, bg=BG_APP)
        form.pack(fill="x", padx=20)

        ttk.Label(form, text="Category").grid(row=0, column=0, sticky="w")
        cat_var = tk.StringVar(value=cats[0])
        cat_cb = ttk.Combobox(form, values=cats, textvariable=cat_var, state="readonly")
        cat_cb.grid(row=1, column=0, sticky="we", pady=(2, 10))

        ttk.Label(form, text="Description").grid(row=2, column=0, sticky="w")
        desc_var = tk.StringVar(value="")
        ttk.Entry(form, textvariable=desc_var).grid(row=3, column=0, sticky="we", pady=(2, 10))

        ttk.Label(form, text="Amount").grid(row=4, column=0, sticky="w")
        amt_var = tk.StringVar(value="")
        ttk.Entry(form, textvariable=amt_var).grid(row=5, column=0, sticky="we", pady=(2, 6))

        form.columnconfigure(0, weight=1)

        def submit():
            try:
                amt = float(amt_var.get() or 0)
            except ValueError:
                messagebox.showerror("Invalid amount", "Amount must be a number.")
                return
            if amt <= 0:
                messagebox.showerror("Invalid amount", "Amount must be positive.")
                return
            self.controller.add_transaction(cat_var.get(), desc_var.get(), amt)
            dlg.destroy()

        tk.Frame(dlg, height=6, bg=BG_APP).pack()
        ttk.Button(dlg, text="Add Expense", style="Accent.TButton", command=submit).pack(padx=20, pady=12, fill="x")

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
