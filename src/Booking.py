from datetime import datetime, timedelta


class Booking(object):
    __id = -1  # must alter id so that it continues flow.

    def __init__(self, HC, HP, time, user, note=None):
        self._id = self._generate_id()
        self._HC = HC
        self._HP = HP
        self._time = time
        self._user = user
        self._has_past = False
        self._note = note

    @property
    def note(self):
        """
        Returns the note stored in the Booking object. If the note is an empty string
        or None, returns the string "Nil".
        """
        if self._note:
            return self._note
        return "Nil"

    @property
    def note_newline_delimited(self):
        return self.note.split("\n")

    @property
    def name(self):
        return self.user.name

    @property
    def user(self):
        return self._user

    @property
    def ID(self):
        return self._id

    @property
    def HC(self):
        return self._HC

    @property
    def HP(self):
        return self._HP

    @property
    def time(self):
        """
        Returns the starting date and time of a booking as a raw datetime object.
        """
        return self._time

    @property
    def fmt_time(self):
        """
        Returns the starting date and time of a booking as a string with the appropriate
        date and time representation.
        """
        return self._time.strftime("%c")

    def has_past(self):
        """
        Provides a boolean indicating if the booking should have already elapsed assuming
        they'd always end 30 minutes after the start time.
        Small optimization to only compare with the current time if it's known to have
        been passed.
        """
        if not self._has_past:
            has_past = (self.time + timedelta(minutes=30)) < (datetime.now())
            self._has_past = has_past
            return has_past
        return True

    def has_not_past(self):
        """
        Provides a boolean indicating if the booking should have already elapsed assuming
        they'd always end 30 minutes after the start time.
        Small optimization to only compare with the current time if it's known to have
        been passed.
        """
        return not self.has_past()

    def is_provider(self, user):
        """
        Takes a user object and returns True if that user is a provider for this booking.
        """
        return user.ID == self.HP.ID

    def is_patient(self, user):
        """
        Takes a user object and returns True if that user is a patient for this booking.
        """
        return user.ID == self.user.ID

    def _generate_id(self):
        Booking.__id += 1
        return Booking.__id

    def __str__(self):
        return f"Booking for ID: {self.ID} for {self.name} by {self.HP.name} at {self.time}, {self.HC.name}"
