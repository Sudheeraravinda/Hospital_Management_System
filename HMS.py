import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection
def connect_db():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    disease TEXT)''')
    conn.commit()
    conn.close()

# Add patient
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    disease = entry_disease.get()
    
    if name and age and gender and disease:
        conn = sqlite3.connect("hospital.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)", 
                    (name, age, gender, disease))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient added successfully")
        clear_entries()
        view_patients()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# View patients
def view_patients():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

# Delete patient
def delete_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to delete")
        return
    
    patient_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient deleted successfully")
    view_patients()

# Clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    entry_disease.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("600x400")

# Labels and Entry Widgets
tk.Label(root, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)

tk.Label(root, text="Gender").grid(row=2, column=0)
combo_gender = ttk.Combobox(root, values=["Male", "Female", "Other"])
combo_gender.grid(row=2, column=1)

tk.Label(root, text="Disease").grid(row=3, column=0)
entry_disease = tk.Entry(root)
entry_disease.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Patient", command=add_patient).grid(row=4, column=0)
tk.Button(root, text="Delete Patient", command=delete_patient).grid(row=4, column=1)
tk.Button(root, text="View Patients", command=view_patients).grid(row=4, column=2)

# Treeview for displaying patients
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Gender", "Disease"), show="headings")
for col in ("ID", "Name", "Age", "Gender", "Disease"):
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=3)

# Initialize database
connect_db()
view_patients()

root.mainloop()
