import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to export PDF
def export_bill_as_pdf(order_items, total, gst_amount, grand_total):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Bill_{now}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "🧾 Royal Feast -  Bill")

    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Quantity")
    c.drawString(400, y, "Subtotal")

    y -= 20
    for item, qty, sub in order_items:
        c.drawString(50, y, str(item))
        c.drawString(250, y, str(qty))
        c.drawString(400, y, f"₹{sub}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20
    c.drawString(50, y, "-" * 50)
    y -= 20
    c.drawString(50, y, f"Subtotal: ₹{total:.2f}")
    y -= 20
    c.drawString(50, y, f"GST (5%): ₹{gst_amount:.2f}")
    y -= 20
    c.drawString(50, y, f"Total Amount: ₹{grand_total:.2f}")
    y -= 30
    c.drawString(50, y, "Thank you for dining with us!")

    c.save()
    return filename

# Function to save order to Excel
def save_to_excel(order_items):
    file = "orders.xlsx"
    columns = ["Item", "Quantity", "Subtotal", "DateTime"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = [[item, qty, sub, now] for item, qty, sub in order_items]
    new_df = pd.DataFrame(new_data, columns=columns)

    if os.path.exists(file):
        try:
            existing_df = pd.read_excel(file)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except Exception as e:
            print("Error reading existing file:", e)
            combined_df = new_df
    else:
        combined_df = new_df

    combined_df.to_excel(file, index=False)

# Main billing UI
def open_billing_window(order_items):
    billing_win = tk.Toplevel()
    billing_win.title("Billing Summary")
    billing_win.geometry("500x500")
    billing_win.configure(bg="#f8f4ec")

    total = sum(item[2] for item in order_items)
    gst_rate = 0.05
    gst_amount = total * gst_rate
    grand_total = total + gst_amount

    # Title
    tk.Label(billing_win, text="🧾 Final Bill", font=("Arial", 16, "bold"), bg="#f8f4ec").pack(pady=10)

    # Bill Text Area
    text_area = tk.Text(billing_win, height=20, width=60, font=("Courier", 10))
    text_area.pack()

    bill_text = "Item\tQty\tSubtotal\n"
    bill_text += "-" * 35 + "\n"
    for item, qty, sub in order_items:
        bill_text += f"{item}\t{qty}\t₹{sub}\n"
    bill_text += "-" * 35 + "\n"
    bill_text += f"Subtotal:\t\t₹{total:.2f}\n"
    bill_text += f"GST (5%):\t\t₹{gst_amount:.2f}\n"
    bill_text += f"Total:\t\t₹{grand_total:.2f}\n"

    text_area.insert(tk.END, bill_text)
    text_area.config(state="disabled")

    # Save to Excel Button
    tk.Button(billing_win, text="💾 Save Order to Excel",
              command=lambda: save_to_excel(order_items),
              bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=10)

    # PDF Export Button
    def download_pdf():
        filename = export_bill_as_pdf(order_items, total, gst_amount, grand_total)
        messagebox.showinfo("PDF Saved", f"Bill exported as {filename}")

    tk.Button(billing_win, text="🖨️ Print Bill", command=download_pdf,
              bg="#ff9800", fg="white", font=("Arial", 12)).pack(pady=5)

    # Done button
    tk.Button(billing_win, text="✅ Done", command=billing_win.destroy,
              bg="#2196f3", fg="white", font=("Arial", 12)).pack(pady=5)

# For standalone test
if __name__ == "__main__":
    test_order = [("Burger", 2, 240), ("Coke", 1, 40)]
    root = tk.Tk()
    root.withdraw()
    open_billing_window(test_order)
    root.mainloop()
