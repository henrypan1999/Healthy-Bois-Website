from flask import Flask
from flask_login import LoginManager
from src.AuthenticationManager import AuthenticationManager
from src.HealthCentreManager import HealthCentreManager
from src.UserManager import UserManager
from src.client import bootstrap_system
from src.User import Patient
from src.BookingSystem import BookingSystem
from src.RatingManager import RatingManager

from src.ReferralSystem import ReferralSystem

app = Flask(__name__)
app.secret_key = "super extra secret"


# Authentication manager and System setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
booking_system = BookingSystem()

referral_system = ReferralSystem()
auth_manager = AuthenticationManager(login_manager)
hc_manager = HealthCentreManager()
user_manager = UserManager()
rating_manager = RatingManager(app.root_path)
system = bootstrap_system(auth_manager, app.root_path, hc_manager, user_manager, booking_system, rating_manager, referral_system)


@login_manager.user_loader
def load_user(user_id):
    return system.get_user_by_id(user_id)


import routes
