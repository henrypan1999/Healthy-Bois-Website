from .Booking import Booking
from .HealthCentre import HealthCentre
from .User import Patient, Provider
from .Rating import Rating
from .Note import Note
from utils.flaskhelpers import flash
from datetime import datetime, date, time
import copy



class UserManager:
    def __init__(self):
        self._patients = []
        self._providers = []

    @property
    def patients(self):
        return self._patients

    def add_multiple_patients(self, patients):                #centres is a list / mainly for csv
        for c in patients:
            self._patients.append(c)

    def add_patient(self, patient):
        self._patients.append(patient)

    @property
    def providers(self):
        return self._providers

    def add_multiple_providers(self, providers):                #centres is a list / mainly for csv
        for c in providers:
            self._providers.append(c)

    def add_provider(self, provider):
        self._provider.append(provider)

    def get_HP_by_username(self, username):
        for c in self._providers:
            if c.username == username:
                return c

    def get_Patient_by_username(self, username):
        for c in self._patients:
            if c.username == username:
                return c

    def get_HP_by_name(self, name):
        for c in self._providers:
            if c.name == name:
                return c

    def get_Patient_by_name(self, name):
        for c in self._patients:
            if c.name == name:
                return c

    def get_notes(self, notes):
        for n in notes:
            for p in self.patients:
                if p.name == n[4]:
                    p.add_note(
                        Note(
                            self.get_HP_by_name(n[0]),
                            n[1],
                            n[2],
                            datetime.strptime(n[3], "%Y-%m-%d %H:%M:%S")
                        )
                    )
                    break
