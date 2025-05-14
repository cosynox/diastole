import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l

from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_weights, \
                    makeISODate, \
                    getTime, \
                    getDate, date_format, time_format

from pdftable import gen_pdfchart

def weight_chart():
    """ Generate a Body weight chart
    """
    userid = session["user_id"]
    conn = getDB()
    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format( personal["birthday"])
    filter = {}
    filter["datefrom"] = ""
    filter["dateuntil"] = ""
    status = "" 
    if request.method == "POST":
        filter = {}
        filter["datefrom"] = ""
        filter["dateuntil"] = ""
        tmp = request.form.get("datefrom")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.form.get("dateuntil")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp

        weights = get_weights(conn, userid, filter)
        status = request.form.get("status")

    else:
        status = request.args.get("status")
        weights = get_weights(conn, userid, None)

    if len(weights) > 0:
        minweight = weights[0]["body_weight"]
        maxweight = weights[0]["body_weight"]
    else:
        minweight = 0
        maxweight = 0
    sumweight = 0
    n = 0
    for data in weights:
        data["mdate"] = date_format(data["mdate"])
        data["mtime"] = time_format(data["mtime"])
        if minweight > data["body_weight"]:
            minweight = data["body_weight"]
        if maxweight < data["body_weight"]:
            maxweight = data["body_weight"]    
        sumweight += data["body_weight"]
        n += 1
    if n > 0:
        avgweight = int(round(sumweight / n ,0))
    else:
        avgweight = 0
    # do something
    conn.close()
    if status == "pdf":
        return apology("TODO", 400)
#        return gen_pdfchart(personal, 
#                           measurements,
#                           minsystole,
#                           maxsystole,
#                           mindiastole,
#                           maxdiastole,
#                           minpulse,
#                            maxpulse,
#                           avgsystole,
#                           avgdiastole,
#                           avgpulse)
    else:   
        return render_template( "weight_chart.html",                             
                           personal = personal,
                           weightchart = weights,
                           filter = filter,
                           minweight = minweight, 
                           maxweight = maxweight,
                           avgweight = avgweight)
