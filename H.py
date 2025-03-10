import ttkbootstrap as tk
from ttkbootstrap.constants import *
from tkinter import messagebox


def on_login_click():
    username = entry_username.get()
    password = entry_password.get()

    correct_username = "admin"
    correct_password = "password123"

    if username == correct_username and password == correct_password:
        messagebox.showinfo("Login Successful", "Welcome to the application!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


root = tk.Window(themename="darkly")


root.title("Login Application")
root.geometry("400x300")


title_label = tk.Label(root, text="Login", font=("Helvetica", 20, "bold"))
title_label.pack(pady=20)


label_username = tk.Label(root, text="Username", font=("Helvetica", 12))
label_username.pack(pady=(0, 5))
entry_username = tk.Entry(root, bootstyle="success", font=("Helvetica", 12))
entry_username.pack(pady=5)


label_password = tk.Label(root, text="Password", font=("Helvetica", 12))
label_password.pack(pady=(0, 5))
entry_password = tk.Entry(root, bootstyle="success",
                          show="*", font=("Helvetica", 12))
entry_password.pack(pady=5)


login_button = tk.Button(
    root, text="Login", bootstyle=PRIMARY, command=on_login_click)
login_button.pack(pady=20)

root.mainloop()
