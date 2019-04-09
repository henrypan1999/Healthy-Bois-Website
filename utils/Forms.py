from wtforms import (
    Form,
    PasswordField,
    SelectField,
    StringField,
    validators,
    IntegerField,
    DateField,
    TimeField,
    ValidationError,
)


class FormExtended(Form):
    @property
    def lerrors(self):
        """
        Returns a list of error messages from failed validators
        """
        return [x[0] for x in self.errors.values()]


class LoginForm(FormExtended):
    email = StringField(
        ("email"),
        [
            validators.DataRequired(message="Please enter your email."),
            validators.Email(message="Please enter a valid email address."),
        ],
    )
    password = PasswordField(
        ("password"), [validators.DataRequired(message="Please enter your password.")]
    )


class SearchForm(FormExtended):
    search_type = SelectField(
        "search_type",
        choices=[
            ("name", "name"),
            ("suburb", "suburb"),
            ("service", "service"),
            ("provider", "provider"),
        ],
        validators=[validators.DataRequired(message="Don't break my app.")],
    )
    query = StringField(("query"))


class RateForm(FormExtended):
    rating = IntegerField(
        "rating",
        validators=[
            validators.DataRequired(
                message="Empty rating received, please enter a rating."
            ),
            validators.NumberRange(
                min=1,
                max=5,
                message="Rating received was out of bounds, please try again.",
            ),
        ],
    )


class BookingForm(FormExtended):

    time = TimeField(
        "time",
        format="%H:%M",
        validators=[validators.DataRequired(message="Time required.")],
    )
    note = StringField("note")

    def validate_time(form, field):
        """
        Simple validator to ensure that booking times are at 30minute intervals.
        """

        if field.data.minute == 30 or field.data.minute == 0:
            pass
        else:
            raise ValidationError(
                "Bookings must be made on the hour or every 30 minutes."
            )


class NoteForm(FormExtended):
    note = StringField(
        "note", validators=[validators.DataRequired(message="Note required.")]
    )
    medication = StringField("medication")
