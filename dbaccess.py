import os
from datetime import datetime, date
from flask import request, current_app
from babel.dates import format_date,format_time
import sqlite3

def get_locale():
    """ return the desired language """
    # return "en"
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def getDB():
    conn = sqlite3.connect('diastole.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_personal_info(conn, userid):
    cur = conn.cursor()
    cur.execute("SELECT firstname, lastname, birthday, body_height FROM users WHERE id = ?", (userid,))
    rows = cur.fetchall()
    if len(rows) > 0:
        result = {}
        if rows[0]["firstname"] != None:
            result["firstname"] = rows[0]["firstname"]
        else:
            result["firstname"] = ""
        if rows[0]["lastname"] != None:
            result["lastname"] = rows[0]["lastname"]
        else:
            result["lastname"] = ""
        if rows[0]["birthday"] != None:
            result["birthday"] = rows[0]["birthday"]
        else:
            result["birthday"] = ""
        try:
            result["body_height"] = int( rows[0]["body_height"] )
        except (ValueError, TypeError):
            result["body_height"] = 0
        return result
    else:
        return {}

def set_personal_info(conn, info):
    cur = conn.cursor()
    rval = True
    try:
        cur.execute(
        """UPDATE users \
        SET firstname = ?, \
        lastname = ?, \
        birthday = ?, \
        body_height = ? \
        WHERE id = ?""", (info["firstname"], info["lastname"], info["birthday"], info["body_height"], info["id"],))
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def get_last_measurement(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return {}

def get_first_measurement(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   ORDER BY id ASC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return {}

def get_next_measurement(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND id > ? \
                   ORDER BY id ASC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return get_last_measurement(conn,userid)

def get_previous_measurement(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND id < ? \
                   ORDER BY id DESC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return get_first_measurement(conn,userid)

def get_this_measurement(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND id = ? LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return {}

def is_first_measurement(conn, userid, recordId):
    mdata = get_first_measurement(conn,userid)
    result = True
    if mdata == {}:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def is_last_measurement(conn, userid, recordId):
    mdata = get_last_measurement(conn,userid)
    result = True
    if mdata == {}:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def get_measurement_five(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 5""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows
    else:
        return []

def get_measurements(conn, userid, filter):
    cur = conn.cursor()
    if filter == None or \
        (filter["datefrom"].strip() == "" and filter["dateuntil"].strip() == ""):
        cur.execute("""SELECT mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   ORDER BY mdate""", (userid,) )
    elif filter["datefrom"].strip() != "" and filter["dateuntil"].strip() != "" :
        cur.execute("""SELECT mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND mdate >= ?
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["datefrom"], filter["dateuntil"],) )
    elif filter["datefrom"].strip() != "":
        cur.execute("""SELECT mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND mdate >= ?
                   ORDER BY mdate""", (userid,filter["datefrom"],) )
    elif filter["dateuntil"].strip() != "":
        cur.execute("""SELECT mdate, systole, diastole, pulse, remarks \
                   FROM measurements \
                   WHERE userid = ? \
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["dateuntil"],) )
    rows = cur.fetchall()
    if len(rows) > 0:
        result = []
        for row in rows:
            nrow = {}
            nrow["misodate"] = row["mdate"]
            nrow["mdate"] = getDate( row["mdate"] )
            nrow["mtime"] = getTime( row["mdate"] )
            nrow["systole"] = row["systole"]
            nrow["diastole"] = row["diastole"]
            nrow["pulse"] = row["pulse"]
            nrow["remarks"] = row["remarks"]
            result.append(nrow)
        return result
    else:
        return []

def get_weights(conn, userid, filter):
    cur = conn.cursor()
    if filter == None or \
        (filter["datefrom"].strip() == "" and filter["dateuntil"].strip() == ""):
        cur.execute("""SELECT mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   ORDER BY mdate""", (userid,) )
    elif filter["datefrom"].strip() != "" and filter["dateuntil"].strip() != "" :
        cur.execute("""SELECT mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND mdate >= ?
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["datefrom"], filter["dateuntil"],) )
    elif filter["datefrom"].strip() != "":
        cur.execute("""SELECT mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND mdate >= ?
                   ORDER BY mdate""", (userid,filter["datefrom"],) )
    elif filter["dateuntil"].strip() != "":
        cur.execute("""SELECT mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["dateuntil"],) )
    rows = cur.fetchall()
    if len(rows) > 0:
        result = []
        for row in rows:
            nrow = {}
            nrow["misodate"] = row["mdate"]
            nrow["mtime"] = getTime( row["mdate"] )
            nrow["mdate"] = getDate( row["mdate"] )
            nrow["body_weight"] = int2weight(row["body_weight"])
            nrow["remarks"] = row["remarks"]
            result.append(nrow)
        return result
    else:
        return []

def get_last_weight(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_weight"] = int2weight(rows[0]["body_weight"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def get_first_weight(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   ORDER BY id ASC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_weight"] = int2weight(rows[0]["body_weight"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def get_next_weight(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND id > ? \
                   ORDER BY id ASC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_weight"] = int2weight(rows[0]["body_weight"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return get_last_weight(conn,userid)

def get_previous_weight(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND id < ? \
                   ORDER BY id DESC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_weight"] = int2weight(rows[0]["body_weight"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return get_first_weight(conn,userid)

def get_this_weight(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   AND id = ? LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_weight"] = int2weight(rows[0]["body_weight"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def is_first_weight(conn, userid, recordId):
    mdata = get_first_weight(conn,userid)
    result = True
    if mdata == None:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def is_last_weight(conn, userid, recordId):
    mdata = get_last_weight(conn,userid)
    result = True
    if mdata == None:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def get_weight_five(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT mdate, body_weight, remarks \
                   FROM weights \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 5""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        result = []
        for row in rows:
            nrow = {}
            nrow["misodate"] = row["mdate"]
            nrow["mtime"] = getTime( row["mdate"] )
            nrow["mdate"] = getDate( row["mdate"] )
            nrow["body_weight"] = int2weight(row["body_weight"])
            nrow["remarks"] = row["remarks"]
            result.append(nrow)
        return result
    else:
        return []


def append_weight(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """INSERT INTO weights \
        ( userid, mdate, body_weight, remarks ) \
        VALUES ( ?, ?, ?, ? )""",
         (userid, mdate, weight2int(info["body_weight"]), info["remarks"],))
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def is_weight( conn, userid, dataset_id ):
    cur = conn.cursor()
    cur.execute("""SELECT id FROM weights \
                   WHERE id = ? \
                   AND userid = ?""", (dataset_id, userid) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False

def update_weight(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """UPDATE weights \
        SET mdate = ?, \
            body_weight = ?, \
            remarks = ? \
        WHERE userid = ? \
        AND id = ?""", \
        (mdate, weight2int(info["body_weight"]), info["remarks"], \
         userid, info["id"],) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def delete_weight(conn, userid, recordId):
    cur = conn.cursor()
    rval = True
    try:
        cur.execute(
        """DELETE FROM weights \
        WHERE id = ?
        AND userid = ? LIMIT 1""",
        (recordId, userid,) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def weight2int( weight ):
    try:
        intweight = int(round(float(weight.replace(',', '.')),2) * 100) 
    except (ValueError, TypeError):
        intweight = 0
    return intweight

def int2weight( iweight ):
    flweight = round( iweight / 100.0, 2)
    weight = f"{flweight}"
    if "de" in get_locale():
        weight.replace('.', ',')
    return weight

def get_temperatures(conn, userid, filter):
    cur = conn.cursor()
    if filter == None or \
        (filter["datefrom"].strip() == "" and filter["dateuntil"].strip() == ""):
        cur.execute("""SELECT mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   ORDER BY mdate""", (userid,) )
    elif filter["datefrom"].strip() != "" and filter["dateuntil"].strip() != "" :
        cur.execute("""SELECT mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND mdate >= ?
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["datefrom"], filter["dateuntil"],) )
    elif filter["datefrom"].strip() != "":
        cur.execute("""SELECT mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND mdate >= ?
                   ORDER BY mdate""", (userid,filter["datefrom"],) )
    elif filter["dateuntil"].strip() != "":
        cur.execute("""SELECT mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND mdate <= ?
                   ORDER BY mdate""", (userid,filter["dateuntil"],) )
    rows = cur.fetchall()
    if len(rows) > 0:
        result = []
        for row in rows:
            nrow = {}
            nrow["misodate"] = row["mdate"]
            nrow["mtime"] = getTime( row["mdate"] )
            nrow["mdate"] = getDate( row["mdate"] )
            nrow["body_temperature"] = int2temperature(row["body_temperature"])
            nrow["remarks"] = row["remarks"]
            result.append(nrow)
        return result
    else:
        return []

def get_last_temperature(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_temperature"] = int2temperature(rows[0]["body_temperature"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def get_first_temperature(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   ORDER BY id ASC LIMIT 1""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_temperature"] = int2temperature(rows[0]["body_temperature"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def get_next_temperature(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND id > ? \
                   ORDER BY id ASC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_temperature"] = int2temperature(rows[0]["body_temperature"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return get_last_temperature(conn,userid)

def get_previous_temperature(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND id < ? \
                   ORDER BY id DESC LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_temperature"] = int2temperature(rows[0]["body_temperature"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return get_first_temperature(conn,userid)

def get_this_temperature(conn, userid, recordId):
    cur = conn.cursor()
    cur.execute("""SELECT id, userid, mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   AND id = ? LIMIT 1""", (userid,recordId,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        nrow = {}
        nrow["id"] = rows[0]["id"]
        nrow["userid"] = rows[0]["userid"]
        nrow["misodate"] = rows[0]["mdate"]
        nrow["mtime"] = getTime( rows[0]["mdate"] )
        nrow["mdate"] = getDate( rows[0]["mdate"] )
        nrow["body_temperature"] = int2temperature(rows[0]["body_temperature"])
        nrow["remarks"] = rows[0]["remarks"]
        return nrow
    else:
        return None

def is_first_temperature(conn, userid, recordId):
    mdata = get_first_temperature(conn,userid)
    result = True
    if mdata == None:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def is_last_temperature(conn, userid, recordId):
    mdata = get_last_temperature(conn,userid)
    result = True
    if mdata == None:
        result = True
    elif mdata["id"] == recordId:
        result = True
    else:
        result = False
    return result

def get_temperature_five(conn, userid):
    cur = conn.cursor()
    cur.execute("""SELECT mdate, body_temperature, remarks \
                   FROM temperatures \
                   WHERE userid = ? \
                   ORDER BY id DESC LIMIT 5""", (userid,) )
    rows = cur.fetchall()
    if len(rows) > 0:
        result = []
        for row in rows:
            nrow = {}
            nrow["misodate"] = row["mdate"]
            nrow["mtime"] = getTime( row["mdate"] )
            nrow["mdate"] = getDate( row["mdate"] )
            nrow["body_temperature"] = int2temperature(row["body_temperature"])
            nrow["remarks"] = row["remarks"]
            result.append(nrow)
        return result
    else:
        return []


def append_temperature(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """INSERT INTO temperatures \
        ( userid, mdate, body_temperature, remarks ) \
        VALUES ( ?, ?, ?, ? )""",
         (userid, mdate, temperature2int(info["body_temperature"]), info["remarks"],))
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def is_temperature( conn, userid, dataset_id ):
    cur = conn.cursor()
    cur.execute("""SELECT id FROM temperatures \
                   WHERE id = ? \
                   AND userid = ?""", (dataset_id, userid) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False

def update_temperature(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """UPDATE temperatures \
        SET mdate = ?, \
            body_temperature = ?, \
            remarks = ? \
        WHERE userid = ? \
        AND id = ?""", \
        (mdate, temperature2int(info["body_temperature"]), info["remarks"], \
         userid, info["id"],) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def delete_temperature(conn, userid, recordId):
    cur = conn.cursor()
    rval = True
    try:
        cur.execute(
        """DELETE FROM temperatures \
        WHERE id = ?
        AND userid = ? LIMIT 1""",
        (recordId, userid,) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def temperature2int( temperature ):
    try:
        inttemperature = int(round(float(temperature.replace(',', '.')),2) * 100) 
    except (ValueError, TypeError):
        inttemperature = 0
    return inttemperature

def int2temperature( itemperature ):
    fltemperature = round( itemperature / 100.0, 2)
    temperature = f"{fltemperature}"
    if "de" in get_locale():
        temperature.replace('.', ',')
    return temperature


def makeISODate ( mdate, mtime ):
    try:
        isodate = datetime.fromisoformat(mdate + ' ' + mtime).isoformat(sep=' ')
    except ValueError:
        return None
    return isodate

def getTime( mdate ):
    date = datetime.fromisoformat(mdate)
    return date.strftime("%H:%M")


def getDate( mdate ):
    date = datetime.fromisoformat(mdate)
    return date.strftime("%Y-%m-%d")

def append_measurement(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """INSERT INTO measurements \
        ( userid, mdate, systole, diastole, pulse, remarks ) \
        VALUES ( ?, ?, ?, ?, ?, ? )""",
         (userid, mdate, info["systole"],
          info["diastole"], info["pulse"], info["remarks"],))
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def is_measurement( conn, userid, dataset_id ):
    cur = conn.cursor()
    cur.execute("""SELECT id FROM measurements \
                   WHERE id = ? \
                   AND userid = ?""", (dataset_id, userid) )
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False

def update_measurement(conn, userid, info):
    cur = conn.cursor()
    rval = True
    mdate = makeISODate( info["mdate"], info["mtime"])
    try:
        cur.execute(
        """UPDATE measurements \
        SET mdate = ?, \
            systole = ?, \
            diastole = ?, \
            pulse = ?,
            remarks = ?
        WHERE userid = ?
        AND id = ?""",
        (mdate, info["systole"], info["diastole"], info["pulse"],
        info["remarks"], userid, info["id"],) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def delete_measurement(conn, userid, recordId):
    cur = conn.cursor()
    rval = True
    try:
        cur.execute(
        """DELETE FROM measurements \
        WHERE id = ?
        AND userid = ? LIMIT 1""",
        (recordId, userid,) )
    except sqlite3.OperationalError:
        rval = False
    except sqlite3.IntegrityError:
        rval = False
    conn.commit()
    return rval

def date_format(mdate):
    try:
        d = date.fromisoformat(mdate)
    except (TypeError, ValueError):
        return ""
    return format_date(d, locale=get_locale())

def time_format(mtime):
    try:
        d = datetime.strptime(mtime, '%H:%M').time()
    except (TypeError, ValueError):
        return ""
    return format_time(d, locale=get_locale())

if __name__ == "__main__":
    test = makeISODate( "1959-07-10", "01:20")
    print(getTime(test))
    print(getDate(test))
    d = date(2007, 4, 1)
    d = date.fromisoformat("1959-07-10")
    print( format_date(d, locale="de" ) )
    print( format_date(d, locale="en" ) )
    time_str = '13:20'
    time_object = datetime.strptime(time_str, '%H:%M').time()
    print(type(time_object))
    print(time_object)
    print( format_time(time_object, locale="de" ) )
    print( format_time(time_object, locale="en" ) )
