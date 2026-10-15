"""A simple command-line application for managing hospital patients."""

from dataclasses import dataclass, field


@dataclass
class Patient:
    """Store the identifying and billing information for one patient."""

    patient_id: int
    name: str
    age: int
    diagnosis: str
    doctor: str = "Not assigned"
    charges: float = 0.0


class Hospital:
    """Manage patient admissions, doctor assignments, and billing."""

    def __init__(self):
        # Records are kept in memory and are cleared when the program exits.
        self.patients = {}
        self.next_patient_id = 1

    def admit_patient(self, name, age, diagnosis):
        """Admit a patient and return their new Patient record.

        Args:
            name: The patient's full name.
            age: The patient's age in years; must be greater than zero.
            diagnosis: A short description of the patient's condition.

        Raises:
            ValueError: If the name is empty or the age is not positive.
        """
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
        """Assign a doctor to an admitted patient and return the updated record.

        Args:
            patient_id: The ID given to the patient during admission.
            doctor_name: The assigned doctor's name.

        Raises:
            ValueError: If the patient does not exist or the doctor's name is empty.
        """
        patient = self._get_patient(patient_id)
        if not doctor_name.strip():
            raise ValueError("Doctor name cannot be empty.")
        patient.doctor = doctor_name.strip()
        print(f"Dr. {patient.doctor} assigned to {patient.name}.")
        return patient

    def generate_bill(self, patient_id, daily_rate, days, treatment_charges=0.0):
        """Calculate, save, and display a patient's bill total.

        Args:
            patient_id: The ID given to the patient during admission.
            daily_rate: The hospital charge for one day of stay.
            days: The number of days to include in the bill.
            treatment_charges: Additional charges for treatment (defaults to 0).

        Returns:
            The total bill amount.

        Raises:
            ValueError: If the patient does not exist or any amount/count is negative.
        """
        patient = self._get_patient(patient_id)
        if daily_rate < 0 or treatment_charges < 0 or days < 0:
            raise ValueError("Rates, days, and charges cannot be negative.")

        # The bill combines the stay cost with any additional treatment charges.
        patient.charges = daily_rate * days + treatment_charges
        print(
            f"Bill for {patient.name} (ID {patient.patient_id}): "
            f"${patient.charges:.2f}"
        )
        return patient.charges

    def patient_summary(self, patient_id):
        """Print and return a readable summary for one patient.

        Args:
            patient_id: The ID given to the patient during admission.

        Returns:
            A multiline string containing the patient's details and current bill.

        Raises:
            ValueError: If no patient has the supplied ID.
        """
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
        """Print a compact list of all admitted patients."""
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
        """Find a patient by ID or raise ValueError when the ID is unknown."""
        try:
            return self.patients[int(patient_id)]
        except (KeyError, ValueError):
            raise ValueError(f"No patient found with ID {patient_id}.") from None


def main():
    """Run the interactive menu and dispatch choices to Hospital methods."""
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
