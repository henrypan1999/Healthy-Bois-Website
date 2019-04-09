from flask_login import UserMixin
from abc import ABC, abstractclassmethod


class User(UserMixin, ABC):
    __id = -1

    def __init__(self, username, password, name):
        self._id = self._generate_id()
        self._username = username
        self._password = password
        self._name = name
        self._usertype = None

    @abstractclassmethod
    def is_provider(self):
        pass

    @abstractclassmethod
    def is_patient(self):
        pass

    @property
    def ID(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property  # flask for login
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        User.__id += 1
        return User.__id

    def validate_password(self, password):
        return (
            self._password == password
        )  # dont need a getter for password - flask will validate

    @property
    def usertype(self):
        return self._usertype

    @property
    def name(self):
        return self._name


    def __str__(self):
        return f"{self.usertype}: {self.username}"


class Patient(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name)
        self._usertype = "patient"  # patient is usertype
        self._notes = []                                                                    #notes is a list of the OBJECTS(NOTE)

    @property
    def notes(self):
        return self._notes

    def add_note(self, note):
        self._notes.append(note)

    def __str__(self):
        return f"Patient: <{self._id} {self.username} {self._password} {self.usertype} {self.name}>"

    @property
    def is_provider(self):
        return False

    @property
    def is_patient(self):
        return True


class Provider(User):
    def __init__(self, username, password, profession, name):
        super().__init__(username, password, name)
        self._usertype = "provider"
        self._profession = profession
        self._workplaces = []
        self._blurb = 'Please write a description about provider.'
        self._ratings = []

    @property
    def workplaces(self):
        """
        Workplaces stores the name of the Healthcare centre in a list of strings. We're
        assuming that no two centres have the same name so we can uniquely identify
        provider's workplaces.
        """
        return self._workplaces

    def add_workplace(self, centre_name):
        self._workplaces.append(centre_name)

    @property
    def profession(self):
        return self._profession

    @property
    def blurb(self):
        return self._blurb

    @blurb.setter
    def blurb(self, blurb):
        self._blurb = blurb

    @property
    def is_provider(self):
        return True

    @property
    def is_patient(self):
        return False

    @property
    def ratings(self):
        return self._ratings

    @property
    def average_rating(self):
        rating_len = len(self.ratings)
        if rating_len < 1:
            return 0
        total = 0
        for rating in self.ratings:
            total += rating.value
        return round(total / rating_len, 2)

    def add_rating(self, rating):
        self.ratings.append(rating)

    def __str__(self):
        return f"Provider: <{self._id} {self.username} {self._password} {self.usertype} {self.name}>"
