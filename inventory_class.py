from tkinter import ttk
import tkinter as tk
import sqlite3


class InventoryClass(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.config(width=800, height=600)
        tab_len = int(500 / 5)
        self.pack_propagate(False)
        self.tree = ttk.Treeview(self, columns=("product id", "product name", "product type", "quantity", "price"), show="headings")
        self.tree.pack(pady=20, padx=20, fill='both', expand=True)

        self.tree.column("product id", anchor=tk.CENTER, width=tab_len)
        self.tree.column("product name", anchor=tk.CENTER, width=tab_len)
        self.tree.column("product type", anchor=tk.CENTER, width=tab_len)
        self.tree.column("quantity", anchor=tk.CENTER, width=tab_len)
        self.tree.column("price", anchor=tk.CENTER, width=tab_len)

        self.tree.heading("product id", text="ID")
        self.tree.heading("product name", text="Product Name")
        self.tree.heading("product type", text="Product Type")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price")

        cnxn = sqlite3.connect("inventory.db")
        cursor = cnxn.cursor()

        products = cursor.execute("""select * from product""").fetchall()

        for row in products:
            self.tree.insert("", tk.END, values=row)
