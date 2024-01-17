import tkinter as tk
from tkinter import messagebox, simpledialog

# In-memory list to store patient records
patient_records = []

# Function to check login credentials
def check_login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password match registered credentials
    if username in registered_users and registered_users[username] == password:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_patient_details_window(username)  # Open patient details window after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to register a new account
def register_account():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Registration Failed", "Please enter both username and password")
    elif username in registered_users:
        messagebox.showerror("Registration Failed", "Username already exists")
    else:
        registered_users[username] = password
        messagebox.showinfo("Registration Successful", "Account created for " + username)

# Function to open the patient details window
def open_patient_details_window(username):
    details_window = tk.Toplevel(root)
    details_window.title("ELENI HEALTH CENTER - Patient Details")
    details_window.configure(bg="#c9e2f2")  # Light blue background color

    # Create and place widgets for patient details form
    title_label = tk.Label(details_window, text="ELENI HEALTH CENTER", font=("Arial", 16, "bold"), bg="#c9e2f2")  # Larger font size and bold
    title_label.pack()

    name_label = tk.Label(details_window, text="Name:", bg="#c9e2f2")  # Light blue background color
    name_label.pack()

    name_entry = tk.Entry(details_window, width=40)  # Larger width
    name_entry.pack()

    age_label = tk.Label(details_window, text="Age:", bg="#c9e2f2")
    age_label.pack()

    age_entry = tk.Entry(details_window, width=40)
    age_entry.pack()

    address_label = tk.Label(details_window, text="Address:", bg="#c9e2f2")
    address_label.pack()

    address_entry = tk.Entry(details_window, width=40)
    address_entry.pack()

    phone_label = tk.Label(details_window, text="Phone Number:", bg="#c9e2f2")
    phone_label.pack()

    phone_entry = tk.Entry(details_window, width=40)
    phone_entry.pack()

    problem_label = tk.Label(details_window, text="Select Health Problems (if any):", bg="#c9e2f2")
    problem_label.pack()

    # List of health problems
    health_problems = [
        "Fever",
        "Cough",
        "Headache",
        "Stomach pain",
        "Fatigue",
        "Other (Specify)"
    ]

    # Variable to hold selected problems
    selected_problems = []

    # Function to handle selection/deselection of health problems
    def select_problem(problem):
        if problem == "Other (Specify)":
            other_problem = simpledialog.askstring("Other Problem", "Please specify the other problem:")
            if other_problem:
                selected_problems.append(other_problem)
                problems_var.set(", ".join(selected_problems))
        elif problem in selected_problems:
            selected_problems.remove(problem)
            problems_var.set(", ".join(selected_problems))
        else:
            selected_problems.append(problem)
            problems_var.set(", ".join(selected_problems))

    # Display health problems as checkbuttons
    problems_var = tk.StringVar()
    for problem in health_problems:
        problem_check = tk.Checkbutton(details_window, text=problem, command=lambda pb=problem: select_problem(pb), bg="#c9e2f2")  # Light blue background color
        problem_check.pack()

    selected_problems_label = tk.Label(details_window, textvariable=problems_var, bg="#c9e2f2")  # Light blue background color
    selected_problems_label.pack()

    # Radio buttons for doctor appointment or buying medicine
    appointment_option_var = tk.StringVar()
    appointment_option_var.set("Meet Doctor")  # Default selection is "Meet Doctor"

    appointment_label = tk.Label(details_window, text="Select an option:", bg="#c9e2f2")
    appointment_label.pack()

    meet_doctor_button = tk.Radiobutton(details_window, text="Meet Doctor", variable=appointment_option_var, value="Meet Doctor", bg="#c9e2f2")  # Light blue background color
    meet_doctor_button.pack()

    buy_medicine_button = tk.Radiobutton(details_window, text="Buy Medicine", variable=appointment_option_var, value="Buy Medicine", bg="#c9e2f2")  # Light blue background color
    buy_medicine_button.pack()

    # Dropdown menu for medicine selection
    medicine_label = tk.Label(details_window, text="Select Medicine:", bg="#c9e2f2")  # Light blue background color
    medicine_label.pack()

    medicine_prices = {
        "Antibiotics": 15.0,
        "Anlgestics": 10.0,
        "Antipyretics": 12.0,
        "Anti-inflammatory drugs": 18.0,
        "Anticoagulants": 20.0,
        "Antihypertensives": 25.0,
        "Antidiabetic drugs": 22.0,
        "Bronchodilators": 15.0,
        "Diuretics": 18.0,
        "Antiemetics": 12.0,
        "Antipsychotics": 30.0,
        "Antivirals": 40.0,
        "Immunosuppressants": 35.0,
        "Cardiac medications": 28.0,
        "Anesthetics": 50.0,
        "Others(Specify)": 0.0
    }

    selected_medicine_var = tk.StringVar()
    selected_medicine_var.set("Medicine A")  # Default selection is the first medicine

    medicine_dropdown = tk.OptionMenu(details_window, selected_medicine_var, *medicine_prices.keys())
    medicine_dropdown.pack()

    quantity_label = tk.Label(details_window, text="Quantity:", bg="#c9e2f2")  # Light blue background color
    quantity_label.pack()

    quantity_entry = tk.Entry(details_window, width=40)
    quantity_entry.pack()

    # Button to save patient details and perform CRUD operations
    submit_button = tk.Button(details_window, text="Submit", command=lambda: handle_crud_operations(username, name_entry.get(), age_entry.get(), address_entry.get(), phone_entry.get(), selected_problems, appointment_option_var.get(), selected_medicine_var.get(), quantity_entry.get()), width=20, height=2, bg="#4285f4", fg="white")  # Larger size and blue color
    submit_button.pack()

# Function to save patient details and perform CRUD operations
def handle_crud_operations(username, name, age, address, phone, problems, appointment_option, selected_medicine, quantity):
    if appointment_option == "Buy Medicine":
        buy_medicine(username, problems, selected_medicine, quantity)
    else:
        existing_patient = find_patient_record(username)

        if existing_patient:
            update_patient_record(existing_patient, name, age, address, phone, problems, appointment_option, selected_medicine, quantity)
        else:
            create_patient_record(username, name, age, address, phone, problems, appointment_option, selected_medicine, quantity)

# Function to create a new patient record
def create_patient_record(username, name, age, address, phone, problems, appointment_option, selected_medicine, quantity):
    # Create a dictionary to represent a patient record
    patient_record = {
        "Username": username,
        "Name": name,
        "Age": age,
        "Address": address,
        "Phone": phone,
        "Health Problems": problems,
        "Appointment Option": appointment_option,
        "Selected Medicine": selected_medicine,
        "Quantity": quantity
    }

    # Add the patient record to the in-memory list
    patient_records.append(patient_record)

    messagebox.showinfo("Details Saved", f"Patient details saved for {username}: \nName: {name}\nAge: {age}\nAddress: {address}\nPhone Number: {phone}\nHealth Problems: {', '.join(problems)}\nAppointment Option: {appointment_option}\nSelected Medicine: {selected_medicine}\nQuantity: {quantity}")

# Function to update an existing patient record
def update_patient_record(existing_patient, name, age, address, phone, problems, appointment_option, selected_medicine, quantity):
    # Update the fields of the existing patient record
    existing_patient["Name"] = name
    existing_patient["Age"] = age
    existing_patient["Address"] = address
    existing_patient["Phone"] = phone
    existing_patient["Health Problems"] = problems
    existing_patient["Appointment Option"] = appointment_option
    existing_patient["Selected Medicine"] = selected_medicine
    existing_patient["Quantity"] = quantity

    messagebox.showinfo("Details Updated", f"Patient details updated for {existing_patient['Username']}: \nName: {name}\nAge: {age}\nAddress: {address}\nPhone Number: {phone}\nHealth Problems: {', '.join(problems)}\nAppointment Option: {appointment_option}\nSelected Medicine: {selected_medicine}\nQuantity: {quantity}")

# Function to find an existing patient record based on username
def find_patient_record(username):
    for record in patient_records:
        if record["Username"] == username:
            return record
    return None

# Function to handle the "Buy Medicine" option
def buy_medicine(username, problems, selected_medicine, quantity):
    messagebox.showinfo("Buy Medicine", f"Prescription for {username}: \nHealth Problems: {', '.join(problems)}\nSelected Medicine: {selected_medicine}\nQuantity: {quantity}\nPlease visit the pharmacy to purchase the prescribed medicine.")

# GUI setup
root = tk.Tk()
root.title("ELENI HEALTH CENTER")  # Title set to "ELENI HEALTH CENTER"
root.configure(bg="#c9e2f2")  # Light blue background color

# Dictionary to store registered users and passwords
registered_users = {}

# Create and place widgets
title_label = tk.Label(root, text="ELENI HEALTH CENTER", font=("Arial", 20, "bold"), bg="#c9e2f2")  # Larger font size and bold
title_label.pack()

username_label = tk.Label(root, text="Username:", bg="#c9e2f2")  # Light blue background color
username_label.pack()

username_entry = tk.Entry(root, width=40)  # Larger width
username_entry.pack()

password_label = tk.Label(root, text="Password:", bg="#c9e2f2")  # Light blue background color
password_label.pack()

password_entry = tk.Entry(root, show="*", width=40)  # Larger width
password_entry.pack()

register_button = tk.Button(root, text="Register", command=register_account, width=20, height=2, bg="#4285f4", fg="white")  # Larger size and blue color
register_button.pack()

login_button = tk.Button(root, text="Login", command=check_login, width=20, height=2, bg="#4285f4", fg="white")  # Larger size and blue color
login_button.pack()

root.mainloop()



