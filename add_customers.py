import sqlite3
import threading
import tkinter as tk
from tkinter import ttk



class AddCustomer(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x260")
        self.title("Add Customer")
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

        self.email_label = tk.Label(self, text="Email:", background="#ebf2f2")
        self.email_label.pack()

        self.email_box = tk.Entry(self)
        self.email_box.pack()

        self.phone_number_label = tk.Label(self, text="Phone Number:", background="#ebf2f2")
        self.phone_number_label.pack()

        self.phone_number = tk.Entry(self)
        self.phone_number.pack()

        self.submit_button = tk.Button(self, text="Submit", background="#ebf2f2",
                                       command=lambda: threading.Thread(target=self.add_customer).start())
        self.submit_button.pack()

    def add_customer(self):
        first_name = self.first_name_box.get()
        last_name = self.last_name_box.get()
        email = self.email_box.get()
        phone_number = self.phone_number.get()

        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()
        cursor.execute("insert into customers (customer_name, customer_last_name, customer_email, customer_phone) values (?, ?, ?, ?)",
                       (first_name, last_name, email, phone_number))
        cnxn.commit()

    def after_add(self, func, *args):
        self.after(1, func, args)