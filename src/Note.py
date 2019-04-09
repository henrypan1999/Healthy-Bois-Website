class Note:
    """
    A note object takes 4 arguments on init, a provider object, the actual note as
    a string, medication prescribed as a string, and a datetime object containing the
    datetime in which the note was created.
    """

    def __init__(self, provider, note, medication, date_time):
        self._provider = provider
        self._note = note
        self._medication = medication
        self._datetime = date_time.replace(microsecond=0)

    @property
    def provider(self):
        return self._provider

    @property
    def note(self):
        return self._note

    @property
    def medication(self):
        return self._medication

    @property
    def datetime(self):
        return self._datetime

    @property
    def fmt_datetime(self):
        return self._datetime.strftime("%c")

    @property
    def note_newline_delimited(self):
        return self.note.split("\n")

    @property
    def medication_newline_delimited(self):
        return self.medication.split("\n")
