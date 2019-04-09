class Referral:
    def __init__(self,GP, specialist, patient, note):
        self._GP = GP
        self._specialist = specialist
        self._patient = patient
        self._note = note
    
    @property
    def GP(self):
        return self._GP

    @property
    def specialist(self):
        return self._specialist

    @property
    def patient (self):
        return self._patient

    @property
    def note(self):
        return self._note