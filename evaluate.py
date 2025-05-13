import datetime
import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, make_response
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l
from io import BytesIO
import base64 
from matplotlib.figure import Figure
from matplotlib.dates import datestr2num
import matplotlib.dates as mdates
from helpers import apology
from dbaccess import getDB, \
                    get_measurements, \
                    get_personal_info, date_format

def evaluate_measurements():
    """ Edit the personal data of a person
    """
    conn = getDB()
    userid = session["user_id"]
    conn = getDB()
    filter = {}
    filter["datefrom"] = ""
    filter["dateuntil"] = ""

    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format(personal["birthday"])
    if request.method == "GET":
        tmp = request.args.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.args.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
    elif request.method == "POST":
        tmp = request.form.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.form.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
    
    measurements = get_measurements(conn, userid, filter)
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
    
    category = _l("undefined")
    if avgsystole < 100 and avgdiastole < 60:
        category = _l("low")
    elif avgsystole < 120 and avgdiastole < 80:
        category = _l("optimal")
    elif avgsystole < 130 and avgdiastole < 85:
        category = _l("normal")
    elif avgsystole <= 139 and avgdiastole <= 89:
        category = _l("high-normal")
    elif avgsystole <= 159 and avgdiastole <= 99:
        category = _l("grade 1 (mild hypertonia)")
    elif avgsystole <= 179 and avgdiastole <= 109:
        category = _l("grade 2 (moderate hypertonia)")
    elif avgsystole >= 180 or avgdiastole >= 110:
        category = _l("grade 3 (severe hypertonia)")

    conn.close()

    myimage = plotdata()

   
    return render_template( "evaluate.html",
                           dataplot = myimage,                             
                           personal = personal,
                           filter = filter,
                           category = category,
                           minsystole = minsystole, 
                           maxsystole = maxsystole,
                           mindiastole = mindiastole,
                           maxdiastole = maxdiastole,
                           minpulse = minpulse,
                           maxpulse = maxpulse,
                           avgsystole = avgsystole,
                           avgdiastole = avgdiastole,
                           avgpulse = avgpulse )

def plotdata():
    userid = session["user_id"]
    conn = getDB()
    filter = {}
    filter["datefrom"] = ""
    filter["dateuntil"] = ""
    if request.method == "GET":
        tmp = request.args.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.args.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
    else:
        tmp = request.args.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.args.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
    measurements = get_measurements(conn, userid, filter)
    x_axis = []
    y_systole = []
    y_diastole = []
    y_pulse = []
    minx = -1
    maxx = 0
    miny = 0
    maxy = 0
    for data in measurements:
        x = datetime.datetime.fromisoformat(data["misodate"])
        x_axis.append(x)
        if minx == -1:
            minx = x
            maxx = x
            miny = data["systole"]
            maxy = data["systole"]
        else:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
        if miny > data["systole"]:
            miny = data["systole"]
        if miny > data["diastole"]:
            miny = data["diastole"]
        if miny > data["pulse"]:
            miny = data["pulse"]
        if maxy < data["pulse"]:
            maxy = data["pulse"]
        if maxy < data["diastole"]:
            maxy = data["diastole"]
        if maxy < data["systole"]:
            maxy = data["systole"]
        y_systole.append(data["systole"])
        y_diastole.append(data["diastole"])
        y_pulse.append(data["pulse"])

    size = 8 / 2.54 
    fig = Figure(figsize=(8,6), dpi=80)
    ax = fig.subplots()
#    ax.set_xbound(lower=minx-1, upper=maxx+1)
#    ax.set_xlim(minx-1, maxx+1)
    ax.set_ybound(lower=miny-5, upper=maxy+5)
    ax.set_ylim(miny-10, maxy+10)
    # Text in the x-axis will be displayed in 'YYYY-mm-dd' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='center')

    line, = ax.plot(x_axis, y_systole, color='red', linewidth=2)
    line.set_label(_l('systolic blood pressure'))
    line, = ax.plot(x_axis, y_diastole, color='green', linewidth=2)
    line.set_label(_l('diastolic blood pressure'))
    line, = ax.plot(x_axis, y_pulse, color='blue', linewidth=2)
    line.set_label(_l('pulse'))
    ax.legend()
    ax.set_xlabel(_l('Date'), fontsize=15)
    ax.set_ylabel(_l('mmHg and Pulse'), fontsize=15)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'
#    return f"<img src='data:image/png;base64,{data}'/>"
#    response = make_response(buf)
#    response.headers.set('Content-Type', 'image/png')
#    return response
