import sqlite3
import threading
import tkinter as tk
from tkinter import ttk
import tkinter



class AddEmployee(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.geometry("300x300")
        self.title("Add Employee")
        self.style = ttk.Style()
        self.style.configure("AcStyle", background="#ebf2f2")
        self.configure(bg="#ebf2f2")

        self.first_name_label = tk.Label(self, text="First Name:")
        self.first_name_label.pack(pady=(13, 0))

        self.first_name_box = tk.Entry(self)
        self.first_name_box.pack()

        self.last_name_label = tk.Label(self, text="Last Name:", background="#ebf2f2")
        self.last_name_label.pack()

        self.last_name_box = tk.Entry(self)
        self.last_name_box.pack()

        self.age_label = tk.Label(self, text="Age:", background="#ebf2f2")
        self.age_label.pack()

        self.age_box = tk.Entry(self)
        self.age_box.pack()

        self.position_label = tk.Label(self, text="Position:", background="#ebf2f2")
        self.position_label.pack()

        self.position_box = tk.Entry(self)
        self.position_box.pack()

        self.email_label = tk.Label(self, text="Email:", background="#ebf2f2")
        self.email_label.pack()

        self.email_box = tk.Entry(self)
        self.email_box.pack()

        self.submit_button = tk.Button(self, text="Submit", background="#ebf2f2",
                                       command=self.confirm)
        self.submit_button.pack()

    def confirm(self):
        proceed = tk.messagebox.askyesno("~CONFIRM~", "Are you sure you want add the new employee?")
        if proceed:
            threading.Thread(target=self.add_employee).start()

    def add_employee(self):
        first_name = self.first_name_box.get()
        last_name = self.last_name_box.get()
        age = self.age_box.get()
        position = self.position_box.get()
        email = self.email_box.get()

        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()
        cursor.execute("insert into employees (employee_name, employee_last_name, employee_age, employee_position, email) values (?, ?, ?, ?, ?)",
                       (first_name, last_name, age, position, email))
        cnxn.commit()
        self.after(1, self.master.fetch_data)