from dataclasses import dataclass, field


@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    diagnosis: str
    doctor: str = "Not assigned"
    charges: float = 0.0


class Hospital:
    def __init__(self):
        self.patients = {}
        self.next_patient_id = 1

    def admit_patient(self, name, age, diagnosis):
        if not name.strip():
            raise ValueError("Patient name cannot be empty.")
        if age <= 0:
            raise ValueError("Patient age must be greater than zero.")

        patient = Patient(self.next_patient_id, name.strip(), age, diagnosis.strip())
        self.patients[patient.patient_id] = patient
        self.next_patient_id += 1
        print(f"Admitted {patient.name}. Patient ID: {patient.patient_id}")
        return patient

    def assign_doctor(self, patient_id, doctor_name):
        patient = self._get_patient(patient_id)
        if not doctor_name.strip():
            raise ValueError("Doctor name cannot be empty.")
        patient.doctor = doctor_name.strip()
        print(f"Dr. {patient.doctor} assigned to {patient.name}.")
        return patient

    def generate_bill(self, patient_id, daily_rate, days, treatment_charges=0.0):
        patient = self._get_patient(patient_id)
        if daily_rate < 0 or treatment_charges < 0 or days < 0:
            raise ValueError("Rates, days, and charges cannot be negative.")

        patient.charges = daily_rate * days + treatment_charges
        print(
            f"Bill for {patient.name} (ID {patient.patient_id}): "
            f"${patient.charges:.2f}"
        )
        return patient.charges

    def patient_summary(self, patient_id):
        patient = self._get_patient(patient_id)
        summary = (
            f"Patient ID: {patient.patient_id}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Diagnosis: {patient.diagnosis or 'Not provided'}\n"
            f"Doctor: {patient.doctor}\n"
            f"Current bill: ${patient.charges:.2f}"
        )
        print(summary)
        return summary

    def print_patients(self):
        if not self.patients:
            print("No patients have been admitted.")
            return

        print("Patient list:")
        for patient in self.patients.values():
            print(
                f"{patient.patient_id}: {patient.name} | Age: {patient.age} | "
                f"Doctor: {patient.doctor}"
            )

    def _get_patient(self, patient_id):
        try:
            return self.patients[int(patient_id)]
        except (KeyError, ValueError):
            raise ValueError(f"No patient found with ID {patient_id}.") from None


def main():
    hospital = Hospital()
    actions = {
        "1": "Admit a patient",
        "2": "Assign a doctor",
        "3": "Generate a bill",
        "4": "Show patient summary",
        "5": "Print patient list",
        "0": "Exit",
    }

    while True:
        print("\nHospital Patient Management")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                hospital.admit_patient(
                    input("Patient name: "),
                    int(input("Age: ")),
                    input("Diagnosis: "),
                )
            elif choice == "2":
                hospital.assign_doctor(
                    input("Patient ID: "), input("Doctor name: ")
                )
            elif choice == "3":
                hospital.generate_bill(
                    input("Patient ID: "),
                    float(input("Daily rate: $")),
                    int(input("Number of days: ")),
                    float(input("Treatment charges: $")),
                )
            elif choice == "4":
                hospital.patient_summary(input("Patient ID: "))
            elif choice == "5":
                hospital.print_patients()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Please choose a listed option.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
