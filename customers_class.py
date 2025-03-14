import threading
import tkinter.messagebox
from distutils.command.check import check
from logging import exception
from threading import Thread
from tkinter import ttk
import tkinter as tk
import sqlite3
from add_customers import AddCustomer

import webbrowser
from PIL import Image, ImageDraw, ImageTk
from PIL.ImageOps import expand


class CustomerClass(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.config(width=800, height=600)

        # this controls the length of each tab in a tree
        tab_len = int(500 / 5)

        # data structure system
        self.changes = []
        self.memory = []
        self.has_add = False
        self.search_list = None
        self.delete_list = []


        self.pack_propagate(0)

        # create the tree frame and configure
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(expand=True, fill="both", side="top")
        self.tree = ttk.Treeview(self.tree_frame, columns=("row id", "customer id", "first name", "last name", "email", "phone number"),
                                 show="headings", height=5, displaycolumns=("customer id", "first name", "last name", "email", "phone number"), selectmode="extended")
        self.tree.pack(expand=True, fill="both")
        self.tree.tag_configure("oddrow", background="light grey")


        # creating the seperator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(expand=True, fill="both")

        #creating the search bar
        self.search_bar = ttk.Entry(self, width=40)
        self.search_bar.pack(pady=(15,0))
        self.search_bar.insert(0, " Search...")

        #creating the frame for the buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True, fill="both", side="top")

        # configuring the frames
        self.tree_frame.config(height=600 * 0.85)
        self.tree_frame.pack_propagate(0)
        self.button_frame.config(height=600 * 0.15)
        self.button_frame.pack_propagate(0)

        # building out our buttons

        self.apply_image = tk.PhotoImage(file="png/001-check.png")
        self.apply_button = tk.Button(self.button_frame, text="Apply", command=self.apply_changes, image=self.apply_image, compound=tk.LEFT, width=100, height=40)
        self.apply_button.pack(side="left", expand=True, padx=5, pady=5)

        self.reset_image = tk.PhotoImage(file="png/002-circular.png")
        self.reset_button = tk.Button(self.button_frame, text="Reset", image=self.reset_image, compound=tk.LEFT, command=self.reset, width=100, height=40)
        self.reset_button.pack(side="left", expand=True, padx=5, pady=5)

        self.email_image = tk.PhotoImage(file="png/003-mail.png")
        self.email_button = tk.Button(self.button_frame, text="Email", image=self.email_image, compound=tk.LEFT, command=self.email, width=100, height=40)
        self.email_button.pack(side="left", expand=True, padx=5, pady=5)

        self.add_image = tk.PhotoImage(file="png/add-user.png")
        self.add_button = tk.Button(self.button_frame, text=" Add", command=self.run_add, image=self.add_image, compound=tk.LEFT, width=100, height=40)
        self.add_button.pack(side="left", expand=True, padx=5, pady=5)

        self.delete_image = tk.PhotoImage(file="png/delete.png")
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete, image=self.delete_image, compound=tk.LEFT, width=100, height=40)
        self.delete_button.pack(side="left", expand=True, padx=5, pady=5)

        # configuring all the tree columns

        self.tree.column("row id", width=0, stretch=False)
        self.tree.column("customer id", anchor=tk.CENTER, width=tab_len)
        self.tree.column("first name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("last name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("email", anchor=tk.CENTER, width=tab_len)
        self.tree.column("phone number", anchor=tk.CENTER, width=tab_len)

        self.tree.heading("row id", text = "")
        self.tree.heading("customer id", text="customer id")
        self.tree.heading("first name", text="first name")
        self.tree.heading("last name", text="last name")
        self.tree.heading("email", text="email")
        self.tree.heading("phone number", text="phone number")

        #binding our tree to the double click
        self.tree.bind("<Double-1>", self.process_dc)
        self.tree.bind("<ButtonRelease-1>", self.process_sc)

        #binding our search bar to the disappear methods
        self.search_bar.bind("<FocusIn>", self.search_bar_clicked)
        self.search_bar.bind("<FocusOut>", self.search_bar_clicked_out)
        self.search_bar.bind("<KeyRelease>", self.filter)

        # thread that populates the treee
        threading.Thread(target=self.fetch_data).start()

    def fetch_data(self):
        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        customers = cursor.execute("""select * from customers""").fetchall()
        self.after(1, self.populate_tree, customers)


    def fetch_data_apply(self):
        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        customers = cursor.execute("""select * from customers""").fetchall()
        self.after(1, lambda: setattr(self, "search_list",  customers))


    def populate_tree(self, customers):
        self.clear_tree()
        self.search_list = customers
        for index, row in enumerate(customers):
            if index % 2 != 0:
                self.tree.insert("", tk.END, values=(index,) + row)
            else:
                self.tree.insert("", tk.END, values=(index,) + row, tags=("oddrow", ))

    def process_dc(self, event):
        row_id = event.widget.selection()[0]
        row_id_values = event.widget.item(row_id, "values")
        row_index = int(row_id_values[0])
        column = self.tree.identify_column(event.x)
        if column != "#1" and row_id:
            column_index = int(column.replace("#", ""))

            existing_value = self.tree.item(row_id)["values"][column_index]

            x, y, width, height = self.tree.bbox(row_id, column)

            self.entry = tk.Entry(self.tree)
            self.entry.place(x=x, y=y, height=height, width=width)
            self.entry.insert(0, existing_value)
            self.entry.focus()

            self.entry.bind("<Return>", lambda e: self.save_edit(row_index, row_id, column, column_index, existing_value))
            self.entry.bind("<FocusOut>", lambda e: e.widget.destroy())

    def process_sc(self, event):
        #print(self.tree.selection())
        pass
        # row_id = event.widget.selection()[0]
        # row_id_values = event.widget.item(row_id, "values")
        # customer_id = int(row_id_values[1])
        # print(customer_id)
        # self.delete_list.append(customer_id)


    def save_edit(self, row_index, row, column, column_index, old_value):
        new_value = self.entry.get()
        self.entry.destroy()
        if new_value != old_value:
            self.memory.append([row, column, column_index, old_value, row_index])
            values = list(self.tree.item(row)["values"])
            values[column_index] = new_value
            self.tree.item(row, values=values)
            self.tree.tag_configure("red_font", foreground="red")
            self.tree.item(row, tags=("red_font",))
            customer_id = values[1]  # made a fix here
            customer_dict = {"#1": "customer_id", "#2": "customer_name",
                             "#3": "customer_last_name", "#4": "customer_email",
                             "#5": "customer_phone"}
            self.changes.append([customer_id, customer_dict[column], new_value, row_index, row])
            self.entry.destroy()
        else:
            print("Same Value")

    def apply_changes(self):
        #if somthing has been changed
        if self.changes:
            cnxn = sqlite3.connect("inventory.db")
            cursor = cnxn.cursor()

            for i in self.changes:
                print(i[1], i[2], i[0])
                cursor.execute(f"""update customers set {i[1]} = '{i[2]}' where customer_id = {i[0]}""")
                cnxn.commit()

            self.tree.tag_configure("oddrow", background="light grey")
            self.tree.tag_configure("evenrow", background="white")


            for i in self.changes:
                if int(i[3]) % 2 == 0:
                    self.tree.item(i[4], tags=("oddrow",))
                else:
                    self.tree.item(i[4], tags=("evenrow",))
            self.memory.clear()
            self.changes.clear()
            self.search_list.clear()
            threading.Thread(target= self.fetch_data_apply).start()

    def run_delete(self, customers):
        print("run_delete")
        for i in customers:
            customer_id = self.tree.item(i)["values"][1]
            cnxn = sqlite3.connect("inventory.db")
            cursor = cnxn.cursor()
            cursor.execute(f"delete from customers where customer_id=?", (customer_id,))
            cnxn.commit()
        self.after(1, lambda: threading.Thread(target=self.fetch_data).start())

    def delete(self):
        proceed = tkinter.messagebox.askyesno("~CONFIRM~", "Are you sure you want to delete the highlighted customers?")
        if proceed:
            selected = self.tree.selection()
            threading.Thread(target=self.run_delete, args=(selected,)).start()


        #row_id_values = event.widget.item(row_id, "values")
         #customer_id = int(row_id_values[1])



    def reset(self):
        if self.memory:
            for memory in self.memory:
                row, col, col_index, old_val, row_index = memory
                current_values = list(self.tree.item(row, "values"))

                current_values[col_index] = old_val
                self.tree.item(row, values=current_values)

                self.tree.tag_configure("oddrow", background="light grey")
                self.tree.tag_configure("evenrow", background="white")

                if int(row_index) % 2 == 0:
                    self.tree.item(row, tags=("oddrow",))
                else:
                    self.tree.item(row, tags=("evenrow",))

            self.memory.clear()
            self.changes.clear()

    def email(self):
        selected = self.tree.selection()
        emails = []
        for i in selected:
            customer_email = self.tree.item(i)["values"][4]
            #print(customer_id)
            emails.append(customer_email)
        print(emails)
        #subprocess.run(["open", "-a", "mail"])
        try:
            mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={','.join(emails)}"
            webbrowser.open(mailto_link)
        except Exception as e:
            print("failed")





    def run_add(self):
        if not self.has_add:
            self.add_window = AddCustomer(self)
            self.has_add = True

        def on_closing():
            self.add_window.destroy()
            self.has_add = False

        self.add_window.protocol("WM_DELETE_WINDOW", on_closing)


    #search bar disappear methods
    def search_bar_clicked(self, e):
        if self.search_bar.get() == " Search...":
            self.search_bar.delete(0, "end")

    def search_bar_clicked_out(self, e):
        if self.search_bar.get() == "":
            self.search_bar.insert(0, " Search...")
        #self.search_bar.delete(0, "end")
        # self.search_bar.delete(0, "end")

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def filter(self, e):
        self.tree.tag_configure("oddrow", background="light grey")
        value_to_search = self.search_bar.get()

        def search_each_row(x):
            for i in x:
                if value_to_search.lower() in str(i).lower():
                    return True

        matches = list(filter(search_each_row, self.search_list ))

        self.clear_tree()

        for index, row in enumerate(matches):
            if index % 2 != 0:
                self.tree.insert("", tk.END, values=(index,) + row)
            else:
                self.tree.insert("", tk.END, values=(index,) + row, tags=("oddrow",))





# notes

