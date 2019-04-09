import csv
import os
from datetime import datetime
from utils.flaskhelpers import flash
from flask_login import login_user, logout_user

from .AuthenticationManager import AuthenticationManager
from .BookingSystem import BookingSystem
from .HealthCentre import HealthCentre
from .User import Patient, Provider
from .CSVLoader import CSVLoader
from .Note import Note
from .Search import Search
from .ReferralSystem import ReferralSystem

class HealthCareSystem:
    def __init__(self, auth_manager, root_path, hc_manager, user_manager, booking_system, rating_manager, referral_system):
        self._auth_manager = auth_manager
        self._base_path = root_path
        loader = CSVLoader(root_path)
        dbs = loader.get_dict()
        self._user_manager = user_manager
        user_manager.add_multiple_patients(dbs["patients"])
        user_manager.add_multiple_providers(dbs["providers"])
        self._hc_manager = hc_manager
        hc_manager.add_multiple_centres(dbs["centres"])
        self._booking_system = booking_system
        self._affiliation_linker(dbs["affiliations"])
        self._booking_system = booking_system 
        booking_system.make_multiple_bookings(dbs["booking"], hc_manager, user_manager)
        self._rating_manager = rating_manager
        rating_manager.add_multiple_ratings(user_manager, hc_manager, dbs["ratings"])
        user_manager.get_notes(dbs["HP_notes"])
        self._referral_system = referral_system
        self._search = Search(hc_manager,user_manager)

    def _affiliation_linker(self, affiliations):
        """Linker accepts 1 arg with a list of (health_centre_name, provider_email) tuples"""
        for centre_name, provider_email in affiliations:
            centre = self.hc_manager.get_HC_by_name(centre_name)
            provider = self.user_manager.get_HP_by_username(provider_email)
            assert centre_name and provider_email
            provider.add_workplace(centre.name)
            centre.add_provider(provider.get_id())

    
    @property
    def hc_manager(self):
        return self._hc_manager
    
    @property
    def user_manager(self):
        return self._user_manager
    
    @property
    def booking_system(self):
        return self._booking_system
        
    @property
    def rating_manager(self):
        return self._rating_manager

    @property
    def search(self):
        return self._search
        
    @property
    def base_path(self):
        return self._base_path
    
    def add_patient_note(self, note, patient):
        bookings = self.booking_system.get_user_bookings(note.provider)
        for b in bookings:
            #lol = str(datetime.now())
            #flash(lol)  
            x = b.time.replace(minute = (b.time.minute+30)%60)
            #flash('1')
            if x.minute == 00:
                #flash('2')
                x = x.replace(hour=(x.hour+1)%24)
            #lol = str(x)
            #flash(lol)
            #lol = str(b.time)
            #flash(lol)
            #lol = str(note.datetime)
            #flash(lol)
            if note.datetime <= x and note.datetime >= b.time:           #if current time inside appointment time
                loader = CSVLoader(self.base_path)
                loader.write_HP_notes(note, patient)
                patient.add_note(note)
                flash('Note Added Successfully')
                return
        flash("Note Failed - Not within an appointment.")
        
    """
    Query Processing Services
    """
    # Search 1
    # Input: string - name of healthcentre
    # Output: List of all healthcentres(object)
    #def search_HC_name(self, name=""):
    #    return Search.search_HC_name(self.hc_manager, name)

    # Search 2
    # Input: string - suburb
    # Output: List of all healthcentres(object)
    #def search_HC_suburb(self, suburb=""):
    #    return Search.search_HC_suburb(self.hc_manager, suburb)

    # Search 3
    # Input: string - name of service/profession
    # Output: List of all providers(object)
    #def search_HP_service(self, service=""):
    #    return Search.search_HP_service(self.user_manager, service)

    # Search 4
    # Input: string - name of provider
    # Output: List of all providers(object)
    #def search_HP_name(self, name=""):
    #    return Search.search_HP_name(self.user_manager, name)

    """
    Following Queries
    """

    # Profile Page List 1
    # At this step, person has clicked on healthcentre, and the profile page needs to list all its providers
    # Input: healthcentre(object)
    # Output: List of all providers(object)
    def list_hc_providers(self, hc):
        return [self.get_user_by_id(x) for x in hc.providers]

    # Profile Page List 2
    # At this step, person has clicked on provider, and the profile page needs to list all its healthcentres
    # After this function, look at booking system
    # Input: provider(object)
    # Output: List of all healthcentres(object)
    def list_provider_hcs(self, provider):
        return [self.hc_manager.get_HC_by_name(x) for x in provider.workplaces]

    def HP_list(self, hp):
        new_search_list = []
        for centre in hp.workplaces:
            new_search_list.append(self.hc_manager.get_HC_by_name(centre))
        return new_search_list

    

    """
    login
    """

    def login(self, username, password):
        for patient in self.user_manager.patients:
            if username == patient._username and password == patient._password:
                login_user(patient)
                return True

        for provider in self.user_manager.providers:
            if username == provider._username and password == provider._password:
                login_user(provider)
                return True

        return False

    def logout(self):
        logout_user()

    def get_user_by_id(self, user_id):
        for u in self.user_manager.patients:
            if u.get_id() == user_id:
                return u
        for u in self.user_manager.providers:
            if u.get_id() == user_id:
                return u
        return None


if __name__ == "__main__":
    # close to search words
    # already saved inputs check

    login_manager = LoginManager()
    auth_manager = AuthenticationManager(login_manager)
    HCsystem = HealthCareSystem(auth_manager)

    chris = Patient("email", "pass", "chris")
    dan = Patient("email", "pass", "dan")
    jennifer = Provider("email", "pass", "Pathologist", "jennifer")
    andy = Provider("email", "pass", "Psychologist", "andy")
    randwick = HealthCentre(
        "2111", "Randwick da Best Hosotail", "8888 8888", "Randwick"
    )
    carlingford = HealthCentre(
        "2111", "Carlo da Best Hospitail", "8888 8888", "Carlingford"
    )

    HCsystem.add_patient(chris)
    HCsystem.add_patient(dan)
    HCsystem.add_provider(jennifer)
    HCsystem.add_provider(andy)
    HCsystem.add_centre(randwick)
    HCsystem.add_centre(carlingford)

    patients = HCsystem.patients
    print(patients)
    providers = HCsystem.providers
    print(providers)
    centres = HCsystem.centres
    print(centres)

    for c in centres:
        if c.ID == 0:
            print(c)

    print()
    HCNAMES = HCsystem.search_HC_name("Carlo da Best Hospitail")
    for c in HCNAMES:
        print(c)

    print()
    HCSUB = HCsystem.search_HC_suburb("Randwick")
    for c in HCSUB:
        print(c)

    print()
    HPSERV = HCsystem.search_HP_service("Pathologist")
    for c in HPSERV:
        print(c)

    print()
    HPNAMES = HCsystem.search_HP_name("jennifer")
    for c in HPNAMES:
        print(c)

    print("\nAffiliations")
    HCLIST = HCsystem.HC_list(randwick)
    for c in HCLIST:
        print(c)

    print("\nAffiliations2")
    HPLIST = HCsystem.HP_list(jennifer)
    for c in HPLIST:
        print(c)

    bsystem = BookingSystem()
    # bsystem.print_bookings()

    print("\nGET Appointments")
    AppList = bsystem.get_user_bookings(chris)
    HCsystem.print_list(AppList)
    AppList = bsystem.get_user_bookings(jennifer)
    HCsystem.print_list(AppList)
