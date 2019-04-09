
from flask_login import current_user
from flask import redirect, url_for
from functools import wraps


"""
    Wraps around flask-login's LoginManager
    to provide additional functionalities
"""


class AuthenticationManager:
    def __init__(self, login_manager):
        self._login_manager = login_manager
        self._default_page = "home"

    def patient_required(self, fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            if not current_user or not current_user.is_authenticated:
                return self._to_default_page()

            if not current_user.is_patient:
                return self._to_default_page()
            return fn(*args, **kwargs)

        return decorated_fn

    def provider_required(self, fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            if not current_user or not current_user.is_authenticated:
                return self._to_default_page()
            if not current_user.is_provider:
                return self._to_default_page()

            return fn(*args, **kwargs)

        return decorated_fn

    # Redirect user to default page
    def _to_default_page(self):
        return redirect(url_for(self._default_page))
