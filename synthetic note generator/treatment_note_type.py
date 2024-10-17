# treatment_note_type.py
from note import BaseNote
from datetime import date
from data_elements import *

class TreatmentSummary(BaseNote):
    def __init__(self, patient):
        super().__init__()
        self.note_type = 'treatment_summary'
        self.patient = patient
        self.plan = self.generate_treatment_plan()
        self.outcome = self.generate_treatment_outcome()
        self.follow_up = self.generate_follow_up_plan()

    def generate_note(self):
        self.note_text = ""
        self.note_text += self.get_header()
        self.note_text += self.treatment_summary()
        self.note_text += self.treatment_plan()
        self.note_text += self.treatment_outcome()
        self.note_text += self.follow_up_plan()
        self.note_text += self.get_footer()
        return self.note_text

    def treatment_summary(self):
        return (f"\nTreatment Summary:\n"
                f"Patient Name: {self.patient.name}\n"
                f"Diagnosis: {self.patient.diagnosis}\n"
                f"Treatment Initiated: {self.plan}\n"
                f"Current Condition: {self.patient.condition}\n"
                f"Outcome: {self.outcome}\n")

    def treatment_plan(self):
        return (f"\nTreatment Plan:\n"
                f"The patient was treated with {self.plan} based on the clinical assessment of {self.patient.condition}.\n")

    def treatment_outcome(self):
        return (f"\nTreatment Outcome:\n"
                f"The patient's response to treatment has been classified as: {self.outcome}.\n"
                f"Further follow-up will monitor for any signs of recurrence or progression.")

    def follow_up_plan(self):
        return (f"\nFollow-up Plan:\n"
                f"Next scheduled follow-up: {self.follow_up}\n"
                f"Additional tests or evaluations to be conducted during the follow-up to assess the patient's ongoing condition.")

    def generate_treatment_plan(self):
        diagnosis = self.patient.diagnosis
        condition = self.patient.condition

        if diagnosis == 'Cancer':
            if condition == 'Early Stage':
                return "Surgery and chemotherapy"
            elif condition == 'Advanced Stage':
                return "Surgery, chemotherapy, and radiation"
            else:
                return "Unknown treatment plan"
        elif diagnosis == 'Infection':
            if condition == 'Mild':
                return "Antibiotics"
            elif condition == 'Severe':
                return "Antibiotics and hospitalization"
            else:
                return "Unknown treatment plan"
        else:
            return "Unknown treatment plan"

    def generate_treatment_outcome(self):
        response = self.patient.response_to_treatment

        if response == 'Excellent':
            return "Complete remission"
        elif response == 'Good':
            return "Partial remission"
        elif response == 'Fair':
            return "Stable disease"
        elif response == 'Poor':
            return "Progressive disease"
        else:
            return "Unknown treatment outcome"

    def generate_follow_up_plan(self):
        return "Follow-up appointment in 3 months"

    def get_header(self):
        return ("Clinical Note\n"
                "-------------------------------\n"
                f"Date: {date.today()}\n"
                "Provider: Dr. Smith\n"
                "-------------------------------\n")

    def get_footer(self):
        return "\n-------------------------------\nEnd of Clinical Note"

    def print_note(self):
        print(self.generate_note())

# Create a Patient object
class Patient:
    def __init__(self, name, diagnosis, condition, response_to_treatment):
        self.name = name
        self.diagnosis = diagnosis
        self.condition = condition
        self.response_to_treatment = response_to_treatment

# Create a TreatmentSummary object and print the note
patient = Patient(name='John Doe', diagnosis='Cancer', condition='Early Stage', response_to_treatment='Excellent')
treatment_summary = TreatmentSummary(patient)
treatment_summary.print_note()
