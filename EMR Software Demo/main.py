import tkinter as tk
from auth import *
from tkinter import simpledialog
from datetime import datetime
import json
from tkinter import messagebox


def load_patients():
    """Loads patient data from JSON file as a list of Patient objects."""
    try:
        with open("patient_data.json", "r", encoding="utf-8") as patient_file:
            patient_data = json.load(patient_file)
            return patient_data
    except json.JSONDecodeError as e:
        print("❌ JSON format error:", e)
        return []

def save_patients(patients):
    """Saves a list of Patient objects (as dictionaries) to JSON file."""
    try:
        with open("patient_data.json", "w", encoding="utf-8") as file:
            # Assuming 'patients' is a list of dictionaries, you can directly dump it to the file
            json.dump(patients, file, indent=4)
            print("💾 Patient data saved.")
    except Exception as e:
        print("❌ Error saving patient data:", e)



patients = load_patients()
current_patient_index = None

class Page(tk.Frame):
    """Base Page class to allow for switching between pages."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class LoginPage(Page):
    """Login Page."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.logo_image = tk.PhotoImage(file="Logo.png")
        self.image_label = tk.Label(self, image=self.logo_image)
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        # Username Label & Entry
        self.username_label = tk.Label(self, text="Username")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Password Label & Entry
        self.password_label = tk.Label(self, text="Password")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Login Button
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Signup Button
        self.signup_button = tk.Button(self, text="Signup", command=self.go_to_signup)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        # Dummy login logic
        user = login(username=self.username_entry.get(), password=self.password_entry.get())
        if user:
            self.controller.show_frame(DashboardPage.__name__)
        else:
            print("Login password Incorrect")

    def go_to_signup(self):
        self.controller.show_frame(SignupPage.__name__)

class SignupPage(Page):
    """Signup Page."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # Username Label & Entry
        self.username_label = tk.Label(self, text="Username")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Password Label & Entry
        self.password_label = tk.Label(self, text="Password")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Signup Button
        self.signup_button = tk.Button(self, text="Signup", command=self.signup)
        self.signup_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Back to Login Button
        self.login_button = tk.Button(self, text="Back to Login", command=self.go_to_login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def signup(self):
        # Placeholder for signup logic
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(username, password)
        create_account(username=username, password=password)

    def go_to_login(self):
        self.controller.show_frame(LoginPage.__name__)
class DashboardPage(Page):
    """Unified Dashboard Page for all users."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Left Panel (Patient List)
        self.patient_list_frame = tk.Frame(self)
        self.patient_list_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.patient_label = tk.Label(self.patient_list_frame, text="Patients List", font=("Arial", 14))
        self.patient_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Placeholder for patient data (Patient ID, Name, Diagnosis)
        self.patient_buttons = []
        for i, patient in enumerate(patients):
            button = tk.Button(self.patient_list_frame, text=f"{patient['name']} - {patient['diagnosis']}",
                               command=lambda p=patient: self.display_patient_data_update_current(p))
            button.grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            self.patient_buttons.append(button)

        # Right Panel (Patient Details)
        self.details_frame = tk.Frame(self)
        self.details_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Patient ID and Name Box
        self.vital_signs_frame = tk.LabelFrame(self.details_frame, text="Patient Particular", padx=10, pady=10)
        self.vital_signs_frame.grid(row=0, column=0, padx= 10, pady=10, sticky= "nsew")
        self.namelabel = tk.Label(self.vital_signs_frame, text= "Name :")
        self.namelabel.grid(row=0, column=0, padx= 5, pady= 5, sticky= "w")
        self.age_label = tk.Label(self.vital_signs_frame, text="ID :")
        self.age_label.grid(row=1, column=0, padx= 5, pady= 5, sticky= "w")

        # Vital Signs Box
        self.vital_signs_frame = tk.LabelFrame(self.details_frame, text="Vital Signs History", padx=10, pady=10)
        self.vital_signs_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.bp_label = tk.Label(self.vital_signs_frame, text="Blood Pressure:")
        self.bp_label.grid(row=0, column=0, sticky="w", padx=5)
        self.bp_entry = tk.Entry(self.vital_signs_frame)
        self.bp_entry.grid(row=0, column=1, padx=5)

        self.pulse_label = tk.Label(self.vital_signs_frame, text="Pulse:")
        self.pulse_label.grid(row=1, column=0, sticky="w", padx=5)
        self.pulse_entry = tk.Entry(self.vital_signs_frame)
        self.pulse_entry.grid(row=1, column=1, padx=5)

        self.temp_label = tk.Label(self.vital_signs_frame, text="Temperature:")
        self.temp_label.grid(row=2, column=0, sticky="w", padx=5)
        self.temp_entry = tk.Entry(self.vital_signs_frame)
        self.temp_entry.grid(row=2, column=1, padx=5)

        self.update_vital_button = tk.Button(self.vital_signs_frame, text="Add/Update Vital Sign", command=self.update_vital_signs)
        self.update_vital_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.vital_signs_history = tk.Listbox(self.vital_signs_frame, width= 70)
        self.vital_signs_history.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        # Diagnosis Box
        self.diagnosis_frame = tk.LabelFrame(self.details_frame, text="Diagnosis & Other History", padx=10, pady=10)
        self.diagnosis_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.diagnosis_label = tk.Label(self.diagnosis_frame, text="Diagnosis:")
        self.diagnosis_label.grid(row=0, column=0, sticky="w", padx=5)
        self.diagnosis_entry = tk.Entry(self.diagnosis_frame, width= 30)
        self.diagnosis_entry.grid(row=0, column=1, padx=5)

        self.hopi_label = tk.Label(self.diagnosis_frame, text="HOPI (History of Present Illness):")
        self.hopi_label.grid(row=1, column=0, sticky="w", padx=5)
        self.hopi_text = tk.Text(self.diagnosis_frame, height=8)
        self.hopi_text.grid(row=1, column=1, padx=5)

        # Ward Round Notes Box
        self.ward_round_frame = tk.LabelFrame(self.details_frame, text="Ward Round Notes", padx=10, pady=10)
        self.ward_round_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.ward_round_label = tk.Label(self.ward_round_frame, text="Ward Round Notes:")
        self.ward_round_label.grid(row=0, column=0, sticky="w", padx=5)
        self.ward_round_text = tk.Text(self.ward_round_frame,height= 5)
        self.ward_round_text.grid(row=0, column=1, padx=5)

        # Bottom Buttons: Save Changes and Logout
        self.bottom_buttons_frame = tk.Frame(self)
        self.bottom_buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.save_button = tk.Button(self.bottom_buttons_frame, text="Save Changes", command=self.save_changes)
        self.save_button.pack(side="left", padx=20)

        self.logout_button = tk.Button(self.bottom_buttons_frame, text="Logout", command=self.logout)
        self.logout_button.pack(side="left", padx=20)

        self.delete_button = tk.Button(self.bottom_buttons_frame, text="Delete", command=self.delete_patient)
        self.delete_button.pack(side="left", padx=20)

        self.admit_patient = tk.Button(self.bottom_buttons_frame, text="Admit Patient", command=self.open_popup)
        self.admit_patient.pack(side="left", padx=20)



    def display_patient_data_update_current(self, patient):
        """Display selected patient data on the right side."""
        # Populate the details based on the selected patient
        global current_patient_index
        current_patient_index = patients.index(patient)
        self.bp_entry.delete(0, tk.END)
        self.pulse_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)
        self.hopi_text.delete("1.0", tk.END)
        self.ward_round_text.delete("1.0", tk.END)
        self.vital_signs_history.delete(0, tk.END)
        print(current_patient_index)

        self.namelabel["text"] = f"Name : {patients[current_patient_index]['name']}"
        self.age_label["text"] = str(patients[current_patient_index]['age'])
        self.diagnosis_entry.insert(0, patient["diagnosis"])
        self.hopi_text.insert("1.0", patient["history_of_present_illness"])
        self.ward_round_text.insert("1.0", "\n".join(patient["ward_round_notes"]))
        for vital in patients[current_patient_index]["vital_signs_history"]:
            self.vital_signs_history.insert(tk.END, str(vital))
        

    def update_vital_signs(self):
        """Update vital signs and append to history."""
        bp = self.bp_entry.get()
        pulse = self.pulse_entry.get()
        temp = self.temp_entry.get()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        vital_sign_entry = {
            "datetime": current_date,
            "BP": bp,
            "HR": pulse,
            "Temp": f"{temp} C"
            }
        patients[current_patient_index]["vital_signs_history"].append(vital_sign_entry)
        self.vital_signs_history.insert(tk.END, str(vital_sign_entry))

    def save_changes(self):
        diagnosis = self.diagnosis_entry.get()  # Get text from the diagnosis box
        hopi = self.hopi_text.get("1.0", tk.END).strip()  # Get text from HOPI box
        ward_round_notes = self.ward_round_text.get("1.0", tk.END).strip()  # Get text from ward round notes box

        # Update the current patient data with the gathered information
        patients[current_patient_index]["diagnosis"] = diagnosis
        patients[current_patient_index]["history_of_present_illness"] = hopi
        patients[current_patient_index]["ward_round_notes"] = ward_round_notes.splitlines()
        save_patients(patients=patients)

    def logout(self):
        self.controller.show_frame(LoginPage.__name__)
        self.controller.clear_username_pwd()

    def delete_patient(self):
        """Delete the currently selected patient."""
        global current_patient_index
        if current_patient_index is not None:
            patient_name = patients[current_patient_index]["name"]
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {patient_name}?")
            if confirm:
                del patients[current_patient_index]  # Remove the patient
                save_patients(patients)  # Save the updated patient list
                self.update_patient_list()  # Update the displayed list of patients
                self.clear_patient_details()  # Clear the patient details form
                messagebox.showinfo("Patient Deleted", f"{patient_name} has been deleted.")
        else:
            messagebox.showerror("Error", "No patient selected to delete.")


    def open_popup(self):
        """Open a popup window to admit a new patient."""
        popup = tk.Toplevel(self)
        popup.title("Admit New Patient")

        # Create fields for patient data entry
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Age:").grid(row=1, column=0, padx=10, pady=5)
        age_entry = tk.Entry(popup)
        age_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Diagnosis:").grid(row=2, column=0, padx=10, pady=5)
        diagnosis_entry = tk.Entry(popup)
        diagnosis_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(popup, text="HOPI:").grid(row=3, column=0, padx=10, pady=5)
        hopi_text = tk.Text(popup, height=5, width=30)
        hopi_text.grid(row=3, column=1, padx=10, pady=5)

    # Submit button to admit the patient
        def admit_patient():
            name = name_entry.get()
            age = age_entry.get()
            diagnosis = diagnosis_entry.get()
            hopi = hopi_text.get("1.0", tk.END).strip()

            # Create new patient dictionary
            new_patient = {
                "name": name,
                "age": age,
                "diagnosis": diagnosis,
                "history_of_present_illness": hopi,
                "vital_signs_history": [],
                "ward_round_notes": [],
            }

            # Add the new patient to the list
            patients.append(new_patient)

            # Save the patient data to JSON file
            save_patients(patients)

            # Update the patient list in the dashboard
            self.update_patient_list()

            # Close the popup
            popup.destroy()

        admit_button = tk.Button(popup, text="Admit Patient", command=admit_patient)
        admit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_patient_list(self):
        """Update the patient list in the dashboard."""
        # Clear existing patient buttons
        for button in self.patient_buttons:
            button.grid_forget()

        # Recreate the patient list buttons
        self.patient_buttons = []
        for i, patient in enumerate(patients):
            button = tk.Button(self.patient_list_frame, text=f"{patient['name']} - {patient['diagnosis']}",
                            command=lambda p=patient: self.display_patient_data_update_current(p))
            button.grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            self.patient_buttons.append(button)

    def clear_patient_details(self):
        """Clear the patient details form."""
        self.namelabel["text"] = "Name :"
        self.age_label["text"] = "ID :"
        self.diagnosis_entry.delete(0, tk.END)
        self.hopi_text.delete("1.0", tk.END)
        self.ward_round_text.delete("1.0", tk.END)
        self.vital_signs_history.delete(0, tk.END)



class Application(tk.Tk):
    """Main Application that controls page switching."""

    def __init__(self):
        super().__init__()

        self.title("EMR Application")
        self.geometry("1600x1000")

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")

        self.frames = {}
        for F in (LoginPage, SignupPage, DashboardPage):
            page_name = F.__name__  # Store the class name as a string
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")  # Pass the string name of the page

    def show_frame(self, page_name):
        frame = self.frames[page_name]  # Use the page name string to get the frame
        frame.tkraise()

    def clear_username_pwd(self):
        login_page = self.frames["LoginPage"]
        login_page.username_entry.delete(0)
        login_page.password_entry.delete(0)
        login_page.username_entry.focus_set()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
