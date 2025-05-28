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
                    get_weights, \
                    get_personal_info, date_format

from pdftable import write_header, respond_pdf

def weight_evaluation():
    """ Evaluate the body weight chart of a person
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

    if request.method == "POST":

        tmp = request.form.get("datefrom")
        if len(tmp) > 0:
            filter["datefrom"] = tmp

        tmp = request.form.get("dateuntil")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp

        status = request.form.get("status")

    else:
        tmp = request.args.get("datefrom", "")
        if len(tmp) > 0:
            filter["datefrom"] = tmp

        tmp = request.args.get("dateuntil", "")
        if len(tmp) > 0:
            filter["dateuntil"] = tmp

        status = request.args.get("status")

    weights = get_weights(conn, userid, filter)
    if len(weights) > 0:
        try:
            minweight = float(weights[0]["body_weight"]) 
            maxweight = minweight
            lastweight = minweight
        except IndexError:
            minweight = 0
            maxweight = 0
            lastweight = 0
            
    else:
        minweight = 0
        maxweight = 0
        lastweight = 0
    sumweight = 0
    n = 0
    for data in weights:
        flweight =  float(data["body_weight"])
        if minweight > flweight:
            minweight = flweight
        if maxweight < flweight:
            maxweight = flweight    
        lastweight = flweight 
        sumweight += flweight
        n += 1
    if n > 0:
        avgweight = round(sumweight / n ,1)
    else:
        avgweight = 0


    bmi = body_mass_index(lastweight, personal["body_height"] / 100.0)

    category = _l("undefined")

    if bmi < 18.5:
        category = _l("underweight")
    elif bmi >= 18.5 and bmi < 25:
        category = _l("normal weight")
    elif bmi >= 25 and bmi < 30:
        category = _l("pre obesity")
    elif bmi >= 30 and bmi < 35:
        category = _l("obesity grade 1")
    elif bmi >= 35 and bmi < 40:
        category = _l("obesity grade 2")
    elif bmi >= 40:
        category = _l("obesity grade 3")

    conn.close()
    if status == 'pdf':
        return gen_pdfweightdiagram(personal,  weights)
    else:
        myimage = weight_plotdata(weights)
        return render_template( "weight_evaluate.html",
                           dataplot = myimage,                             
                           personal = personal,
                           filter = filter,
                           category = category,
                           minweight = minweight, 
                           maxweight = maxweight,
                           avgweight = avgweight,
                           bmi = bmi)

def weight_plotdata(weights):
    x_axis = []
    y_weight = []
    minx = -1
    maxx = 0
    miny = 0
    maxy = 0
    for data in weights:
        x = datetime.datetime.fromisoformat(data["misodate"])
        x_axis.append(x)
        flweight =  float(data["body_weight"]) 
        if minx == -1:
            minx = x
            maxx = x
            miny = flweight
            maxy = flweight
        else:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
        if miny > flweight:
            miny = flweight
        if maxy < flweight:
            maxy = flweight
        y_weight.append(flweight)

    size = 8 / 2.54 
    fig = Figure(figsize=(8,6), dpi=80)
    ax = fig.subplots()
#    ax.set_xbound(lower=minx-1, upper=maxx+1)
#    ax.set_xlim(minx-1, maxx+1)
    ax.set_ybound(lower=miny-2, upper=maxy+2)
    ax.set_ylim(miny-4, maxy+4)

    # Text in the x-axis will be displayed in 'YYYY-mm-dd' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='center')

    line, = ax.plot(x_axis, y_weight, color='blue', marker="o",  linewidth=2)
    line.set_label(_l('body weight'))
    ax.set_title(_l("Weight diagram"), loc='center')
    ax.legend()
    ax.set_xlabel(_l('Date'), fontsize=15)
    ax.set_ylabel(_l('kg'), fontsize=15)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'
#    return f"<img src='data:image/png;base64,{data}'/>"
#    response = make_response(buf)
#    response.headers.set('Content-Type', 'image/png')
#    return response

def body_mass_index( weight_in_kg, body_height_in_m):
    try:
        bmi = weight_in_kg / float(body_height_in_m * body_height_in_m)
    except ZeroDivisionError:
        bmi = 0

    bmi = round(bmi,1)
    return bmi

def gen_pdfweightdiagram(personal,  weights):
    """ Generate a pdf weight diagram for download
    """
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    leftmargin = 48
    LINE = int(round(12 * 1.3,0))
    pdf.set_font("Helvetica", style="", size=12)
    s = "AB01234567"
    width = int(round(pdf.get_string_width(s) / 10,0))

    # write page header with personal info
    heading = _l("Weight diagram")
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
    y_weight = []
    minx = -1
    maxx = 0
    miny = 0
    maxy = 0
    for data in weights:
        x = datetime.datetime.fromisoformat(data["misodate"])
        x_axis.append(x)
        flweight =  float(data["body_weight"]) 
        if minx == -1:
            minx = x
            maxx = x
            miny = flweight
            maxy = flweight

        else:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
        if miny > flweight:
            miny = flweight
        if maxy < flweight:
            maxy = flweight
        y_weight.append(flweight)

    size = 8 / 2.54 
    fig = Figure(figsize=(8,6), dpi=300)
    ax = fig.subplots()
#    ax.set_xbound(lower=minx-1, upper=maxx+1)
#    ax.set_xlim(minx-1, maxx+1)
    ax.set_ybound(lower=miny-2, upper=maxy+2)
    ax.set_ylim(miny-4, maxy+4)
    # Text in the x-axis will be displayed in 'YYYY-mm-dd' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='center')

    line, = ax.plot(x_axis, y_weight, color='blue', marker="o", linewidth=2)
    line.set_label(_l('body weight'))
    ax.legend()
    ax.set_title(_l("Weight diagram"), loc='center')
    ax.set_xlabel(_l('Date'), fontsize=15)
    ax.set_ylabel(_l('kg'), fontsize=15)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    pdf.image(buf,leftmargin, startpos, w=pdf.epw)  # Make the image full width
   # write actual pdf file to binary doc and deliver it for download
    doc = pdf.output(dest='S')
    return respond_pdf( doc, "weight_diagram.pdf" )


