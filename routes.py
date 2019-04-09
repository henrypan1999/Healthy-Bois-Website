from datetime import date, datetime
from os.path import join as path_join

from flask import (
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required

from app import app, auth_manager, booking_system, system
from src.Note import Note
from src.CSVLoader import CSVLoader
from src.Booking import Booking
from src.Rating import Rating
from utils.flaskhelpers import flash
from utils.Forms import BookingForm, LoginForm, NoteForm, RateForm, SearchForm
from copy import copy


@app.route("/hams", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        form = LoginForm(request.form)

        if form.validate():
            if system.login(form.email.data, form.password.data):
                redir = request.args.get("next")
                flash("Successfully logged in.")
                return redirect(redir or url_for("home"))

            error_messages = ["Login failed, please check your email and password."]
            return render_template(
                "login.html", email=form.email.data, error_messages=error_messages
            )

        else:
            return render_template(
                "login.html", email=form.email.data, error_messages=form.lerrors
            )

    return render_template("login.html")


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route("/appointments")
@login_required
def appointments():
    upcoming_apts = system.booking_system.get_user_bookings(current_user, "upcoming")
    return render_template("appointments.html", appointments=upcoming_apts)


@app.route("/history")
@login_required
def history():
    prev_apts = system.booking_system.get_user_bookings(current_user, "past")
    return render_template("appointments.html", appointments=prev_apts, history=True)


@app.route("/logout")
@login_required
def logout():
    system.logout()
    flash("Successfully logged out.")
    return redirect(url_for("login"))


@app.route("/centre_profile/<centrename>", methods=["GET", "POST"])
@auth_manager.patient_required
def centre_profile(centrename):
    centre = system.hc_manager.get_HC_by_name(centrename)
    providers = system.list_hc_providers(centre)
    if centre:
        if request.method == "POST":
            # TODO: rate centres
            form = RateForm(request.form)
            if form.validate():
                rate = Rating(copy(current_user), form.rating.data)
                loader = CSVLoader(app.root_path)
                rate_type = system.rating_manager.add_rating(
                    rate, centre, system, current_user
                )
                if rate_type != "failure":
                    loader.remove_rating(centre, current_user)
                    loader.add_rating(rate, rate_type, centre)
                
        return render_template(
            "centre_profile.html",
            centre=centre,
            providers=providers,
            centrename=centrename,
        )
    abort(404)


@app.route("/provider_profile/<uid>", methods=["GET", "POST"])
@auth_manager.patient_required
def provider_profile(uid):
    provider = system.get_user_by_id(uid)
    if provider:
        if request.method == "POST":
            # TODO: rate providers
            form = RateForm(request.form)
            if form.validate():
                rate = Rating(copy(current_user), form.rating.data)
                loader = CSVLoader(app.root_path)
                rate_type = system.rating_manager.add_rating(
                    rate, provider, system, current_user
                )
                if rate_type != "failure":
                    loader.remove_rating(provider, current_user)
                    loader.add_rating(rate, rate_type, provider)
        return render_template(
            "provider_profile.html",
            provider=provider,
            workplaces=system.list_provider_hcs(provider),
            uid=uid,
        )
    abort(404)


@app.route("/book_apt/<provider>/<centre>", methods=["GET", "POST"])
def book_appointment(provider, centre):
    provider = system.get_user_by_id(provider)
    centre = system.hc_manager.get_HC_by_name(centre)
    # 404 if provider or centre does not exist in our system.
    if not provider or not centre:
        abort(404)

    booking_date = request.args.get("date")
    if booking_date:
        # Validate date
        try:
            year, month, day = booking_date.split("-")
            booking_date = date(int(year), int(month), int(day))
            if booking_date < datetime.now().date():
                raise Exception("date provided is before current date.")
        except (ValueError, Exception) as e:
            flash("Invalid date: " + str(e))
            return render_template(
                "book_appointment.html", provider=provider, centre=centre
            )
        times = system.booking_system.booking_availabilities(provider, booking_date)
        # Handle submitted forms
        if request.method == "POST":
            form = BookingForm(request.form)
            if form.validate():
                booking_datetime = datetime.combine(booking_date, form.time.data)
                if booking_datetime > datetime.now():
                    loader = CSVLoader(app.root_path)
                    new_booking = Booking(
                        centre, 
                        provider, 
                        booking_datetime, 
                        copy(current_user), 
                        form.note.data
                    )
                    booking_system.make_booking(new_booking)
                    loader.write_booking(new_booking)
                    flash("Booking Successful!")
                    return redirect(url_for("appointments"))
                else:
                    flash("Appointments cannot be made in the past.")
            else:
                flash(form.errors)
            return render_template(
                "book_appointment.html",
                times=times,
                provider=provider,
                centre=centre,
                date=request.args.get("date"),
                note=form.note.data,
            )
        # If a valid booking_date was provided but it's a GET request
        else:
            return render_template(
                "book_appointment.html",
                times=times,
                provider=provider,
                centre=centre,
                date=request.args.get("date"),
            )
    # No valid date provided
    if booking_date == "":
        flash("Please enter a date.")
    return render_template("book_appointment.html", provider=provider, centre=centre)


@app.route("/appointment/<bid>", methods=["GET", "POST"])
@auth_manager.provider_required
def appointment_info(bid):
    # Make sure that it can be converted to an int
    try:
        bid = int(bid)
    except ValueError as e:
        abort(404)
    booking = system.booking_system.get_booking_by_id(bid, current_user)
    if booking:
        patient = booking.user
        if request.method == "POST":
            form = NoteForm(request.form)
            if form.validate():
                # Most of this stuff should really be in HealthCareSystem
                date = datetime.now()
                new_note = Note(
                    copy(current_user), form.note.data, form.medication.data, date
                )
                system.add_patient_note(new_note, patient)
            else:
                flash(form.lerrors)
            return render_template(
                "appointment.html",
                booking=booking,
                patient=patient,
                note=form.note.data,
                medication=form.medication.data,
            )

        # If GET request
        # Rather hacky way to create "newlines" in HTML, but probably the least hacky.
        return render_template("appointment.html", booking=booking, patient=patient)
    # If booking not found
    abort(404)


@app.route("/search", methods=["GET", "POST"])
@auth_manager.patient_required
def search():
    if request.method == "POST":
        form = SearchForm(request.form)
        if form.validate():
            # TODO: change template's ABN detail field to rating when implemented
            query = form.query.data
            search_type = form.search_type.data
            if search_type == "name":
                results = system.search.search_HC_name(query)
                results_kind = "HC"
                prev_type = "name"
            elif search_type == "suburb":
                results = system.search.search_HC_suburb(query)
                results_kind = "HC"
                prev_type = "suburb"
            elif search_type == "service":
                results = system.search.search_HP_service(query)
                results_kind = "HP"
                prev_type = "service"
            else:
                # by provider's name
                results = system.search.search_HP_name(query)
                results_kind = "HP"
                prev_type = "provider"
            return render_template(
                "search.html",
                results=results,
                results_kind=results_kind,
                prev_type=prev_type,
                query=query,
            )
        else:
            flash("Invalid search request.")
        return render_template("search.html", query=query)
    return render_template("search.html")


"""
Error Handlers
"""


@app.errorhandler(404)
def error_404(e):
    return send_from_directory(path_join(app.root_path, "static"), "404.html")


"""
Static Content
"""


@app.route("/css/materialize.css", methods=["GET"])
def serve_css():
    if not app.debug:
        return send_from_directory(
            path_join(app.root_path, "static"), "materialize.min.css"
        )
    else:
        return send_from_directory(
            path_join(app.root_path, "static"), "materialize.css"
        )


@app.route("/css/custom.css", methods=["GET"])
def serve_custom_css():
    return send_from_directory(path_join(app.root_path, "static"), "custom.css")


@app.route("/js/materialize.js", methods=["GET"])
def serve_js():
    return send_from_directory(path_join(app.root_path, "static"), "materialize.js")
