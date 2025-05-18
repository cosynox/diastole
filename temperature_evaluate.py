import datetime
import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, make_response
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l
from fpdf import FPDF
from io import BytesIO
import base64 
from matplotlib.figure import Figure
from matplotlib.dates import datestr2num
import matplotlib.dates as mdates
from helpers import apology
from dbaccess import getDB, \
                    get_temperatures, \
                    get_personal_info, date_format

from pdftable import write_header, respond_pdf

def temperature_evaluation():
    """ Evaluate the body temperature chart of a person
    """
    conn = getDB()
    userid = session["user_id"]
    conn = getDB()
    filter = {}
    filter["datefrom"] = ""
    filter["dateuntil"] = ""
    status = ""
    personal = get_personal_info(conn, userid)
    personal["birthday"] = date_format(personal["birthday"])
    if request.method == "GET":
        tmp = request.args.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.args.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
        status = request.args.get("status")

    elif request.method == "POST":
        tmp = request.form.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp
        tmp = request.form.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp
        status = request.form.get("status")
    
    temperatures = get_temperatures(conn, userid, filter)
    if len(temperatures) > 0:
        try:
            mintemperature = float(temperatures[0]["body_temperature"]) 
            maxtemperature = mintemperature
            lasttemperature = mintemperature
        except IndexError:
            mintemperature = 0
            maxtemperature = 0
            lasttemperature = 0
            
    else:
        mintemperature = 0
        maxtemperature = 0
        lasttemperature = 0
    sumtemperature = 0
    n = 0
    for data in temperatures:
        fltemperature =  float(data["body_temperature"])
        if mintemperature > fltemperature:
            mintemperature = fltemperature
        if maxtemperature < fltemperature:
            maxtemperature = fltemperature    
        lasttemperature = fltemperature 
        sumtemperature += fltemperature
        n += 1
    if n > 0:
        avgtemperature = round(sumtemperature / n ,1)
    else:
        avgtemperature = 0

    category = _l("undefined")

    if lasttemperature < 20.0:
        category = _l("cold death")
    elif lasttemperature < 27.0:
        category = _l("maybe deadly cold")
    elif lasttemperature < 33.0:
        category = _l("hypothermia")
    elif lasttemperature >= 35.0 and lasttemperature < 36.3: 
        category = _l("under temperature")
    elif lasttemperature >= 36.3 and lasttemperature <= 37.4:
        category = _l("normal temperature") 
    elif lasttemperature > 37.4 and lasttemperature < 38.1:
        category = _l("increased temperature")
    elif lasttemperature >= 38.1 and lasttemperature < 38.6:
        category = _l("slight fever")
    elif lasttemperature >= 38.6 and lasttemperature < 39.1:
        category = _l("fever")
    elif lasttemperature >= 39.1 and lasttemperature < 40.0:
        category = _l("high fever")
    elif lasttemperature >= 40.0 and lasttemperature < 42.0:
        category = _l("very high fever")
    elif lasttemperature >= 42.0 and lasttemperature < 44.0:
        category = _l("circulatory collapse")
    else:
        category = _l("heat death, thermal denaturation of proteins")    

    conn.close()
    if status == 'pdf':
        return gen_pdftemperaturediagram(personal,  temperatures)
    else:
        myimage = temperature_plotdata()
        return render_template( "temperature_evaluate.html",
                           dataplot = myimage,                             
                           personal = personal,
                           filter = filter,
                           category = category,
                           mintemp = mintemperature, 
                           maxtemp = maxtemperature,
                           avgtemp = avgtemperature)

def temperature_plotdata():
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
    temperatures = get_temperatures(conn, userid, filter)
    x_axis = []
    y_temperature = []
    minx = -1
    maxx = 0
    miny = 0
    maxy = 0
    for data in temperatures:
        x = datetime.datetime.fromisoformat(data["misodate"])
        x_axis.append(x)
        fltemperature =  float(data["body_temperature"]) 
        if minx == -1:
            minx = x
            maxx = x
            miny = fltemperature
            maxy = fltemperature
        else:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
        if miny > fltemperature:
            miny = fltemperature
        if maxy < fltemperature:
            maxy = fltemperature
        y_temperature.append(fltemperature)

    size = 8 / 2.54 
    fig = Figure(figsize=(8,6), dpi=80)
    ax = fig.subplots()
#    ax.set_xbound(lower=minx-1, upper=maxx+1)
#    ax.set_xlim(minx-1, maxx+1)
    ax.set_ybound(lower=miny-1, upper=maxy+1)
    ax.set_ylim(miny-2, maxy+2)

    # Text in the x-axis will be displayed in 'YYYY-mm-dd' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='center')

    line, = ax.plot(x_axis, y_temperature, color='blue', marker="o",  linewidth=2)
    line.set_label(_l('body temperature'))
    ax.set_title(_l("temperature diagram"), loc='center')
    ax.legend()
    ax.set_xlabel(_l('Date'), fontsize=15)
    ax.set_ylabel(_l('°C'), fontsize=15)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'
#    return f"<img src='data:image/png;base64,{data}'/>"
#    response = make_response(buf)
#    response.headers.set('Content-Type', 'image/png')
#    return response


def gen_pdftemperaturediagram(personal,  temperatures):
    """ Generate a pdf temperature diagram for download
    """
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    leftmargin = 48
    LINE = int(round(12 * 1.3,0))
    pdf.set_font("Helvetica", style="", size=12)
    s = "AB01234567"
    width = int(round(pdf.get_string_width(s) / 10,0))

    # write page header with personal info
    heading = _l("temperature diagram")
    startpos = write_header(pdf, personal, heading)

    # write the table header
    j = 0
    startpos += 2 * LINE
    pdf.set_font("Helvetica", style="", size=12)
    # write the lines in the table
    i = 0
    la = 1.5
    startpos += 1 * LINE * la

    x_axis = []
    y_temperature = []
    minx = -1
    maxx = 0
    miny = 0
    maxy = 0
    for data in temperatures:
        x = datetime.datetime.fromisoformat(data["misodate"])
        x_axis.append(x)
        fltemperature =  float(data["body_temperature"]) 
        if minx == -1:
            minx = x
            maxx = x
            miny = fltemperature
            maxy = fltemperature

        else:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
        if miny > fltemperature:
            miny = fltemperature
        if maxy < fltemperature:
            maxy = fltemperature
        y_temperature.append(fltemperature)

    size = 8 / 2.54 
    fig = Figure(figsize=(8,6), dpi=300)
    ax = fig.subplots()
#    ax.set_xbound(lower=minx-1, upper=maxx+1)
#    ax.set_xlim(minx-1, maxx+1)
    ax.set_ybound(lower=miny-1, upper=maxy+1)
    ax.set_ylim(miny-2, maxy+2)
    # Text in the x-axis will be displayed in 'YYYY-mm-dd' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='center')

    line, = ax.plot(x_axis, y_temperature, color='blue', marker="o", linewidth=2)
    line.set_label(_l('body temperature'))
    ax.legend()
    ax.set_title(_l("temperature diagram"), loc='center')
    ax.set_xlabel(_l('Date'), fontsize=15)
    ax.set_ylabel(_l('°C'), fontsize=15)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    pdf.image(buf,leftmargin, startpos, w=pdf.epw)  # Make the image full width
   # write actual pdf file to binary doc and deliver it for download
    doc = pdf.output(dest='S')
    return respond_pdf( doc, "temperature_diagram.pdf" )


