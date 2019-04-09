from flask import Flask
from flask_login import LoginManager
from src.AuthenticationManager import AuthenticationManager
from src.HealthCentreManager import HealthCentreManager
from src.UserManager import UserManager
from src.client import bootstrap_system
from src.User import Patient
from src.BookingSystem import BookingSystem
from src.RatingManager import RatingManager
from datetime import datetime, time
from src.Booking import Booking
from src.Rating import Rating
from src.Note import Note


from src.ReferralSystem import ReferralSystem
from app import app, auth_manager, booking_system, system, rating_manager
#   book an appointment
#   view a patient history
#   manage a patient history

#   book an appointment
def test_make_booking():
    provider = system.user_manager.get_HP_by_name('toby')
    health_centre = system.hc_manager.get_HC_by_name('Sydney Children Hospital')
    patient = system.user_manager.get_Patient_by_name('jack')
    date = '2019-05-20'
    year, month, day = date.split("-")
    booking_date = datetime(int(year), int(month), int(day))
    time1 = time(9,30)
    booking_datetime = datetime.combine(booking_date,time1)
    booking = Booking(health_centre, provider, booking_datetime, patient, "")
    assert(system.booking_system.make_booking(booking))


#   view patient history
def test_view_patient_history_past_not_none():
    patient = system.user_manager.get_Patient_by_name('jack')
    prev_apts = system.booking_system.get_user_bookings(patient, 'past')
    assert(prev_apts is not None)

def test_view_patient_history_upcoming_not_none():
    patient = system.user_manager.get_Patient_by_name('jack')
    upcoming_apts = system.booking_system.get_user_bookings(patient, "upcoming")
    assert(upcoming_apts is not None)
def test_view_patient_history_past_none():
    patient = system.user_manager.get_Patient_by_name('hao')
    prev_apts = system.booking_system.get_user_bookings(patient, 'past')
    assert(prev_apts == [])
def test_view_patient_history_upcoming_none():
    patient = system.user_manager.get_Patient_by_name('hao')
    upcoming_apts = system.booking_system.get_user_bookings(patient, "upcoming")
    assert(upcoming_apts == [])



#   check if appointment history is sorted
def test_patient_past_history_is_sorted():
    patient = system.user_manager.get_Patient_by_name('jack')
    patient_history = system.booking_system.get_user_bookings(patient,"past");
    times = []
    for x in patient_history:
        times.append(x.time)
    assert(sorted(times,reverse = True) == times)

def test_patient_upcoming_history_is_sorted():
    patient = system.user_manager.get_Patient_by_name('jack')
    patient_history = system.booking_system.get_user_bookings(patient,"upcoming");
    times = []
    for x in patient_history:
        times.append(x.time)
    assert(sorted(times,reverse = False) == times)
    
def test_provider_past_history_is_sorted():
    provider = system.user_manager.get_HP_by_name('toby')
    provider_history = system.booking_system.get_user_bookings(provider,"past");
    times = []
    for x in provider_history:
        times.append(x.time)
    assert(sorted(times,reverse = True) == times)

def test_provider_upcoming_history_is_sorted():
    provider = system.user_manager.get_HP_by_name('toby')
    provider_history = system.booking_system.get_user_bookings(provider,"upcoming");
    times = []
    for x in provider_history:
        times.append(x.time)
    assert(sorted(times,reverse = False) == times)

def test_provider_patient_notes_history_is_sorted():
    patient = system.user_manager.get_Patient_by_name('jack')
    times = []
    for x in patient.notes:
        times.append(x.datetime)
    assert(sorted(times,reverse = False) == times)

def test_login_legit():
    legit_email = 'jack@gmail.com'
    legit_password = 'cs1531'
    for patient in system.user_manager.patients:
        if legit_email == patient._username and legit_password == patient._password:
            assert(True)
            return
    assert(False)

def test_login_not_legit():
    legit_email = 'dab@gmail.com'
    legit_password = 'whip'
    for patient in system.user_manager.patients:
        if legit_email == patient._username and legit_password == patient._password:
            assert(False)
            return
    assert(True)

#   manage a patient history
def test_manage_patient_history():
    #get, add, delete?
    assert(True)

#   test rating
def test_rating():
    patient = system.user_manager.get_Patient_by_name('jack')
    assert(Rating(patient, 4))

def test_patient_notes():
    provider = system.user_manager.get_HP_by_name('toby')
    health_centre = system.hc_manager.get_HC_by_name('Sydney Children Hospital')
    patient = system.user_manager.get_Patient_by_name('jack')
    date = '2019-05-20'
    year, month, day = date.split("-")
    booking_date = datetime(int(year), int(month), int(day))
    time1 = time(9,30)
    booking_datetime = datetime.combine(booking_date,time1)
    booking = Booking(health_centre, provider, booking_datetime, patient, "Despacito")
    assert(booking.note == "Despacito")
#   test notes

def test_provider_notes():
    provider = system.user_manager.get_HP_by_name('toby')
    date = '2019-05-20'
    year, month, day = date.split("-")
    booking_date = datetime(int(year), int(month), int(day))
    time1 = time(9,30)
    booking_datetime = datetime.combine(booking_date,time1)
    new_note = Note(
                    provider, "Concurrent Despacito", "Despacito", booking_datetime
                )
    assert(new_note.medication == "Despacito")