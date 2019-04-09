from .Booking import Booking
from .HealthCentre import HealthCentre
from .User import Patient, Provider
from .Rating import Rating
from utils.flaskhelpers import flash
from .CSVLoader import CSVLoader
import copy

class RatingManager:
    """rating manager simply adds ratings to UserManager and HealthCentreManager"""
    def __init__(self, root_path):
        self._root_path = root_path

    @property
    def root_path(self):
        return self._root_path

    def add_rating(self, rating, patient, name, system):
        bookings = system.booking_system.get_user_bookings(patient, "past")
        loader = CSVLoader(self.root_path)
        for b in bookings:
            if b.HC == name or b.HP == name: # checks both centre and provider
                flash("Rating submitted.")
                if b.HC == name:
                    rate_type = 'centre'
                else:
                    rate_type = 'provider'
                # iterate in csv file to check for previous ratings, and re-rate.
                for r in name.ratings: # centre
                    if r.patient == patient:
                        r.value = rate.value
                        flash('Changed Rating - Previously Rated')
                        return rate_type
                name.add_rating(rate)
                flash('Added Rating')
                return rate_type
        flash("Failed to submit rating - Never booked.")
        return "failure"

    def add_multiple_ratings(self, user_manager, hc_manager, ratings):
        """This function adds multiple ratings from the CSV to a program recognised format."""
        for r in ratings:
            rate = Rating(user_manager.get_Patient_by_username(r[2]), float(r[3]))
            if r[0] == "provider":
                name = user_manager.get_HP_by_name(r[1])
            else:
                name = hc_manager.get_HC_by_name(r[1])

            name.add_rating(rate)
