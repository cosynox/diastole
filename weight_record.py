import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l


from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_last_measurement, \
                    get_measurement_five, \
                    get_previous_measurement, \
                    get_next_measurement, \
                    get_this_measurement, \
                    is_first_measurement, \
                    is_last_measurement, \
                    append_measurement, \
                    is_measurement, \
                    update_measurement, \
                    delete_measurement, \
                    makeISODate, \
                    getTime, \
                    getDate, date_format

def weight_record():
    """ Record the body weight
    """
    return apology("TODO",400)
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
                mdata = get_last_measurement(conn, userid)
            elif request.form.get("status") == "next":
                mdata = get_next_measurement(conn, userid, dataset_id)
            elif request.form.get("status") == "previous":
                mdata = get_previous_measurement(conn, userid, dataset_id)
            elif request.form.get("status") == "delete":
                delete_measurement(conn, userid, dataset_id)
                mdata = get_previous_measurement(conn, userid, dataset_id)
                if len(mdata) == 0:
                    mdata = get_next_measurement(conn, userid, dataset_id)
                    if len(mdata) == 0:
                        conn.close()
                        return record_measurement_new()

            measurement = {}
            measurement["id"] = mdata["id"]
            measurement["userid"] = mdata["userid"]
            measurement["mdate"] = mdata["mdate"]
            measurement["systole"] = mdata["systole"]
            measurement["diastole"] = mdata["diastole"]
            measurement["pulse"] = mdata["pulse"]
            measurement["remarks"] = mdata["remarks"]
            measurement["mtime"] = getTime( measurement["mdate"])
            measurement["mdate"] = getDate( measurement["mdate"])
            datasets = get_measurement_five(conn, userid)
            active = {}
            if is_first_measurement(conn,userid,measurement["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_measurement(conn,userid,measurement["id"]):
                active["next"] = False
            else:
                active["next"] = True
            conn.close()

            return render_template("record.html",
                           personal = personal,
                           measurement = measurement,
                           datasets = datasets,
                           dstatus = _l("Edit"),
                           active = active )

        elif request.form.get("status") == "new":
            return record_measurement_new()

        elif request.form.get("status") == "save":
            measurement = {}

            try:
                measurement["systole"] = int( request.form.get("systole") )
            except ValueError:
                return apology(_l("Invalid systolic value"), 400)

            try:
                measurement["diastole"] = int(request.form.get("diastole"))
            except ValueError:
                return apology(_l("Invalid diastolic value"), 400)

            try:
                measurement["pulse"] = int(request.form.get("pulse"))
            except ValueError:
                return apology(_("Invalid pulse value"), 400)

            measurement["remarks"] = request.form.get("remarks")

            measurement["mdate"] = request.form.get("mdate")
            measurement["mtime"] = request.form.get("mtime")

            isodate = makeISODate(measurement["mdate"], measurement["mtime"])
            if isodate == None:
                return apology(_l("Invalid Date/Time format"), 400)

            dataset_id = request.form.get("recordId")
            if not dataset_id:
                return record_measurement_new()
            try:
                dataset_id = int(dataset_id)
            except ValueError:
                dataset_id = 0
            measurement["id"] = dataset_id
            if dataset_id == 0:
                # new dataset
                append_measurement(conn, userid, measurement)
                mdata = get_last_measurement(conn, userid)

            elif dataset_id > 0:
                # update dataset
                if not is_measurement( conn, userid, dataset_id ):
                    return apology( _l("Dataset and user do not fit") , 400)

                update_measurement(conn, userid, measurement)
                mdata = get_this_measurement(conn, userid, dataset_id)

            personal = get_personal_info(conn, userid)
            personal["birthday"] = date_format(personal["birthday"])

            measurement = {}
            measurement["id"] = mdata["id"]
            measurement["userid"] = mdata["userid"]
            measurement["mdate"] = mdata["mdate"]
            measurement["systole"] = mdata["systole"]
            measurement["diastole"] = mdata["diastole"]
            measurement["pulse"] = mdata["pulse"]
            measurement["remarks"] = mdata["remarks"]
            measurement["mtime"] = getTime( measurement["mdate"])
            measurement["mdate"] = getDate( measurement["mdate"])
            datasets = get_measurement_five(conn, userid)
            active = {}
            if is_first_measurement(conn,userid,measurement["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_measurement(conn,userid,measurement["id"]):
                active["next"] = False
            else:
                active["next"] = True

            conn.close()
            return render_template("record.html",
                           personal = personal,
                           measurement = measurement,
                           datasets = datasets,
                           dstatus = _l("Edit"),
                           active = active )
    else:
    # User reached route via GET (as by clicking a link or via redirect)
    # or it falls through after POST
    # it is easier for the user to initially be posted on a new record
        return record_measurement_new()

    # this code is never reached, but I let it here
    # because it is if I decide to position on the last record
        personal = get_personal_info(conn, userid)
        personal["birthday"] = date_format(personal["birthday"])
        mdata = get_last_measurement(conn, userid)
        if len(mdata) == 0:
            return record_measurement_new()

        measurement = {}
        measurement["id"] = mdata["id"]
        measurement["userid"] = mdata["userid"]
        measurement["mdate"] = mdata["mdate"]
        measurement["systole"] = mdata["systole"]
        measurement["diastole"] = mdata["diastole"]
        measurement["pulse"] = mdata["pulse"]
        measurement["remarks"] = mdata["remarks"]
        measurement["mtime"] = getTime( measurement["mdate"])
        measurement["mdate"] = getDate( measurement["mdate"])

        datasets = get_measurement_five(conn, userid)
        conn.close()
        return render_template( "record.html",

                           personal = personal,
                           measurement = measurement,
                           datasets = datasets,
                           dstatus = _l("Edit") )

def record_measurement_new():
    userid = session["user_id"]
    conn = getDB()
    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format(personal["birthday"])
    datasets = get_measurement_five(conn, userid)
    measurement = {}
    measurement["id"] = 0
    measurement["mdate"] = ""
    measurement["mtime"] = ""
    measurement["systole"] = ""
    measurement["diastole"] = ""
    measurement["pulse"] = ""
    measurement["remarks"] = ""
    active = {}
    if is_first_measurement(conn,userid,measurement["id"]):
        active["previous"] = False
    else:
        active["previous"] = True
    if is_last_measurement(conn,userid,measurement["id"]):
        active["next"] = False
    else:
        active["next"] = True
    conn.close()
    return render_template("record.html",
                           personal = personal,
                           measurement = measurement,
                           datasets = datasets,
                           dstatus = _l("New"),
                           active = active )
