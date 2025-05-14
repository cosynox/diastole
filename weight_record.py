import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l


from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_last_weight, \
                    get_previous_weight, \
                    get_next_weight, \
                    get_this_weight, \
                    is_first_weight, \
                    is_last_weight, \
                    append_weight, \
                    is_weight, \
                    update_weight, \
                    delete_weight, \
                    makeISODate, \
                    getTime, \
                    getDate, date_format

def weight_record():
    """ Record the body weight
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
                mdata = get_last_weight(conn, userid)
            elif request.form.get("status") == "next":
                mdata = get_next_weight(conn, userid, dataset_id)
            elif request.form.get("status") == "previous":
                mdata = get_previous_weight(conn, userid, dataset_id)
            elif request.form.get("status") == "delete":
                delete_weight(conn, userid, dataset_id)
                mdata = get_previous_weight(conn, userid, dataset_id)
                if len(mdata) == 0:
                    mdata = get_next_weight(conn, userid, dataset_id)
                    if len(mdata) == 0:
                        conn.close()
                        return record_weight_new()

            weight = {}
            try:
                weight["id"] = mdata["id"]
                weight["userid"] = mdata["userid"]
                weight["mdate"] = mdata["mdate"]
                weight["body_weight"] = mdata["body_weight"]
                weight["remarks"] = mdata["remarks"]
                weight["mtime"] = mdata["mtime"]               
            except IndexError:
                conn.close()
                return record_weight_new()
            active = {}
            if is_first_weight(conn,userid,weight["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_weight(conn,userid,weight["id"]):
                active["next"] = False
            else:
                active["next"] = True
            conn.close()

            return render_template("weight_record.html",
                           personal = personal,
                           weight = weight,
                           dstatus = _l("Edit"),
                           active = active )

        elif request.form.get("status") == "new":
            return record_weight_new()

        elif request.form.get("status") == "save":
            weight = {}

            try:
                weight["body_weight"] = request.form.get("body_weight") 
            except ValueError:
                return apology(_l("Invalid weight value"), 400)

            weight["remarks"] = request.form.get("remarks")

            weight["mdate"] = request.form.get("mdate")
            weight["mtime"] = request.form.get("mtime")

            isodate = makeISODate(weight["mdate"], weight["mtime"])
            if isodate == None:
                return apology(_l("Invalid Date/Time format"), 400)

            dataset_id = request.form.get("recordId")
            if not dataset_id:
                return record_weight_new()
            try:
                dataset_id = int(dataset_id)
            except ValueError:
                dataset_id = 0
            weight["id"] = dataset_id
            if dataset_id == 0:
                # new dataset
                append_weight(conn, userid, weight)
                mdata = get_last_weight(conn, userid)

            elif dataset_id > 0:
                # update dataset
                if not is_weight( conn, userid, dataset_id ):
                    return apology( _l("Dataset and user do not fit") , 400)

                update_weight(conn, userid, weight)
                mdata = get_this_weight(conn, userid, dataset_id)

            personal = get_personal_info(conn, userid)
            personal["birthday"] = date_format(personal["birthday"])

            weight = {}
            weight["id"] = mdata["id"]
            weight["userid"] = mdata["userid"]
            weight["mdate"] = mdata["mdate"]
            weight["body_weight"] = mdata["body_weight"]
            weight["remarks"] = mdata["remarks"]
            weight["mtime"] = mdata["mtime"]
            active = {}
            if is_first_weight(conn,userid,weight["id"]):
                active["previous"] = False
            else:
                active["previous"] = True
            if is_last_weight(conn,userid,weight["id"]):
                active["next"] = False
            else:
                active["next"] = True

            conn.close()
            return render_template("weight_record.html",
                           personal = personal,
                           weight = weight,
                           dstatus = _l("Edit"),
                           active = active )
    else:
    # User reached route via GET (as by clicking a link or via redirect)
    # or it falls through after POST
    # it is easier for the user to initially be posted on a new record
        return record_weight_new()


def record_weight_new():
    userid = session["user_id"]
    conn = getDB()
    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format(personal["birthday"])
    weight = {}
    weight["id"] = 0
    weight["mdate"] = ""
    weight["mtime"] = ""
    weight["body_weight"] = ""
    weight["remarks"] = ""
    active = {}
    if is_first_weight(conn,userid,weight["id"]):
        active["previous"] = False
    else:
        active["previous"] = True
    if is_last_weight(conn,userid,weight["id"]):
        active["next"] = False
    else:
        active["next"] = True
    conn.close()
    return render_template("weight_record.html",
                           personal = personal,
                           weight = weight,
                           dstatus = _l("New"),
                           active = active )
