import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l
from helpers import login_required
from personal import edit_personal_info
from bpchart import blood_pressure_chart
from record import record_measurement, record_measurement_new
from evaluate import evaluate_measurements, plotdata
from login import user_login, user_register, user_pwchange, admin_login
from weight_chart import weight_chart
from weight_evaluate import weight_evaluation
from weight_record import weight_record
from temperature_chart import temperature_chart
from temperature_evaluate import temperature_evaluation
from temperature_record import temperature_record


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["LANGUAGES"] = ['en', 'de']

# app.config["SESSION_FILE_DIR"] = "flask_session/"

def get_locale():
    """ return the desired language """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app, locale_selector = get_locale )
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """ only redirection for flask to start correctly """
    return redirect("/diastole")

@app.route("/diastole", methods=["GET", "POST"])
@login_required
def diastole():
    """Show a table of blood pressure records"""
    return blood_pressure_chart()

@app.route("/diastole/personal", methods=["GET", "POST"])
@login_required
def personal():
    """ Show the personal data of a person
        and let it be edited
    """
    return edit_personal_info()

@app.route("/weight", methods=["GET", "POST"])
@login_required
def weightchart():
    return weight_chart()

@app.route("/weight/record", methods=["GET", "POST"])
@login_required
def weightrecord():
    return weight_record()

@app.route("/weight/evaluation", methods=["GET", "POST"])
@login_required
def weightevaluation():
    return weight_evaluation()

@app.route("/diastole/temperature", methods=["GET", "POST"])
@login_required
def temperaturechart():
    return temperature_chart()

@app.route("/diastole/temperature/record", methods=["GET", "POST"])
@login_required
def temperaturerecord():
    return temperature_record()

@app.route("/diastole/temperature/evaluation", methods=["GET", "POST"])
@login_required
def temperatureevaluation():
    return temperature_evaluation()

@app.route("/diastole/record", methods=["GET", "POST"])
@login_required
def record():
    """record and edit blood pressure measurement"""
    return record_measurement()

@app.route("/diastole/newrecord", methods=["GET", "POST"])
@login_required
def newrecord():
    """display a new empty record"""
    return record_measurement_new()

@app.route("/diastole/evaluation", methods=["GET", "POST"])
@login_required
def evaluation():
    """evaluation of blood pressure measurements"""
    return evaluate_measurements()

@app.route("/diastole/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    return user_login()

@app.route("/diastole/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/diastole")

@app.route("/diastole/newpassword", methods=["GET", "POST"])
@login_required
def newpassword():
    return user_pwchange()

@app.route("/diastole/admin/login", methods=["GET", "POST"])
def adminlogin():
    """Log admin in"""

    # Forget any user_id
    session.clear()
    return admin_login()


@app.route("/diastole/admin/register", methods=["GET", "POST"])
@login_required
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    return user_register()

@app.route("/diastole/plotimage")
@login_required
def plotimage():
    return f"<img src='{plotdata()}'/>"

