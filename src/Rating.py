class Rating:


    def __init__(self, patient, value):
        self._patient = patient
        self._value = value
        
    @property
    def patient(self):
        return self._patient
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

