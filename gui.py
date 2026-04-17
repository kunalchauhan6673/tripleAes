import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

from crypto_utils import encrypt_file, decrypt_file
from auth import login, signup

selected_file = ""
current_user = None


# ================= FILE =================
def select_file():
    global selected_file
    file = filedialog.askopenfilename()
    if file:
        selected_file = file
        file_label.config(text=os.path.basename(file))
        show_preview(file)


def show_preview(path):
    try:
        filename = os.path.basename(path)

        if filename.startswith("encrypted_"):
            preview_label.config(image="", text="Encrypted File - No Preview")
            preview_label.image = None
            return

        if path.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(path)
            img = img.resize((180, 180))
            img = ImageTk.PhotoImage(img)

            preview_label.config(image=img, text="")
            preview_label.image = img
        else:
            preview_label.config(image="", text="No Preview Available")

    except:
        preview_label.config(image="", text="Preview Error")


# ================= ENCRYPT =================
def encrypt():
    if not selected_file:
        messagebox.showerror("Error", "No file selected")
        return

    if use_account_var.get():
        password = current_user + password_entry.get()
    else:
        password = password_entry.get()

    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters")
        return

    try:
        progress['value'] = 30
        root.update_idletasks()

        path = encrypt_file(selected_file, password)

        progress['value'] = 100
        messagebox.showinfo("Success", f"Encrypted:\n{path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    progress['value'] = 0


# ================= DECRYPT =================
def decrypt():
    if not selected_file:
        messagebox.showerror("Error", "No file selected")
        return

    if use_account_var.get():
        password = current_user + password_entry.get()
    else:
        password = password_entry.get()

    try:
        progress['value'] = 30
        root.update_idletasks()

        path = decrypt_file(selected_file, password)

        progress['value'] = 100
        messagebox.showinfo("Success", f"Decrypted:\n{path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    progress['value'] = 0


# ================= AUTH =================
def show_main_app():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    app_frame.pack(fill="both", expand=True)


def handle_login():
    global current_user
    u = login_user.get()
    p = login_pass.get()

    success, msg = login(u, p)
    if success:
        current_user = u
        show_main_app()
    else:
        messagebox.showerror("Error", msg)


def handle_signup():
    u = signup_user.get()
    p = signup_pass.get()

    success, msg = signup(u, p)
    if success:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", msg)


# ================= GUI =================
def run_gui():
    global root, file_label, password_entry, progress, preview_label
    global login_frame, signup_frame, app_frame
    global login_user, login_pass, signup_user, signup_pass
    global use_account_var

    root = tk.Tk()
    root.title("Secure File System")
    root.geometry("650x550")
    root.configure(bg="#1e1e1e")

    # ================= LOGIN =================
    login_frame = tk.Frame(root, bg="#1e1e1e")
    login_frame.pack(expand=True)

    login_box = tk.Frame(login_frame, bg="#2c2c2c", padx=30, pady=30)
    login_box.pack()

    tk.Label(login_box, text="Login", fg="white", bg="#2c2c2c",
             font=("Arial", 18, "bold")).pack(pady=10)

    login_user = tk.Entry(login_box, width=30)
    login_user.pack(pady=5)

    login_pass = tk.Entry(login_box, show="*", width=30)
    login_pass.pack(pady=5)

    tk.Button(login_box, text="Login", width=20,
              command=handle_login).pack(pady=10)

    tk.Button(login_box, text="Create Account",
              command=lambda: [login_frame.pack_forget(), signup_frame.pack(expand=True)]
              ).pack()

    # ================= SIGNUP =================
    signup_frame = tk.Frame(root, bg="#1e1e1e")

    signup_box = tk.Frame(signup_frame, bg="#2c2c2c", padx=30, pady=30)
    signup_box.pack()

    tk.Label(signup_box, text="Signup", fg="white", bg="#2c2c2c",
             font=("Arial", 18, "bold")).pack(pady=10)

    signup_user = tk.Entry(signup_box, width=30)
    signup_user.pack(pady=5)

    signup_pass = tk.Entry(signup_box, show="*", width=30)
    signup_pass.pack(pady=5)

    tk.Button(signup_box, text="Create Account", width=20,
              command=handle_signup).pack(pady=10)

    tk.Button(signup_box, text="Back to Login",
              command=lambda: [signup_frame.pack_forget(), login_frame.pack(expand=True)]
              ).pack()

    # ================= MAIN APP =================
    app_frame = tk.Frame(root, bg="#1e1e1e")

    container = tk.Frame(app_frame, bg="#2c2c2c", padx=20, pady=20)
    container.pack(pady=20)

    tk.Label(container, text="Secure File System",
             fg="white", bg="#2c2c2c",
             font=("Arial", 18, "bold")).pack(pady=10)

    tk.Button(container, text="Select File", width=25,
              command=select_file).pack(pady=5)

    file_label = tk.Label(container, text="No file selected",
                          fg="white", bg="#2c2c2c")
    file_label.pack(pady=5)

    preview_label = tk.Label(container, bg="#2c2c2c", fg="white")
    preview_label.pack(pady=10)

    password_entry = tk.Entry(container, show="*", width=30)
    password_entry.pack(pady=5)

    use_account_var = tk.BooleanVar()
    tk.Checkbutton(container,
                   text="Use account credentials as key",
                   variable=use_account_var,
                   bg="#2c2c2c",
                   fg="white",
                   selectcolor="#2c2c2c").pack(pady=5)

    tk.Button(container, text="Encrypt", width=20,
              bg="green", fg="white",
              command=encrypt).pack(pady=5)

    tk.Button(container, text="Decrypt", width=20,
              bg="blue", fg="white",
              command=decrypt).pack(pady=5)

    progress = ttk.Progressbar(container, length=300)
    progress.pack(pady=10)

    tk.Button(container, text="Exit",
              bg="red", fg="white",
              command=root.quit).pack(pady=10)

    root.mainloop()