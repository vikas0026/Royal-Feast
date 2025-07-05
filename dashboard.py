import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def open_dashboard_window():
    dashboard = tk.Toplevel()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("1100x750")
    dashboard.configure(bg="#f0f4f8")

    tk.Label(dashboard, text="📊 Royal Feast - Analytics Dashboard",
             font=("Arial", 18, "bold"), bg="#f0f4f8").pack(pady=10)

    # Scrollable Frame
    canvas = tk.Canvas(dashboard, bg="#f0f4f8", highlightthickness=0)
    scrollbar = tk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f0f4f8")

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load Data
    try:
        df = pd.read_excel("orders.xlsx")
        df["Date"] = pd.to_datetime(df["DateTime"]).dt.date
        df["Hour"] = pd.to_datetime(df["DateTime"]).dt.hour
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        dashboard.destroy()
        return

    # CATEGORY MAPPING
    category_map = {
        'Paneer Butter Masala': 'Indian', 'Dal Makhani': 'Indian', 'Butter Naan': 'Indian',
        'Chicken Biryani': 'Indian', 'Veg Biryani': 'Indian', 'Tandoori Roti': 'Indian', 'Palak Paneer': 'Indian',
        'Veg Manchurian': 'Chinese', 'Chicken Manchurian': 'Chinese', 'Hakka Noodles': 'Chinese',
        'Veg Fried Rice': 'Chinese', 'Chicken Fried Rice': 'Chinese', 'Spring Roll': 'Chinese',
        'Burger': 'Snacks', 'Pizza': 'Snacks', 'French Fries': 'Snacks', 'Garlic Bread': 'Snacks',
        'Samosa': 'Snacks', 'Pav Bhaji': 'Snacks', 'Chole Bhature': 'Snacks',
        'Coke': 'Drinks', 'Mojito': 'Drinks', 'Masala Chai': 'Drinks',
        'Cold Coffee': 'Drinks', 'Lassi': 'Drinks', 'Orange Juice': 'Drinks'
    }
    df["Category"] = df["Item"].map(category_map)

    # ========== Layout Frame ==========
    layout_frame = tk.Frame(scroll_frame, bg="#f0f4f8")
    layout_frame.pack(pady=10, fill="x")

    chart_grid_frame = tk.Frame(layout_frame, bg="#f0f4f8")
    chart_grid_frame.grid(row=0, column=0, sticky="nw", padx=20)

    summary_frame = tk.Frame(layout_frame, bg="#e0f7fa", padx=20, pady=20)
    summary_frame.grid(row=0, column=1, sticky="ne", padx=20)

    # Helper to draw and place charts
    def add_chart(fig, title, row, col):
        chart_frame = tk.Frame(chart_grid_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
        tk.Label(chart_frame, text=title, font=("Arial", 14, "bold"), bg="#ffffff").pack()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        chart_frame.grid(row=row, column=col, padx=10, pady=10)

    # 1. Top 5 Selling Items (by Quantity)
    top_items = df.groupby("Item")["Quantity"].sum().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.bar(top_items.index, top_items.values, color="#4caf50")
    ax1.set_ylabel("Quantity Sold")
    ax1.set_title("Top 5 Selling Items")
    add_chart(fig1, "Top 5 Selling Items", row=0, col=0)

    # 2. Top Items by Total Sales Value
    item_sales = df.groupby("Item")["Subtotal"].sum().sort_values(ascending=False).head(5)
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.bar(item_sales.index, item_sales.values, color="#2196f3")
    ax2.set_ylabel("Total ₹ Sales")
    ax2.set_title("Top Items by Revenue")
    add_chart(fig2, "Top Items by Total Sales", row=0, col=1)

    # 3. Sales by Category (Pie Chart)
    category_sales = df.groupby("Category")["Subtotal"].sum()
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.pie(category_sales, labels=category_sales.index, autopct="%1.1f%%", startangle=140)
    ax3.set_title("Category Revenue Share")
    add_chart(fig3, "Sales by Category", row=1, col=0)

    # 4. Revenue per Category (Bar Chart)
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    ax4.bar(category_sales.index, category_sales.values, color="orange")
    ax4.set_ylabel("₹ Total Sales")
    ax4.set_title("Category-wise Revenue")
    add_chart(fig4, "Category Revenue (Bar)", row=1, col=1)

    # 📋 Summary Box (now on right)
    total_revenue = df["Subtotal"].sum()
    avg_order_value = df.groupby("DateTime")["Subtotal"].sum().mean()
    tk.Label(summary_frame, text="📋 Summary", font=("Arial", 14, "bold"), bg="#e0f7fa").pack(pady=(0, 10))
    tk.Label(summary_frame, text=f"Total Revenue:\n₹{total_revenue:.2f}", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
    tk.Label(summary_frame, text=f"Avg Order Value:\n₹{avg_order_value:.2f}", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)

    # 🔙 Back Button
    def go_back():
        dashboard.destroy()

    tk.Button(scroll_frame, text="⬅ Back to Home", command=go_back, bg="#e57373", fg="white",
              font=("Arial", 12)).pack(pady=20)

# You can call open_dashboard_window() from a main app or welcome window
