import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l
from helpers import apology
from dbaccess import getDB, get_personal_info, set_personal_info

def edit_personal_info():
    """ Edit the personal data of a person
    """
    userid = session["user_id"]
    conn = getDB()
    if request.method == "POST":
        personal = {}
        personal["id"] = userid
        personal["firstname"] = request.form.get("firstname")
        personal["lastname"] = request.form.get("lastname")
        personal["birthday"] = request.form.get("birthday")
        set_personal_info(conn, personal)
    # User reached route via GET (as by clicking a link or via redirect)
    # or it falls through after POST
    personal = get_personal_info(conn, userid)
    conn.close()
    return render_template("personal.html", personal=personal)
