from os.path import join
from .Booking import Booking
from .HealthCentre import HealthCentre
from .User import Patient, Provider
from .CSVLoader import CSVLoader
from .HealthCentreManager import HealthCentreManager

from operator import attrgetter
from copy import copy
from datetime import datetime, date, time


class BookingSystem:
    def __init__(self):
        self._bookings = []

    @property
    def bookings(self):
        return self._bookings

    # iteration 2 methods for CRC, book

    # Book Appointment 1
    # Input: healthcentre(object), healthprovider(object), time(object - however u want to store it), name(string - name of user - may be deleted later), user((object) - in this case, user is always the patient)
    # Output: even though it returns the booking, NO NEED TO RETURN - like code below
    def make_booking(self, new_booking):
        self._bookings.append(new_booking)
        return new_booking

    # Book Appointment Multiple #recent change
    def make_multiple_bookings(self, bookings, hc_manager, user_manager):
        for b in bookings:
            self._bookings.append(
                Booking(
                    hc_manager.get_HC_by_name(b[1]),
                    user_manager.get_HP_by_username(b[2]),
                    datetime.strptime(b[3], "%Y-%m-%d %H:%M:%S"),
                    user_manager.get_Patient_by_username(b[4]),
                    b[5]
                )
            )

    # View Appointment 1
    # Input: User((object) - can be either patient or provider, works for both)
    # Output: List of all bookings(object)
    def get_user_bookings(self, user, time_filter="all"):
        """
        Takes a User object and an optional kwarg, time_filter, to list appointments
        associated with that user. time_filter="upcoming" lists only appointments in the
        future, and time_filter="past" lists only appointments in the past.
        """
        user_filters = {
            "patient": Booking.is_patient,
            "provider": Booking.is_provider,
        }
        time_filters = {
            "all": return_true,
            "upcoming": Booking.has_not_past,
            "past": Booking.has_past,
        }

        assert(user.usertype in user_filters and time_filter in time_filters)
        user_filter = user_filters[user.usertype]
        time_filter = time_filters[time_filter]

        return sorted(
            [x for x in self._bookings if user_filter(x, user) and time_filter(x)],
            key=attrgetter("time"),
            reverse=(time_filter == Booking.has_past),
        )

    def booking_availabilities(self, provider, Datetime):
        bookings = self.get_user_bookings(provider)
        day = Datetime.day
        year = Datetime.year
        month = Datetime.month
        d = date(year, month, day)
        all_bookings = []
        for i in range(24):
            t = time(i, 00)
            n = datetime.combine(d, t)
            all_bookings.append(n)
            t = time(i, 30)
            n = datetime.combine(d, t)
            all_bookings.append(n)
        for b in bookings:
            for i in all_bookings:
                if b.time == i:
                    all_bookings.remove(i)
                    break

        new_allbookings = []
        for i in all_bookings:
            new = str(i.strftime("%H:%M"))
            new_allbookings.append(new)

        return new_allbookings

    def edit_booking_notes(self, new_booking, notes):
        for old_booking in self._bookings:
            if new_booking == old_booking:
                old_booking.notes = notes
        return

    def get_booking_by_id(self, id, user=None):
        """
        Gets a booking from the system with provided ID. Optionally, if a user object is
        specified, get_booking_by_id() will only return the booking if that user is
        the provider for the specific booking.
        """
        # Validation
        for booking in self.bookings:
            if booking.ID == id:
                if user is None:
                    return booking
                if booking.is_provider(user):
                    return booking
                return None


def return_true(*args, **kwargs):
    """Placeholder function that accepts any amount of args and always returns True"""
    return True


"""
Properties
"""

if __name__ == "__main__":

    chris = Patient("email", "pass", "chris")
    jennifer = Provider("email", "pass", "Pathologist", "jennifer")
    randwick = HealthCentre(
        "2111", "Randwick da Best Hosotail", "8888 8888", "Randwick"
    )
    carlingford = HealthCentre(
        "2111", "Carlo da Best Hospitail", "8888 8888", "Carlingford"
    )

    new_book_system = BookingSystem()
    pass
