import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l


from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_last_temperature, \
                    get_previous_temperature, \
                    get_next_temperature, \
                    get_this_temperature, \
                    is_first_temperature, \
                    is_last_temperature, \
                    append_temperature, \
                    is_temperature, \
                    update_temperature, \
                    delete_temperature, \
                    makeISODate, \
                    date_format

def temperature_record():
    """ Record the body temperature
    """
    userid = session["user_id"]
    conn = getDB()
    if request.method == "POST":
        if request.form.get("status") == "next" or \
            request.form.get("status") == "previous" or \
            request.form.get("status") == "delete":
            personal = get_personal_info(conn, userid)
            personal["birthday"] = date_format(personal["birthday"])
            dataset_id = request.form.get("recordId")
            try:
                dataset_id = int(dataset_id)
            except (ValueError, TypeError):
                dataset_id = 0
            if dataset_id == 0:
                mdata = get_last_temperature(conn, userid)
            elif request.form.get("status") == "next":
                mdata = get_next_temperature(conn, userid, dataset_id)
            elif request.form.get("status") == "previous":
                mdata = get_previous_temperature(conn, userid, dataset_id)
            elif request.form.get("status") == "delete":
                delete_temperature(conn, userid, dataset_id)
                mdata = get_previous_temperature(conn, userid, dataset_id)
                if len(mdata) == 0:
                    mdata = get_next_temperature(conn, userid, dataset_id)
                    if len(mdata) == 0:
                        conn.close()
                        return record_temperature_new()

            temperature = {}
            try:
                temperature["id"] = mdata["id"]
                temperature["userid"] = mdata["userid"]
                temperature["mdate"] = mdata["mdate"]
                temperature["body_temperature"] = mdata["body_temperature"]
                temperature["remarks"] = mdata["remarks"]
                temperature["mtime"] = mdata["mtime"]               
            except IndexError:
                conn.close()
                return record_temperature_new()
            active = {}
            if is_first_temperature(conn,userid,temperature["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_temperature(conn,userid,temperature["id"]):
                active["next"] = False
            else:
                active["next"] = True
            conn.close()

            return render_template("temperature_record.html",
                           personal = personal,
                           temperature = temperature,
                           dstatus = _l("Edit"),
                           active = active )

        elif request.form.get("status") == "new":
            return record_temperature_new()

        elif request.form.get("status") == "save":
            temperature = {}

            try:
                temperature["body_temperature"] = request.form.get("body_temperature") 
            except ValueError:
                return apology(_l("Invalid temperature value"), 400)

            temperature["remarks"] = request.form.get("remarks")

            temperature["mdate"] = request.form.get("mdate")
            temperature["mtime"] = request.form.get("mtime")

            isodate = makeISODate(temperature["mdate"], temperature["mtime"])
            if isodate == None:
                return apology(_l("Invalid Date/Time format"), 400)

            dataset_id = request.form.get("recordId")
            if not dataset_id:
                return record_temperature_new()
            try:
                dataset_id = int(dataset_id)
            except ValueError:
                dataset_id = 0
            temperature["id"] = dataset_id
            if dataset_id == 0:
                # new dataset
                append_temperature(conn, userid, temperature)
                mdata = get_last_temperature(conn, userid)

            elif dataset_id > 0:
                # update dataset
                if not is_temperature( conn, userid, dataset_id ):
                    return apology( _l("Dataset and user do not fit") , 400)

                update_temperature(conn, userid, temperature)
                mdata = get_this_temperature(conn, userid, dataset_id)

            personal = get_personal_info(conn, userid)
            personal["birthday"] = date_format(personal["birthday"])

            temperature = {}
            temperature["id"] = mdata["id"]
            temperature["userid"] = mdata["userid"]
            temperature["mdate"] = mdata["mdate"]
            temperature["body_temperature"] = mdata["body_temperature"]
            temperature["remarks"] = mdata["remarks"]
            temperature["mtime"] = mdata["mtime"]
            active = {}
            if is_first_temperature(conn,userid,temperature["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_temperature(conn,userid,temperature["id"]):
                active["next"] = False
            else:
                active["next"] = True

            conn.close()
            return render_template("temperature_record.html",
                           personal = personal,
                           temperature = temperature,
                           dstatus = _l("Edit"),
                           active = active )
    else:
    # User reached route via GET (as by clicking a link or via redirect)
    # or it falls through after POST
    # it is easier for the user to initially be posted on a new record
        return record_temperature_new()


def record_temperature_new():
    userid = session["user_id"]
    conn = getDB()
    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format(personal["birthday"])
    temperature = {}
    temperature["id"] = 0
    temperature["mdate"] = ""
    temperature["mtime"] = ""
    temperature["body_temperature"] = ""
    temperature["remarks"] = ""
    active = {}
    if is_first_temperature(conn,userid,temperature["id"]):
        active["previous"] = False
    else:
        active["previous"] = True
    if is_last_temperature(conn,userid,temperature["id"]):
        active["next"] = False
    else:
        active["next"] = True
    conn.close()
    return render_template("temperature_record.html",
                           personal = personal,
                           temperature = temperature,
                           dstatus = _l("New"),
                           active = active )
