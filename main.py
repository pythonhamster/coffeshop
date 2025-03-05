import tkinter as tk
from tkinter import ttk
from inventory_class import InventoryClass
from employees_class import EmployeeClass
from customers_class import CustomerClass

class SimpleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Shop")  # Set the window title
        self.root.geometry("1000x700")  # Set the window size
        self.style = ttk.Style()
        #theme reinserted
        self.style.theme_use("aqua")
        # You can add more widgets here as needed
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")
        self.tabs()

    def tabs(self):
        tab1 = InventoryClass()
        self.tab1_icon = tk.PhotoImage(file="png/001-coffee-cup.png")
        self.notebook.add(tab1, text="Inventory", image=self.tab1_icon, compound=tk.LEFT)

        tab2 = EmployeeClass()
        self.tab2_icon = tk.PhotoImage(file="png/002-partners.png")
        self.notebook.add(tab2, text="Employees", image=self.tab2_icon, compound=tk.LEFT)

        tab3 = ttk.Frame(self.notebook)
        self.tab3_icon = tk.PhotoImage(file="png/003-checklist.png")
        self.notebook.add(tab3, text="Orders", image=self.tab3_icon, compound=tk.LEFT)

        tab4 = CustomerClass()
        self.tab4_icon = tk.PhotoImage(file="png/004-money.png")
        self.notebook.add(tab4, text="Customers", image=self.tab4_icon, compound=tk.LEFT)

if __name__ == "__main__":
    # Step 1: Create the main application window
    root = tk.Tk()

    # Step 2: Create an instance of the SimpleWindow class
    app = SimpleWindow(root)
    root.update_idletasks()

    # Step 3: Start the main event loop
    root.mainloop()