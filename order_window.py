import tkinter as tk
from tkinter import ttk, messagebox

# Sample categorized menu
menu_data = {
    "Indian": {
        "Paneer Butter Masala": 240,
        "Dal Makhani": 180,
        "Butter Naan": 40,
        "Chicken Biryani": 280,
        "Veg Biryani": 220,
        "Tandoori Roti": 20,
        "Palak Paneer": 210
    },
    "Chinese": {
        "Veg Manchurian": 180,
        "Chicken Manchurian": 220,
        "Hakka Noodles": 160,
        "Veg Fried Rice": 140,
        "Chicken Fried Rice": 190,
        "Spring Roll": 100
    },
    "Snacks": {
        "Burger": 120,
        "Pizza": 250,
        "French Fries": 90,
        "Garlic Bread": 110,
        "Samosa": 30,
        "Pav Bhaji": 100,
        "Chole Bhature": 120
    },
    "Drinks": {
        "Coke": 40,
        "Mojito": 60,
        "Masala Chai": 30,
        "Cold Coffee": 70,
        "Lassi": 50,
        "Orange Juice": 60
    }
}

order_items = []

def open_order_window():
    order_win = tk.Toplevel()
    order_win.title("Take Order")
    order_win.geometry("700x600")
    order_win.configure(bg="#fff8f0")

    # --- Category Dropdown ---
    tk.Label(order_win, text="Select Category:", bg="#fff8f0").pack(pady=(10, 0))
    category_var = tk.StringVar(value="Main Course")
    category_menu = ttk.Combobox(order_win, textvariable=category_var, values=list(menu_data.keys()), state="readonly")
    category_menu.pack()

    # --- Search Bar ---
    tk.Label(order_win, text="Search Item:", bg="#fff8f0").pack(pady=(10, 0))
    search_var = tk.StringVar()
    search_entry = tk.Entry(order_win, textvariable=search_var, width=30)
    search_entry.pack()

    # --- Item Dropdown (Filtered) ---
    tk.Label(order_win, text="Select Item:", bg="#fff8f0").pack(pady=(10, 0))
    item_var = tk.StringVar()
    item_menu = ttk.Combobox(order_win, textvariable=item_var)
    item_menu.pack()

    # --- Quantity ---
    tk.Label(order_win, text="Quantity:", bg="#fff8f0").pack(pady=(10, 0))
    qty_var = tk.IntVar(value=1)
    tk.Entry(order_win, textvariable=qty_var, width=5).pack()

    # --- Treeview for Order Items ---
    columns = ("Item", "Qty", "Subtotal")
    tree = ttk.Treeview(order_win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=20)

    # --- Update Item Dropdown based on filters ---
    def update_item_list(*args):
        category = category_var.get()
        search = search_var.get().lower()
        items = menu_data.get(category, {})
        filtered_items = [item for item in items if search in item.lower()]
        item_menu["values"] = filtered_items
        if filtered_items:
            item_var.set(filtered_items[0])
        else:
            item_var.set("")

    category_var.trace("w", update_item_list)
    search_var.trace("w", update_item_list)
    update_item_list()  # initial fill

    # --- Add Item Button ---
    def add_item():
        item = item_var.get()
        qty = qty_var.get()
        category = category_var.get()
        if not item or qty <= 0:
            messagebox.showerror("Error", "Please select a valid item and quantity.")
            return
        price = menu_data[category][item]
        subtotal = price * qty
        order_items.append((item, qty, subtotal))
        tree.insert('', 'end', values=(item, qty, f"₹{subtotal}"))

    tk.Button(order_win, text="Add to Order", command=add_item, bg="#4caf50", fg="white", font=("Arial", 12)).pack()

    # --- Delete Selected Item Button ---
    def delete_selected_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an item to delete.")
            return
        for item_id in selected:
            values = tree.item(item_id, "values")
            tree.delete(item_id)
            for entry in order_items:
                if str(entry[0]) == str(values[0]) and str(entry[1]) == str(values[1]) and f"₹{entry[2]}" == values[2]:
                    order_items.remove(entry)
                    break

    tk.Button(order_win, text="Delete Selected Item", command=delete_selected_item, bg="#f44336", fg="white",
              font=("Arial", 12)).pack(pady=5)

    # --- Send to Billing ---
    def send_to_billing():
        if not order_items:
            messagebox.showwarning("No Order", "Please add items to the order.")
            return
        from billing_system import open_billing_window
        open_billing_window(order_items)
        order_win.destroy()

    tk.Button(order_win, text="Send to Billing", command=send_to_billing, bg="#2196f3", fg="white",
              font=("Arial", 12)).pack(pady=10)

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide root window
    open_order_window()
    root.mainloop()
