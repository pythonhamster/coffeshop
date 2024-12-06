import tkinter as tk



class AddCustomer(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x350")
        first_name_label = tk.Label(self, text="First Name:")
        first_name_label.pack()

        first_name_box = tk.Entry(self)
        first_name_box.pack()

        last_name_label = tk.Label(self, text="Last Name:")
        last_name_label.pack()

        last_name_box = tk.Entry(self)
        last_name_box.pack()

        email_label = tk.Label(self, text="Email:")
        email_label.pack()

        email_box = tk.Entry(self)
        email_box.pack()

        phone_number_label = tk.Label(self, text="Phone Number:")
        phone_number_label.pack()

        phone_number = tk.Entry(self)
        phone_number.pack()
    
