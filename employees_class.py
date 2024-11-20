from tkinter import ttk
import tkinter as tk
import sqlite3


class EmployeeClass(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.config(width=800, height=600)
        tab_len = int(500 / 5)
        self.pack_propagate(False)
        self.tree = ttk.Treeview(self, columns=("employee id", "employee name", "employee last name", "employee age", "employee position"), show="headings")
        self.tree.pack(pady=20, padx=20, fill='both', expand=True)

        self.tree.column("employee id", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee last name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee age", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee position", anchor=tk.CENTER, width=tab_len)

        self.tree.heading("employee id", text="employee id")
        self.tree.heading("employee name", text="employee name")
        self.tree.heading("employee last name", text="employee last name")
        self.tree.heading("employee age", text="employee age")
        self.tree.heading("employee position", text="employee position")

        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        employees = cursor.execute("""select * from employees""").fetchall()

        for row in employees:
            self.tree.insert("", tk.END, values=row)