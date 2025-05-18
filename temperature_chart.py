import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, lazy_gettext as _l

from helpers import apology
from dbaccess import getDB, \
                    get_personal_info, \
                    get_temperatures, \
                    date_format, time_format, \
                    temperature2int

from pdftable import gen_pdf_temperature_chart

def temperature_chart():
    """ Generate a Body temperature chart
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

        temperatures = get_temperatures(conn, userid, filter)
        status = request.form.get("status")

    else:
        status = request.args.get("status")
        temperatures = get_temperatures(conn, userid, None)
    if len(temperatures) > 0:
        fltemperature = round(float(temperature2int(temperatures[0]["body_temperature"]) / 100.0),2)
        mintemperature = fltemperature 
        maxtemperature = fltemperature
    else:
        mintemperature = 0
        maxtemperature = 0
    sumtemperature = 0
    n = 0
    for data in temperatures:
        data["mdate"] = date_format(data["mdate"])
        data["mtime"] = time_format(data["mtime"])
        temperature = round(float(temperature2int(data["body_temperature"]) /100.0),2)
        if mintemperature > temperature:
            mintemperature = temperature
        if maxtemperature < temperature:
            maxtemperature = temperature    
        sumtemperature += temperature
        n += 1
    if n > 0:
        avgtemperature = round(sumtemperature / n ,1)
    else:
        avgtemperature = 0
    
    # do something
    conn.close()
    if status == "pdf":
        return gen_pdf_temperature_chart(personal,  temperatures)
    else:   
        return render_template( "temperature_chart.html",                             
                           personal = personal,
                           temperaturechart = temperatures,
                           filter = filter,
                           mintemp = mintemperature, 
                           maxtemp = maxtemperature,
                           avgtemp = avgtemperature)
