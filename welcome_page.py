import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from order_window import open_order_window
from dashboard import open_dashboard_window

# Function to open admin dashboard (with password check)
def open_admin_dashboard():
    def check_password():
        if password_entry.get() == 'admin123':
            pw_window.destroy()
            open_dashboard_window()
        else:
            messagebox.showerror("Access Denied", "Incorrect password")

    pw_window = tk.Toplevel(root)
    pw_window.title("Admin Login")
    pw_window.geometry("300x150")  # ✅ fixed
    pw_window.configure(bg="#fff")
    
    tk.Label(pw_window, text="Enter Admin Password:", font=("Arial", 12), bg="#fff").pack(pady=10)
    password_entry = tk.Entry(pw_window, show='*', font=("Arial", 12), width=25)
    password_entry.pack()
    tk.Button(pw_window, text="Login", command=check_password, bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=10)

# Create main window
root = tk.Tk()
root.title("Welcome to Royal Feast")
root.geometry("1000x600")
root.configure(bg="#f0e6d6")

# Adding logo
try: 
    logo_img = Image.open("Royal.png")
    logo_img = logo_img.resize((300, 300))
    logo = ImageTk.PhotoImage(logo_img)
    tk.Label(root, image=logo, bg="#f0e6d6").pack(pady=10)
except Exception as e:
    print("logo not found", e)

# Title
tk.Label(root, text="Welcome to Royal Feast", font=("Helvetica", 20, "bold"), bg="#f0e6d6", fg="#5a3e36").pack(pady=10)

# Start Order Button
tk.Button(root, text="Start Order", font=("Helvetica", 14), bg="#8bc34a", fg="white", width=20, command=open_order_window).pack(pady=10)

# Admin Dashboard Button (✅ fixed)
tk.Button(root, text="Admin Dashboard", font=("Helvetica", 14), bg="#03a9f4", fg="white", width=20, command=open_admin_dashboard).pack(pady=10)

# Footer
tk.Label(root, text="Developed by Vikas", font=("Helvetica", 10), bg="#f0e6d6").pack(side="bottom", pady=10)

# Run the app
root.mainloop()
