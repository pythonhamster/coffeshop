import tkinter as tk
from tkinter import ttk


class AddCustomer(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x260")
        self.title("Add Customer")
        self.style = ttk.Style()
        self.style.configure("AcStyle", background="#9b59b6")
        self.configure(bg="#9b59b6")

        self.first_name_label = tk.Label(self, text="First Name:")
        self.first_name_label.pack(pady=(13, 0))

        self.first_name_box = tk.Entry(self)
        self.first_name_box.pack()

        self.last_name_label = tk.Label(self, text="Last Name:", background="#9b59b6")
        self.last_name_label.pack()

        self.last_name_box = tk.Entry(self)
        self.last_name_box.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()

        self.email_box = tk.Entry(self)
        self.email_box.pack()

        self.phone_number_label = tk.Label(self, text="Phone Number:")
        self.phone_number_label.pack()

        self.phone_number = tk.Entry(self)
        self.phone_number.pack()

        self.submit_button = tk.Button(self, text="Submit")
        self.submit_button.pack()
