import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l

from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_measurements, \
                    makeISODate, \
                    getTime, \
                    getDate, date_format, time_format

from pdftable import gen_pdfchart
from csvtable import export_csv_blood_pressure

def blood_pressure_chart():
    """ Generate a blood pressure chart
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

        measurements = get_measurements(conn, userid, filter)
        status = request.form.get("status")

    else:
        status = request.args.get("status")
        measurements = get_measurements(conn, userid, None)

    if len(measurements) > 0:
        minsystole = measurements[0]["systole"]
        maxsystole = measurements[0]["systole"]
        mindiastole = measurements[0]["diastole"]
        maxdiastole = measurements[0]["diastole"]
        minpulse = measurements[0]["pulse"]
        maxpulse = measurements[0]["pulse"]
    else:
        minsystole = 0
        maxsystole = 0
        mindiastole = 0
        maxdiastole = 0
        minpulse = 0
        maxpulse = 0
    sumsystole = 0
    sumdiastole = 0
    sumpulse = 0
    n = 0
    for data in measurements:
        data["mdate"] = date_format(data["mdate"])
        data["mtime"] = time_format(data["mtime"])
        if minsystole > data["systole"]:
            minsystole = data["systole"]
        if maxsystole < data["systole"]:
            maxsystole = data["systole"]    
        if mindiastole > data["diastole"]:
            mindiastole = data["diastole"]
        if maxdiastole < data["diastole"]:
            maxdiastole = data["diastole"]    
        if minpulse > data["pulse"]:
            minpulse = data["pulse"]
        if maxpulse < data["pulse"]:
            maxpulse = data["pulse"]    
        sumsystole += data["systole"]
        sumdiastole += data["diastole"]
        sumpulse += data["pulse"]
        n += 1
    if n > 0:
        avgsystole = int(round(sumsystole / n ,0))
        avgdiastole = int(round( sumdiastole / n, 0))
        avgpulse = int(round(sumpulse / n, 0))
    else:
        avgsystole = 0
        avgdiastole = 0
        avgpulse = 0
    # do something
    conn.close()
    if status == "pdf":
        return gen_pdfchart(personal, 
                            measurements,
                            minsystole,
                            maxsystole,
                            mindiastole,
                            maxdiastole,
                            minpulse,
                            maxpulse,
                            avgsystole,
                            avgdiastole,
                            avgpulse)
    elif status == "csv":
        return export_csv_blood_pressure(measurements)
    else:   
        return render_template( "bpchart.html",                             
                           personal = personal,
                           bpchart = measurements,
                           filter = filter,
                           minsystole = minsystole, 
                           maxsystole = maxsystole,
                           mindiastole = mindiastole,
                           maxdiastole = maxdiastole,
                           minpulse = minpulse,
                           maxpulse = maxpulse,
                           avgsystole = avgsystole,
                           avgdiastole = avgdiastole,
                           avgpulse = avgpulse )
