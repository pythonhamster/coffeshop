import webbrowser
import sqlite3
import threading
from tkinter import ttk
import tkinter as tk
import tkinter

from add_employees import AddEmployee


class EmployeeClass(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.config(width=800, height=600)
        tab_len = int(500 / 6)
        self.changes = []
        self.memory = []
        self.has_add = False
        self.search_list = None
        self.delete_list = []

        self.pack_propagate(0)

        # create the tree frame and configure
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(expand=True, fill="both", side="top")
        self.tree = ttk.Treeview(self.tree_frame,
                                 columns=("row id", "employee id", "employee name", "employee last name", "employee age", "employee position", "employee email"),
                                 show="headings", height=5,
                                 displaycolumns=("employee id", "employee name", "employee last name", "employee age", "employee position", "employee email"),
                                 selectmode="extended")
        self.tree.pack(expand=True, fill="both")
        self.tree.tag_configure("oddrow", background="light grey")

        # creating the seperator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(expand=True, fill="both")

        # creating the search bar
        self.search_bar = ttk.Entry(self, width=40)
        self.search_bar.pack(pady=(15, 0))
        self.search_bar.insert(0, " Search...")

        # creating the frame for the buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True, fill="both", side="top")

        # configuring the frames
        self.tree_frame.config(height=600 * 0.85)
        self.tree_frame.pack_propagate(0)
        self.button_frame.config(height=600 * 0.15)
        self.button_frame.pack_propagate(0)

        # building out our buttons

        self.apply_image = tk.PhotoImage(file="png/001-check.png")
        self.apply_button = tk.Button(self.button_frame, text="Apply", command=self.apply_changes,
                                      image=self.apply_image, compound=tk.LEFT, width=100, height=40)
        self.apply_button.pack(side="left", expand=True, padx=5, pady=5)

        self.reset_image = tk.PhotoImage(file="png/002-circular.png")
        self.reset_button = tk.Button(self.button_frame, text="Reset", image=self.reset_image, compound=tk.LEFT,
                                      command=self.reset, width=100, height=40)
        self.reset_button.pack(side="left", expand=True, padx=5, pady=5)

        self.email_image = tk.PhotoImage(file="png/003-mail.png")
        self.email_button = tk.Button(self.button_frame, text="Email", image=self.email_image, compound=tk.LEFT,
                                      command=self.email, width=100, height=40)
        self.email_button.pack(side="left", expand=True, padx=5, pady=5)

        self.add_image = tk.PhotoImage(file="png/add-user.png")
        self.add_button = tk.Button(self.button_frame, text=" Add", command=self.run_add, image=self.add_image,
                                    compound=tk.LEFT, width=100, height=40)
        self.add_button.pack(side="left", expand=True, padx=5, pady=5)

        self.delete_image = tk.PhotoImage(file="png/delete.png")
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete, image=self.delete_image,
                                       compound=tk.LEFT, width=100, height=40)
        self.delete_button.pack(side="left", expand=True, padx=5, pady=5)


        self.tree.column("employee id", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee last name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee age", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee position", anchor=tk.CENTER, width=tab_len)
        self.tree.column("employee email", anchor=tk.CENTER, width=tab_len)

        self.tree.heading("employee id", text="employee id")
        self.tree.heading("employee name", text="employee name")
        self.tree.heading("employee last name", text="employee last name")
        self.tree.heading("employee age", text="employee age")
        self.tree.heading("employee position", text="employee position")
        self.tree.heading("employee email", text="employee email")

        self.tree.bind("<Double-1>", self.process_dc)
        self.tree.bind("<ButtonRelease-1>", self.process_sc)

        # binding our search bar to the disappear methods
        self.search_bar.bind("<FocusIn>", self.search_bar_clicked)
        self.search_bar.bind("<FocusOut>", self.search_bar_clicked_out)
        self.search_bar.bind("<KeyRelease>", self.filter)

        # thread that populates the treee
        threading.Thread(target=self.fetch_data).start()

    def fetch_data(self):
        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        employees = cursor.execute("""select * from employees""").fetchall()
        self.after(1, self.populate_tree, employees)

    def fetch_data_apply(self):
        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        employees = cursor.execute("""select * from employees""").fetchall()
        self.after(1, lambda: setattr(self, "search_list", employees))

    def populate_tree(self, employees):
        self.clear_tree()
        self.search_list = employees
        for index, row in enumerate(employees):
            if index % 2 != 0:
                self.tree.insert("", tk.END, values=(index,) + row)
            else:
                self.tree.insert("", tk.END, values=(index,) + row, tags=("oddrow",))

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

            self.entry.bind("<Return>",
                            lambda e: self.save_edit(row_index, row_id, column, column_index, existing_value))
            self.entry.bind("<FocusOut>", lambda e: e.widget.destroy())

    def process_sc(self, event):
        # print(self.tree.selection())
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
            employee_id = values[1]  # made a fix here
            employee_dict = {"#1": "employee_id", "#2": "employee_name",
                             "#3": "employee_last_name", "#4": "employee_age",
                             "#5": "employeer_position", "#6": "email"}
            self.changes.append([employee_id, employee_dict[column], new_value, row_index, row])
            self.entry.destroy()
        else:
            print("Same Value")

    def apply_changes(self):
        # if somthing has been changed
        if self.changes:
            cnxn = sqlite3.connect("inventory.db")
            cursor = cnxn.cursor()

            for i in self.changes:
                print(i[1], i[2], i[0])
                cursor.execute(f"""update employees set {i[1]} = '{i[2]}' where employee_id = {i[0]}""")
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
            threading.Thread(target=self.fetch_data_apply).start()

    def run_delete(self, employees):
        print("run_delete")
        for i in employees:
            employee_id = self.tree.item(i)["values"][1]
            cnxn = sqlite3.connect("inventory.db")
            cursor = cnxn.cursor()
            cursor.execute(f"delete from employees where employee_id=?", (employee_id,))
            cnxn.commit()
        self.after(1, lambda: threading.Thread(target=self.fetch_data).start())

    def delete(self):
        proceed = tkinter.messagebox.askyesno("~CONFIRM~",
                                              "Are you sure you want to delete the highlighted employees?")
        if proceed:
            selected = self.tree.selection()
            threading.Thread(target=self.run_delete, args=(selected,)).start()

        # row_id_values = event.widget.item(row_id, "values")
        # customer_id = int(row_id_values[1])

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
            employee_email = self.tree.item(i)["values"][6]
            # print(customer_id)
            emails.append(employee_email)
        print(emails)
        # subprocess.run(["open", "-a", "mail"])
        try:
            mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={','.join(emails)}"
            webbrowser.open(mailto_link)
        except Exception as e:
            print("failed")
#####################################
    def run_add(self):
        if not self.has_add:
            self.add_window = AddEmployee(self)
            self.has_add = True

        def on_closing():
            self.add_window.destroy()
            self.has_add = False

        self.add_window.protocol("WM_DELETE_WINDOW", on_closing)

    # search bar disappear methods
    def search_bar_clicked(self, e):
        if self.search_bar.get() == " Search...":
            self.search_bar.delete(0, "end")

    def search_bar_clicked_out(self, e):
        if self.search_bar.get() == "":
            self.search_bar.insert(0, " Search...")
        # self.search_bar.delete(0, "end")
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

        matches = list(filter(search_each_row, self.search_list))

        self.clear_tree()

        for index, row in enumerate(matches):
            if index % 2 != 0:
                self.tree.insert("", tk.END, values=(index,) + row)
            else:
                self.tree.insert("", tk.END, values=(index,) + row, tags=("oddrow",))