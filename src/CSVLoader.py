import csv
from os.path import join
from csv import DictReader
from src.User import Patient, Provider
from src.HealthCentre import HealthCentre
from src.Booking import Booking #changed
from src.HealthCentreManager import HealthCentreManager #changed
from src.UserManager import UserManager #changed
from src.Rating import Rating
from src.Note import Note

class CSVLoader:
    """
    CSVLoader takes the root_path of the package as an argument and loads in the CSVs
    required for the operation of HealthCareSystem.
    """

    def __init__(self, root_path):
        self._root_path = root_path
        self._patients = []
        self._providers = []
        self._centres = []
        self._affiliations = []
        self._booking = [] 
        self._ratings = []
        self._HP_note = []
        self._load()

    def _load(self):
        """
        Internal function that calls the relevant loaders after it's set up
        the Reader object.
        """
        dbs = [
            (self._load_patients, "csv/patient.csv"),
            (self._load_providers, "csv/provider.csv"),
            (self._load_centres, "csv/health_centres.csv"),
            (self._load_affiliations, "csv/provider_health_centre.csv"),
            (self._load_booking, "csv/booking.csv"),
            (self._load_rating, "csv/rating.csv"),
            (self._load_HP_note, "csv/provider_notes.csv"),
        ]
        for loader, csv_path in dbs:
            full_path = join(self._root_path, csv_path)
            with open(full_path, "r", encoding="utf-8") as fin:
                reader = DictReader(fin)
                loader(reader)

    def get_dict(self):
        """
        get_dict() provides a dict representation of the CSVs loaded.
        "patients" provides a list of src.User.Patient objects
        "providers" provides a list of src.User.Provider objects
        "centres" provides a list of src.HealthCentre.HealthCentre objects
        "affiliations" provides a list of
            (src.HealthCentre.HealthCentre.name, src.User.Provider.username) tuples
        """
        return {
            "patients": self._patients,
            "providers": self._providers,
            "centres": self._centres,
            "affiliations": self._affiliations,
            "booking": self._booking,
            "ratings":self._ratings,
            "HP_notes":self._HP_note
        }

    def _load_patients(self, reader):
        """Load Patients from CSVReader object"""
        for row in reader:
            self._patients.append(
                Patient(
                    row["patient_email"],
                    row["password"],
                    row["patient_email"].split("@")[0],
                )
            )

    def _load_centres(self, reader):
        """Load HealthCentres from CSVReader object"""
        for row in reader:
            self._centres.append(
                HealthCentre(
                    row["centre_type"],
                    row["abn"],
                    row["name"],
                    row["phone"],
                    row["suburb"],
                )
            )

    def _load_providers(self, reader):
        """Load Providers from CSVReader object"""
        for row in reader:
            self._providers.append(
                Provider(
                    row["provider_email"],
                    row["password"],
                    row["provider_type"],
                    row["provider_email"].split("@")[0],
                )
            )

    def _load_affiliations(self, reader):
        """
        Creates a list of (health_centre_name, provider_email)
        tuples from a CSVReader object.
        """
        for row in reader:
            self._affiliations.append(
                (row["health_centre_name"], row["provider_email"])
            )

    def _load_booking(self, reader):
        """Loads Bookings from booking.csv."""
        for row in reader:
            self._booking.append(
                [
                    row["id"],
                    row["hc"],
                    row["hp"],
                    row["time"],
                    row["user"],
                    row["note"],
                ]
            )

    def _load_rating(self, reader):
        """
        Loads up all the ratings from rating.csv, ordering them into
        their proper arrays.
        """
        for row in reader:
            self._ratings.append(
                [
                    row["type"],
                    row["name"],
                    row["patient"],
                    row["rating"],
                ]
            )
            
    def _load_HP_note(self, reader):
        """
        Loads all the notes that have been written by the providers
        """
        for row in reader:
            self._HP_note.append(
                [
                    row["provider"],
                    row["note"],
                    row["medication"],
                    row["time"],
                    row["patient"],
                ]
            )
               
    """This part writes bookings into a csv file to be accessed again"""
    def write_booking(self, booking):
        full_path = join(self._root_path, 'csv/booking.csv')
        with open(full_path, 'a') as bookings:
            fieldnames = ['id', 'hc', 'hp', 'time', 'user', 'notes']
            writer = csv.DictWriter(bookings, fieldnames=fieldnames)
            writer.writerow({
                'id': booking.ID,
                'hc': booking.HC.name,
                'hp': booking.HP.username,
                'time': booking.time,
                'user': booking.user.username,
                'notes': booking.note,
                })

    """This part adds a new rating to a provider or hc"""
    def add_rating(self, rate, rate_type, name):
        full_path = join(self._root_path, 'csv/rating.csv')
        with open(full_path,'a') as ratings:
            fieldnames = ['type','name','patient','rating']
            writer = csv.DictWriter(ratings, fieldnames=fieldnames)
            writer.writerow({
                'type':rate_type,
                'name':name.name,
                'patient':rate.patient.username,
                'rating':str(rate.value),
                })

    """
    This part deletes an old rating from the csv file. It is to be used
    in conjuction with add_rating
    """
    def remove_rating(self, name, patient):
        temp_ratings = []
        full_path = join(self._root_path, 'csv/rating.csv')
        with open(full_path,'r') as ratings:
            reader = csv.DictReader(ratings)
            for row in reader:
                if row['name'] != name.name or row['patient'] != patient.username:
                    temp_ratings.append(
                        [
                            row['type'],
                            row['name'],
                            row['patient'],
                            row['rating']
                        ]
                    )
        with open(full_path,'w') as ratings:
            fieldnames = ['type','name','patient','rating']
            writer = csv.DictWriter(ratings, fieldnames=fieldnames)
            writer.writerow({ # this rewrites the headers.
                'type':'type',
                'name':'name',
                'patient':'patient',
                'rating':'rating',
                })
            for rating in temp_ratings:
                writer.writerow({
                    'type':rating[0],
                    'name':rating[1],
                    'patient':rating[2],
                    'rating':rating[3],
                    })

    def write_HP_notes(self, note, patient):
        full_path = join(self._root_path, 'csv/provider_notes.csv')
        with open(full_path,'a') as notes: 
            fieldnames = ['provider','note','medication','time','patient']
            writer = csv.DictWriter(notes, fieldnames=fieldnames)
            writer.writerow({
                'provider':note.provider.name,
                'note':note.note,
                'medication':note.medication,
                'time':note.datetime,
                'patient':patient.name
            })
