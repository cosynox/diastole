import csv
from flask import request, Response, make_response
from flask_babel import lazy_gettext as _l
from dbaccess import weight2int,temperature2int
from io import BytesIO, StringIO
from werkzeug import Response
from werkzeug.datastructures import Headers
from werkzeug.wsgi import wrap_file

def export_csv_blood_pressure(measurements ):
    """ Generate a csv blood pressure file for download
    """
    # The field names for the columns of the csv file
    texts = [_l("date"), _l("time"), _l("systolic"), _l("diastolic"), _l("pulse"), _l("remarks") ]
    # write the table header
    f = StringIO()
    writer = csv.DictWriter(f, fieldnames=texts)
    writer.writeheader()
    # write the lines in the table
    for m in measurements:
        row = {}
        row[_l("date")] = str(m["mdate"])
        row[_l("time")] = str(m["mtime"])
        row[_l("systolic")] = str(m["systole"])
        row[_l("diastolic")] = str(m["diastole"])
        row[_l("pulse")] = str(m["pulse"])
        row[_l("remarks")] = m["remarks"]
        writer.writerow(row)

    # write actual pdf file to binary doc and deliver it for download
    doc = f.getvalue()
    f.close()
    return respond_csv( doc, "blood_pressure.csv" )

def export_csv_weight(weights): 
    """ Generate a csv weight file for download
    """
    # The field names for the columns of the csv file
    texts = [_l("date"), _l("time"), _l("body_weight"), _l("remarks") ]
    # write the table header
    f = StringIO()
    writer = csv.DictWriter(f, fieldnames=texts)
    writer.writeheader()
    for m in weights:
        row = {}
        row[_l("date")] = str(m["mdate"])
        row[_l("time")] = str(m["mtime"])
        row[_l("body_weight")] = round(float(weight2int(m["body_weight"]) / 100.0),2)
        row[_l("remarks")] = m["remarks"]
        writer.writerow(row)

    # write actual csv file to binary doc and deliver it for download
    doc = f.getvalue()
    f.close()
    return respond_csv( doc, "body_weight.csv" )

def export_csv_temperature(temperatures): 
    """ Generate a csv temperature file for download
    """
   # The field names for the columns of the csv file
    texts = [_l("date"), _l("time"), _l("body_temperature"), _l("remarks") ]
    # write the table header
    f = StringIO()
    writer = csv.DictWriter(f, fieldnames=texts)
    writer.writeheader()
    for m in temperatures:
        row = {}
        row[_l("date")] = str(m["mdate"])
        row[_l("time")] = str(m["mtime"])
        row[_l("body_temperature")] = round(float(temperature2int(m["body_temperature"]) / 100.0),1)
        row[_l("remarks")] = m["remarks"]
        writer.writerow(row)

    # write actual csv file to binary doc and deliver it for download
    doc = f.getvalue()
    return respond_csv( doc, "body_temperature.csv" )
    
def respond_csv( doc, filename ):
    """ Send back a csv file for download
    """
    output = make_response(doc)
    output.headers["Content-Disposition"] = f"attachment; filename={filename}"
    output.headers["Content-type"] = "text/csv"
    return output    
