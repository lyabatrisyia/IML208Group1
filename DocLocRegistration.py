import tkinter as tk
from tkinter import ttk

class LocumDoctorRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Locum Doctor Registration System")

        # Initialize variables
        self.doctors = []
        self.current_doctor_index = tk.StringVar()

        # Create GUI elements
        self.create_gui()

    def create_gui(self):
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.root, text="Specialization:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # Entry Widgets
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.specialization_entry = tk.Entry(self.root)
        self.specialization_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Doctor", command=self.add_doctor).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Update Doctor", command=self.update_doctor).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete Doctor", command=self.delete_doctor).grid(row=4, column=0, columnspan=2, pady=10)

        # Doctor Listbox
        self.doctor_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.doctor_listbox.grid(row=5, column=0, columnspan=2, pady=10)
        self.doctor_listbox.bind('<<ListboxSelect>>', self.load_doctor_data)

        # Populate the listbox with existing doctors
        self.update_doctor_listbox()

    def add_doctor(self):
        name = self.name_entry.get()
        specialization = self.specialization_entry.get()

        if name and specialization:
            doctor = {"Name": name, "Specialization": specialization}
            self.doctors.append(doctor)
            self.update_doctor_listbox()
            self.clear_entries()

    def update_doctor(self):
        selected_index = self.get_selected_index()
        if selected_index is not None:
            name = self.name_entry.get()
            specialization = self.specialization_entry.get()
            if name and specialization:
                self.doctors[selected_index]["Name"] = name
                self.doctors[selected_index]["Specialization"] = specialization
                self.update_doctor_listbox()
                self.clear_entries()

    def delete_doctor(self):
        selected_index = self.get_selected_index()
        if selected_index is not None:
            del self.doctors[selected_index]
            self.update_doctor_listbox()
            self.clear_entries()

    def load_doctor_data(self, event):
        selected_index = self.get_selected_index()
        if selected_index is not None:
            doctor = self.doctors[selected_index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, doctor["Name"])
            self.specialization_entry.delete(0, tk.END)
            self.specialization_entry.insert(0, doctor["Specialization"])

    def update_doctor_listbox(self):
        self.doctor_listbox.delete(0, tk.END)
        for doctor in self.doctors:
            self.doctor_listbox.insert(tk.END, doctor["Name"])

    def get_selected_index(self):
        selected_index = self.doctor_listbox.curselection()
        if selected_index:
            return selected_index[0]
        return None

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.specialization_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LocumDoctorRegistrationSystem(root)
    root.mainloop()
