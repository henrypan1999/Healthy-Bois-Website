class HealthCentre:
    __id = -1

    def __init__(self, centretype, abn, name, phone, suburb):
        self._id = self._generate_id()
        self._centretype = centretype
        self._abn = abn
        self._name = name
        self._phone = phone
        self._suburb = suburb
        self._blurb = "This is a health centre. Please add description."
        self._providers = []
        self._ratings = []

    @property
    def providers(self):
        """
        Providers stores a list of UIDs that uniquely identify Healthcare Providers
        that work at the centre.
        """
        return self._providers

    def add_provider(self, uid):
        self._providers.append(uid)

    @property
    def ID(self):
        return self._id

    @property
    def centretype(self):
        return self._centretype

    @property
    def abn(self):
        return self._abn

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @property
    def suburb(self):
        return self._suburb

    @property
    def blurb(self):
        return self._blurb

    @blurb.setter
    def blurb(self, blurb):
        self._blurb = blurb

    @property
    def ratings(self):
        return self._ratings

    def add_rating(self, rating):
        self.ratings.append(rating)

    def _generate_id(self):
        HealthCentre.__id += 1
        return HealthCentre.__id

    @property
    def average_rating(self):
        rating_len = len(self.ratings)
        if rating_len < 1:
            return 0
        total = 0
        for rating in self.ratings:
            total += rating.value
        return round(total / rating_len, 2)

    def __str__(self):
        return f"HealthCare Centre: {self.name} located at {self.suburb}"
