from .Booking import Booking
from .HealthCentre import HealthCentre
from .User import Patient, Provider
from .Rating import Rating
from utils.flaskhelpers import flash
import copy

class HealthCentreManager:
    def __init__(self):
        self._centres = []

    @property
    def centres(self):
        return self._centres

    def add_multiple_centres(self, centres):                #centres is a list / mainly for csv
        for c in centres:
            self._centres.append(c)

    def add_centre(self, centre):
        self._centres.append(centre)

    def get_HC_by_name(self, name):
        for c in self._centres:
            if c.name == name:
                return c
if __name__ == "__main__":
    from Booking import Booking
    from HealthCentre import HealthCentre
    from User import Patient, Provider
    from BookingSystem import BookingSystem
    from Rating import Rating
    #from utils.flaskhelpers import flash
    patient = Patient('user', 'pass', 'name')
    patient2 = Patient('lol', 'pass', 'name2')
    rate = Rating(patient, 5)
    rate2 = Rating(patient2, 4)
    print(rate.value)
    randwick = HealthCentre(
        "medical", "2111", "Randwick da Best Hosotail", "8888 8888", "Randwick"
    )
    randwick.add_rating(rate)
    randwick.add_rating(rate2)
    for r in randwick.ratings:
        print(r.patient)
