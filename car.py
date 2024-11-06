import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
# Database setup
def setup_database():
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cars (
            car_id INTEGER PRIMARY KEY,
            make TEXT,
            model TEXT,
            year INTEGER,
            price_per_day REAL,
            available INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rentals (
            rental_id INTEGER PRIMARY KEY,
            car_id INTEGER,
            customer_id INTEGER,
            rental_date TEXT,
            return_date TEXT,
            total_amount REAL,
            damage_cost REAL,
            FOREIGN KEY(car_id) REFERENCES Cars(car_id),
            FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
        )
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO Users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
    ''')
    
    conn.commit()
    conn.close()

# Basic Database functions
def validate_user(username, password, role):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM Users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user and user[0] == role:
        return user[0]
    return None

def register_user(username, password):
    role = 'user'
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def view_cars():
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cars WHERE available=1')
    cars = cursor.fetchall()
    conn.close()
    return cars

def add_car(make, model, year, price_per_day):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Cars (make, model, year, price_per_day, available) VALUES (?, ?, ?, ?, 1)', (make, model, year, price_per_day))
    conn.commit()
    conn.close()

def view_customers():
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    conn.close()
    return customers

def add_customer(name, phone, email):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Customers (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    conn.close()

def rent_car(car_id, customer_id, rental_date, return_date, total_amount):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Rentals (car_id, customer_id, rental_date, return_date, total_amount) VALUES (?, ?, ?, ?, ?)', 
                   (car_id, customer_id, rental_date, return_date, total_amount))
    conn.commit()
    conn.close()

def view_rentals(customer_id):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Rentals WHERE customer_id=?', (customer_id,))
    rentals = cursor.fetchall()
    conn.close()
    return rentals

def return_car(rental_id, damage_cost):
    conn = sqlite3.connect('car_rental_system.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Rentals SET return_date=?, damage_cost=? WHERE rental_id=?', 
                   (str(datetime.now().date()), damage_cost, rental_id))
    conn.commit()
    conn.close()

# Tkinter functions for GUI interactions
def view_cars_gui():
    car_window = tk.Toplevel()
    car_window.title("Available Cars")
    car_window.configure(bg="#f0f8ff")
    cars = view_cars()
    for car in cars:
        tk.Label(car_window, text=str(car), bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    tk.Button(car_window, text="Back", command=car_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

def show_add_car_window():
    add_car_window = tk.Toplevel()
    add_car_window.title("Add a Car")
    add_car_window.configure(bg="#f0f8ff")
    
    tk.Label(add_car_window, text="Make", bg="#f0f8ff").pack(pady=5)
    make_entry = tk.Entry(add_car_window)
    make_entry.pack(pady=5)
    
    tk.Label(add_car_window, text="Model", bg="#f0f8ff").pack(pady=5)
    model_entry = tk.Entry(add_car_window)
    model_entry.pack(pady=5)
    
    tk.Label(add_car_window, text="Year", bg="#f0f8ff").pack(pady=5)
    year_entry = tk.Entry(add_car_window)
    year_entry.pack(pady=5)
    
    tk.Label(add_car_window, text="Price per Day", bg="#f0f8ff").pack(pady=5)
    price_entry = tk.Entry(add_car_window)
    price_entry.pack(pady=5)
    
    def submit_add_car():
        make = make_entry.get()
        model = model_entry.get()
        year = int(year_entry.get())
        price_per_day = float(price_entry.get())
        add_car(make, model, year, price_per_day)
        messagebox.showinfo("Success", "Car added successfully")
        add_car_window.destroy()
    
    tk.Button(add_car_window, text="Add Car", command=submit_add_car, bg="#4CAF50", fg="white").pack(pady=10)

def show_modify_car_window():
    modify_car_window = tk.Toplevel()
    modify_car_window.title("Modify/Delete a Car")
    modify_car_window.configure(bg="#f0f8ff")
    
    tk.Label(modify_car_window, text="Car ID to Modify/Delete", bg="#f0f8ff").pack(pady=5)
    car_id_entry = tk.Entry(modify_car_window)
    car_id_entry.pack(pady=5)
    
    def delete_car():
        car_id = int(car_id_entry.get())
        conn = sqlite3.connect('car_rental_system.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Cars WHERE car_id=?', (car_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car deleted successfully.")
        modify_car_window.destroy()

    tk.Button(modify_car_window, text="Delete Car", command=delete_car, bg="#FF9800", fg="white").pack(pady=10)

    # Back button
    tk.Button(modify_car_window, text="Back", command=modify_car_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

def view_customers_gui():
    customer_window = tk.Toplevel()
    customer_window.title("View Customers")
    customer_window.configure(bg="#f0f8ff")
    customers = view_customers()
    for customer in customers:
        tk.Label(customer_window, text=str(customer), bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    tk.Button(customer_window, text="Back", command=customer_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

def show_add_customer_window():
    add_customer_window = tk.Toplevel()
    add_customer_window.title("Add Customer")
    add_customer_window.configure(bg="#f0f8ff")
    
    tk.Label(add_customer_window, text="Name", bg="#f0f8ff").pack(pady=5)
    name_entry = tk.Entry(add_customer_window)
    name_entry.pack(pady=5)
    
    tk.Label(add_customer_window, text="Phone", bg="#f0f8ff").pack(pady=5)
    phone_entry = tk.Entry(add_customer_window)
    phone_entry.pack(pady=5)
    
    tk.Label(add_customer_window, text="Email", bg="#f0f8ff").pack(pady=5)
    email_entry = tk.Entry(add_customer_window)
    email_entry.pack(pady=5)
    
    def submit_add_customer():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        add_customer(name, phone, email)
        messagebox.showinfo("Success", "Customer added successfully")
        add_customer_window.destroy()
    
    tk.Button(add_customer_window, text="Add Customer", command=submit_add_customer, bg="#4CAF50", fg="white").pack(pady=10)

def show_rent_car_window():
    rent_car_window = tk.Toplevel()
    rent_car_window.title("Rent a Car")
    rent_car_window.configure(bg="#f0f8ff")
    
    tk.Label(rent_car_window, text="Car ID", bg="#f0f8ff").pack(pady=5)
    car_id_entry = tk.Entry(rent_car_window)
    car_id_entry.pack(pady=5)
    
    tk.Label(rent_car_window, text="Customer ID", bg="#f0f8ff").pack(pady=5)
    customer_id_entry = tk.Entry(rent_car_window)
    customer_id_entry.pack(pady=5)
    
    tk.Label(rent_car_window, text="Rental Date", bg="#f0f8ff").pack(pady=5)
    rental_date_entry = tk.Entry(rent_car_window)
    rental_date_entry.pack(pady=5)
    
    tk.Label(rent_car_window, text="Return Date", bg="#f0f8ff").pack(pady=5)
    return_date_entry = tk.Entry(rent_car_window)
    return_date_entry.pack(pady=5)

    def submit_rent_car():
        car_id = int(car_id_entry.get())
        customer_id = int(customer_id_entry.get())
        rental_date = rental_date_entry.get()
        return_date = return_date_entry.get()
        total_amount = 0  # You should calculate the total amount based on rental days and car price
        rent_car(car_id, customer_id, rental_date, return_date, total_amount)
        messagebox.showinfo("Success", "Car rented successfully")
        rent_car_window.destroy()
    
    tk.Button(rent_car_window, text="Rent Car", command=submit_rent_car, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(rent_car_window, text="Back", command=rent_car_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

def show_return_car_window():
    return_car_window = tk.Toplevel()
    return_car_window.title("Return a Car")
    return_car_window.configure(bg="#f0f8ff")
    
    tk.Label(return_car_window, text="Rental ID", bg="#f0f8ff").pack(pady=5)
    rental_id_entry = tk.Entry(return_car_window)
    rental_id_entry.pack(pady=5)
    
    tk.Label(return_car_window, text="Damage Cost (if any)", bg="#f0f8ff").pack(pady=5)
    damage_cost_entry = tk.Entry(return_car_window)
    damage_cost_entry.pack(pady=5)

    def submit_return_car():
        rental_id = int(rental_id_entry.get())
        damage_cost = float(damage_cost_entry.get())
        return_car(rental_id, damage_cost)
        messagebox.showinfo("Success", "Car returned successfully")
        return_car_window.destroy()
    
    tk.Button(return_car_window, text="Return Car", command=submit_return_car, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(return_car_window, text="Back", command=return_car_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

# Main application class
class CarRentalApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Rental Management System")
        self.master.geometry("400x300")
        self.master.configure(bg="#f0f8ff")

        tk.Label(master, text="Car Rental Management System", bg="#f0f8ff", font=("Arial", 16)).pack(pady=20)

        tk.Button(master, text="Login", command=self.show_login_window, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(master, text="Register", command=self.show_register_window, bg="#2196F3", fg="white").pack(pady=10)

    def show_login_window(self):
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.configure(bg="#f0f8ff")
        
        tk.Label(login_window, text="Username", bg="#f0f8ff").pack(pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)

        tk.Label(login_window, text="Password", bg="#f0f8ff").pack(pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        tk.Label(login_window, text="Role (admin/user)", bg="#f0f8ff").pack(pady=5)
        role_entry = tk.Entry(login_window)
        role_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get()
            if validate_user(username, password, role):
                messagebox.showinfo("Success", f"Welcome, {username}!")
                login_window.destroy()
                if role == 'admin':
                    self.show_admin_menu()
                else:
                    self.user_menu()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(login_window, text="Login", command=login, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(login_window, text="Back", command=login_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

    def show_register_window(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.configure(bg="#f0f8ff")

        tk.Label(register_window, text="Username", bg="#f0f8ff").pack(pady=5)
        username_entry = tk.Entry(register_window)
        username_entry.pack(pady=5)

        tk.Label(register_window, text="Password", bg="#f0f8ff").pack(pady=5)
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack(pady=5)

        tk.Label(register_window, text="Confirm Password", bg="#f0f8ff").pack(pady=5)
        confirm_password_entry = tk.Entry(register_window, show="*")
        confirm_password_entry.pack(pady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if password == confirm_password:
                register_user(username, password)
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Passwords do not match.")

        tk.Button(register_window, text="Register", command=register, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(register_window, text="Back", command=register_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

    def show_admin_menu(self):
        admin_window = tk.Toplevel(self.master)
        admin_window.title("Admin Menu")
        admin_window.configure(bg="#f0f8ff")

        tk.Label(admin_window, text="Admin Menu", bg="#f0f8ff", font=("Arial", 16)).pack(pady=20)
        tk.Button(admin_window, text="View Available Cars", command=view_cars_gui, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(admin_window, text="Add Car", command=show_add_car_window, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(admin_window, text="Modify/Delete Car", command=show_modify_car_window, bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(admin_window, text="View Customers", command=view_customers_gui, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(admin_window, text="Add Customer", command=show_add_customer_window, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(admin_window, text="Logout", command=admin_window.destroy, bg="#F44336", fg="white").pack(pady=10)

    def user_menu(self):
        user_window = tk.Toplevel(self.master)
        user_window.title("User Menu")
        user_window.configure(bg="#f0f8ff")

        tk.Label(user_window, text="User Menu", bg="#f0f8ff", font=("Arial", 16)).pack(pady=20)
        tk.Button(user_window, text="View Available Cars", command=view_cars_gui, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(user_window, text="Modify Personal Details", command=self.modify_personal_details, bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(user_window, text="Rent a Car", command=show_rent_car_window, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(user_window, text="View Rental History", command=self.view_rental_history_gui, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(user_window, text="Return a Car", command=show_return_car_window, bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(user_window, text="Logout", command=user_window.destroy, bg="#F44336", fg="white").pack(pady=10)

    def view_rental_history_gui(self):
        rental_window = tk.Toplevel(self.master)
        rental_window.title("Rental History")
        rental_window.configure(bg="#f0f8ff")

        tk.Label(rental_window, text="Enter Customer ID", bg="#f0f8ff").pack(pady=5)
        customer_id_entry = tk.Entry(rental_window)
        customer_id_entry.pack(pady=5)

        def show_rentals():
            customer_id = int(customer_id_entry.get())
            rentals = view_rentals(customer_id)
            for rental in rentals:
                tk.Label(rental_window, text=str(rental), bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
        
        tk.Button(rental_window, text="Show Rentals", command=show_rentals, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(rental_window, text="Back", command=rental_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

    def modify_personal_details(self):
        modify_window = tk.Toplevel(self.master)
        modify_window.title("Modify Personal Details")
        modify_window.configure(bg="#f0f8ff")

        tk.Label(modify_window, text="Customer ID", bg="#f0f8ff").pack(pady=5)
        customer_id_entry = tk.Entry(modify_window)
        customer_id_entry.pack(pady=5)

        tk.Label(modify_window, text="New Phone", bg="#f0f8ff").pack(pady=5)
        new_phone_entry = tk.Entry(modify_window)
        new_phone_entry.pack(pady=5)

        tk.Label(modify_window, text="New Email", bg="#f0f8ff").pack(pady=5)
        new_email_entry = tk.Entry(modify_window)
        new_email_entry.pack(pady=5)

        def update_details():
            customer_id = int(customer_id_entry.get())
            new_phone = new_phone_entry.get()
            new_email = new_email_entry.get()
            conn = sqlite3.connect('car_rental_system.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE Customers SET phone=?, email=? WHERE customer_id=?', (new_phone, new_email, customer_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Personal details updated successfully.")
            modify_window.destroy()

        tk.Button(modify_window, text="Update Details", command=update_details, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(modify_window, text="Back", command=modify_window.destroy, bg="#FF9800", fg="white").pack(pady=10)

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    root.geometry("800x600")
    bg_image = Image.open("C:\\vs code\\py project2\88e0c64bbd4e8646b80efdb68025a2c4.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS) 
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
   

    app = CarRentalApp(root)
root.mainloop()