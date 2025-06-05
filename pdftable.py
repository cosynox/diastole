import os
from fpdf import FPDF
from flask import Flask, request, session, Response
from flask_babel import Babel, lazy_gettext as _l
from dbaccess import date_format, time_format, weight2int,temperature2int
from io import BytesIO
from werkzeug import Response
from werkzeug.datastructures import Headers
from werkzeug.wsgi import wrap_file


def write_header(pdf, personal, heading):
    LINE = int(round(12 * 1.3,0))
   # write top of page
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.set_text_color(0,0,0)
    startpos = 3 * LINE
    leftmargin = 48
    s = ""
    s = heading
    pdf.text(leftmargin, startpos, s)
    pdf.set_font("Helvetica", style="", size=12)
    s = "0123456789"
    width = int(round(pdf.get_string_width(s) / 10,0))
    startpos += 2 * LINE
    s = _l("Last name :")
    pdf.text(leftmargin, startpos, s)
    s = personal["lastname"]
    pdf.text(leftmargin + (12 * width), startpos, s)
    s = _l("Date of birth :")
    pdf.text(leftmargin + (50 * width), startpos, s)
    s = personal["birthday"]
    pdf.text(leftmargin + (62 * width), startpos, s)
    startpos += 1 * LINE
    s = _l("First name :")
    pdf.text(leftmargin, startpos, s)
    s = personal["firstname"]
    pdf.text(leftmargin + (12 * width), startpos, s)
    s = _l('Body height') + " (cm):"
    pdf.text(leftmargin + (48 * width), startpos, s)
    s = str(personal["body_height"])
    pdf.text(leftmargin + (64 * width), startpos, s)
    return startpos


def gen_pdfchart(personal,  measurements,
                            minsystole,
                            maxsystole,
                            mindiastole,
                            maxdiastole,
                            minpulse,
                            maxpulse,
                            avgsystole,
                            avgdiastole,
                            avgpulse):
    """ Generate a pdf blood pressure chart for download
    """
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    leftmargin = 48
    LINE = int(round(12 * 1.3,0))
    pdf.set_font("Helvetica", style="", size=12)
    s = "AB01234567"
    width = int(round(pdf.get_string_width(s) / 10,0))

    # write page header with personal info
    heading = _l("Blood pressure chart")
    startpos = write_header(pdf, personal, heading)

   # The texts and positions of the row colums of the table 
    positions = [ 2 * width, 12 * width, 22 * width, 34 * width, 46 * width, 56 * width ]
    texts = [_l("date"), _l("time"), _l("systolic"), _l("diastolic"), _l("pulse"), _l("remarks") ]
    textlen = []
    # write the table header
    j = 0
    startpos += 2 * LINE
    pdf.set_font("Helvetica", style="B", size=12)
    for position in positions:
        s = texts[j]
        textlen.append(pdf.get_string_width(s))
        pdf.text(leftmargin + position, startpos, s)
        j += 1
    # write the lines in the table
    i = 0
    la = 1.5
    startpos += 1 * LINE * la
    while i < len(measurements):
        pdf.set_font("Helvetica", style="", size=12)
        printline = 0
        while printline < 28:
            if printline < len(measurements) and i < len(measurements):
                s = str(measurements[i]["mdate"])
                pdf.text(leftmargin+positions[0]-6,startpos + printline * LINE * la, s )
                s = measurements[i]["mtime"]
                if s.isascii() :
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, s )
                else:
                    t = ""
                    for c in s:
                        if ord(c) >= 128:
                            c = ' '
                        if ord(c) < 32:
                            c = ' '
                        t = t + c
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, t )
                s = str(measurements[i]["systole"])
                position = leftmargin+positions[2] + pdf.get_string_width(texts[2]) - pdf.get_string_width(s)
                pdf.text(position,startpos + printline * LINE * la, s )
                s = str(measurements[i]["diastole"])
                position = leftmargin+positions[3] + pdf.get_string_width(texts[3]) - pdf.get_string_width(s)
                pdf.text(position,startpos + printline * LINE * la , s )
                s = str(measurements[i]["pulse"])
                position = leftmargin+positions[4] + pdf.get_string_width(texts[4]) - pdf.get_string_width(s)
                pdf.text(position,startpos + printline * LINE * la , s )
                s = measurements[i]["remarks"]
                position = leftmargin+positions[5]
                pdf.text(position,startpos + printline * LINE * la, s )
            i += 1
            printline += 1
        if i < len(measurements):
            # This is the logic for multiple pages
            pdf.add_page()
            startpos = write_header(pdf, personal, heading)
            j = 0
            startpos += 2 * LINE
            # Here comes again the table header
            pdf.set_font("Helvetica", style="B", size=12)
            for position in positions:
                s = texts[j]
                pdf.text(leftmargin + position, startpos, s)
                j += 1
            startpos += 1 * LINE * la

    # write actual pdf file to binary doc and deliver it for download
    doc = pdf.output(dest='S')
    return respond_pdf( doc, "blood_pressure_chart.pdf" )

def gen_pdf_weight_chart(personal,  weights): 
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    leftmargin = 48
    LINE = int(round(12 * 1.3,0))
    pdf.set_font("Helvetica", style="", size=12)
    s = "AB01234567"
    width = int(round(pdf.get_string_width(s) / 10,0))
    heading = _l("Body weight chart")
    startpos = write_header(pdf, personal, heading)
   # write top of page
    positions = [ 2 * width, 12 * width, 22 * width, 38 * width ]
    texts = [_l("date"), _l("time"), _l("body weight"), _l("remarks") ]
    textlen = []
    # write the table header
    j = 0
    startpos += 2 * LINE
    pdf.set_font("Helvetica", style="B", size=12)
    for position in positions:
        s = texts[j]
        textlen.append(pdf.get_string_width(s))
        pdf.text(leftmargin + position, startpos, s)
        j += 1

    i = 0
    la = 1.5
    startpos += 1 * LINE * la
    while i < len(weights):
        pdf.set_font("Helvetica", style="", size=12)
        printline = 0
        while printline < 28:
            if printline < len(weights) and i < len(weights):
                # write date
                s = str(weights[i]["mdate"])
                pdf.text(leftmargin+positions[0]-6,startpos + printline * LINE * la, s )    
                # write time 
                s = weights[i]["mtime"]
                if s.isascii() :
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, s )
                else:
                    t = ""
                    for c in s:
                        if ord(c) >= 128:
                            c = ' '
                        if ord(c) < 32:
                            c = ' '
                        t = t + c
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, t )
                # write body weight
                wgt = round(float(weight2int(weights[i]["body_weight"]) / 100.0),2)                    
                s = f"{wgt:.2f} kg"
                position = leftmargin+positions[2] + pdf.get_string_width(texts[2]) - pdf.get_string_width(s)
                pdf.text(position,startpos + printline * LINE * la, s )
                # write remarks
                s = weights[i]["remarks"]
                position = leftmargin+positions[3]
                pdf.text(position,startpos + printline * LINE * la, s )
            i += 1
            printline += 1
        if i < len(weights):
            # This is the logic for multiple pages
            pdf.add_page()
            startpos = write_header(pdf, personal, heading)
            j = 0
            startpos += 2 * LINE
            # Here comes again the table header
            pdf.set_font("Helvetica", style="B", size=12)
            for position in positions:
                s = texts[j]
                pdf.text(leftmargin + position, startpos, s)
                j += 1
            startpos += 1 * LINE * la

    # write actual pdf file to binary doc and deliver it for download
    doc = pdf.output(dest='S')
    return respond_pdf( doc, "body_weight_chart.pdf" )


def gen_pdf_temperature_chart(personal,  temperatures): 
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    leftmargin = 48
    LINE = int(round(12 * 1.3,0))
    pdf.set_font("Helvetica", style="", size=12)
    s = "AB01234567"
    width = int(round(pdf.get_string_width(s) / 10,0))
    heading = _l("Temperature chart")
    startpos = write_header(pdf, personal, heading)
   # write top of page
    positions = [ 2 * width, 12 * width, 22 * width, 38 * width ]
    texts = [_l("date"), _l("time"), _l("temperature"), _l("remarks") ]
    textlen = []
    # write the table header
    j = 0
    startpos += 2 * LINE
    pdf.set_font("Helvetica", style="B", size=12)
    for position in positions:
        s = texts[j]
        textlen.append(pdf.get_string_width(s))
        pdf.text(leftmargin + position, startpos, s)
        j += 1

    i = 0
    la = 1.5
    startpos += 1 * LINE * la
    while i < len(temperatures):
        pdf.set_font("Helvetica", style="", size=12)
        printline = 0
        while printline < 28:
            if printline < len(temperatures) and i < len(temperatures):
                # write date
                s = str(temperatures[i]["mdate"])
                pdf.text(leftmargin+positions[0]-6,startpos + printline * LINE * la, s )    
                # write time 
                s = temperatures[i]["mtime"]
                if s.isascii() :
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, s )
                else:
                    t = ""
                    for c in s:
                        if ord(c) >= 128:
                            c = ' '
                        if ord(c) < 32:
                            c = ' '
                        t = t + c
                    pdf.text(leftmargin+positions[1],startpos + printline * LINE * la, t )
                # write body temperature
                temperature = round(float(temperature2int(temperatures[i]["body_temperature"]) / 100.0),1)                    
                s = f"{temperature:.2f} °C"
                position = leftmargin+positions[2] + pdf.get_string_width(texts[2]) - pdf.get_string_width(s)
                pdf.text(position,startpos + printline * LINE * la, s )
                # write remarks
                s = temperatures[i]["remarks"]
                position = leftmargin+positions[3]
                pdf.text(position,startpos + printline * LINE * la, s )
            i += 1
            printline += 1
        if i < len(temperatures):
            # This is the logic for multiple pages
            pdf.add_page()
            startpos = write_header(pdf, personal, heading)
            j = 0
            startpos += 2 * LINE
            # Here comes again the table header
            pdf.set_font("Helvetica", style="B", size=12)
            for position in positions:
                s = texts[j]
                pdf.text(leftmargin + position, startpos, s)
                j += 1
            startpos += 1 * LINE * la


    # write actual pdf file to binary doc and deliver it for download
    doc = pdf.output(dest='S')
    return respond_pdf( doc, "body_temperature_chart.pdf" )

    
def respond_pdf( doc, filename ):
    b = BytesIO(doc)
    w = wrap_file(request.environ, b)
    s = f'attachment; filename="{filename}"'
    d = Headers([('Content-Disposition', s)])
    return Response(w, mimetype="application/x-pdf",
                    headers=d,
                    direct_passthrough=True)
