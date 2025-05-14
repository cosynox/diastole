# Manage blood pressure data and produce blood pressure chart
#### Video Demo:  https://youtu.be/aa_QreF2KcI
## Description:
    The program delivers a structure to record the data of
    the taken measurements of the blood pressure and the
    pulse of persons. It is possible to manage a number of
    persons with the program. It is possible to produce
    a chart of blood pressure data of a desired time frame
    as well in HTML as also as a PDF-document. One can
    also get simple statistics about the own data.
    The user only needs a www-browser and internet access.

## The idea
    Often, when I go to the doctor, he asks me to fill out a
    page with a chart of blood pressure measurements that I
    have to make myself at home. So the idea is to have a
    program where I can regularly take my own measurements
    and when the doctor asks me to fill out his form, I can
    present him simply my collected data that I can print out
    with my computer from a pdf file.
    Perhaps it is also possible to give the doctor access to
    my collected data in the internet so that one needs no
    paper or the doctor downloads the pdf blood pressure table
    himself.

### Understanding the Blood Pressure Chart
    A blood pressure chart is a simple yet valuable tool for
    tracking your blood pressure readings at home. It records:

    - Systolic and diastolic values
    - Date and time of each measurement
    - Pulse rate (optional but recommended)

    Since blood pressure can fluctuate throughout the day,
    noting the time of each reading helps provide a clearer
    picture of your overall heart health.

    By regularly updating your chart, you can monitor trends
    and share accurate information with your healthcare
    provider. This supports more precise diagnoses and better
    treatment planning.

#### Why Use a Blood Pressure Chart?
    High blood pressure (hypertension) often develops without
    noticeable symptoms, especially in:
    - Older adults
    - People with a family history of hypertension
    - Individuals with heart conditions or chronic illnesses
      like diabetes

    Using a blood pressure chart helps you:
    - Keep your readings under control
    - Detect unusual changes early
    - Take action before serious complications arise

    Regular monitoring empowers you to actively manage your
    health.

## Preliminary considerations - the plan

    What to keep in mind for every project is that small
    systems beat big intentions and the kiss-principle:
    "keep it simple and stupid".

    A page with a blood pressure table looks like that:

    Blood pressure chart

    Last name:  Schiller                     Date of birth: 1759-11-10
    First name: Friedrich

    Date    |   Time   | Systole | Diastole | Pulse | Remarks
    -----------+----------+---------+----------+-------+----------------
    2025-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    2 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    3 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    4 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    5 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    6 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    7 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    8 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    9 25-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    10 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    11 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    12 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    13 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    14 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    15 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    16 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    17 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    18 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    19 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    20 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    21 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    22 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    23 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    24 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    25 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    26 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    27 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    28 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    29 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
    -----------+----------+---------+----------+-------+----------------
    30 5-05-05 | 09:41 AM |   153   |    102   |  120  | This is a test
            1         2         3         4         5         6
    12345678901234567890123456789012345678901234567890123456789012345678

    This or something equivalent shall be produced by the program.

    It shall also be possible to get the pdf of an empty table, to fill
    it out manually.

    What one sees at the table is, that there is a header for a person
    that consists of the first name, the last name and the birthday of
    the person, and there are table rows of blood pressure data
    consisting of date, time, systole in mmHg, diastole in mmHg, pulse,
    and a field for remarks.

    Initially, when one has logged in, one sees the page of the
    persons blood pressure table with the option to format and
    download it as a pdf file.

    And we need a page to edit the persons data.
    Initially the header data is empty.
    It shall be possible to edit and save a persons header data
    after the person is registered.

    We also need a page to enter one blood pressure measurement.
    On the top of the page shall be written the persons name and
    the birthday.

    There shall be buttons to save the data and it
    shall be possible to scroll through the measurements, delete a
    dataset or change the recorded data. But not accidentally.

    Initially the page shows the last entered dataset or an empty
    page with buttons.

    One shall have a button to edit or delete the displayed dataset
    and one shall have a button to get a form to enter a new dataset.
    On the left and on the right side shall be buttons to scroll one
    dataset backward or one dataset forward.

    On the form of the new dataset there shall be a button to save
    it as a new dataset. When the dataset has been saved the new
    saved dataset shall be displayed.

    It shall also be possible that a person deletes his
    own data from the database als well as his whole registration.

    And, of course, we need a register page, a login page and a logout
    button.

    What I like, is the layout of my current homepage. The idea with
    pages that look like A4 paper pages is good. Especially elder
    people want pages with not very much distraction in an easy to
    read layout. The old paper A4 pages are ideal for something
    like that.

    So I will reuse the layout of my homepage and I will use the
    same kind of menu. But the menu must not be fixed but generated
    by the python program.

    One thing that is of great importance is, that the pages must
    be easy to be handled with a mobile phone because a lot of
    people have their mobile phones to record their data.

    I don't think that I will need a lot of javascript. Perhaps one
    can use javascript to preset date and time of the blood pressure
    measurement. The interface shall not be fancy in any way.
    It shall be functional, simple and stupid.

    In order for the program to be easier integrated into existing
    web sites the routes for the program should all begin with an
    identifying string. I take the string "/diastole".

    What is also needed is a SQL-script to create the database
    correctly.

    The program shall also offer a simple means of evaluation of
    the data.

    Limits for blood pressure

    categorie                           systolic        diastolic
    low                                 < 100           < 60
    optimal                             < 120           < 80
    normal                              < 130           < 85
    high-normal                         130 - 139       85 - 89
    grade 1 (mild hypertonia)           140 - 159       90 - 99
    grade 2 (moderate hypertonia)       160 - 179       100 - 109
    grade 3 (severe hypertonia)         >= 180          >= 110

    source: https://www.hirslanden.ch/de/corporate/fuer-alle-folgen-des-lebens/kardiologie/blutdruck-blutdruckwerte.html
    
    The programm shall calculate the maximum and minimum values
    for systolic, diastolic blood pressure and for the pulse, and
    an average of the values.

    The english abbreviation for systolic blood pressure is SBP.
    The english abbreviation for diastolic blood pressure is DBP.

    The blood pressure is measured in mmHg. 1 mmHg is about
    133 Pascal or 0.00133 bar.

    It should draw a graphic chart of the values and calculate a
    trend line that can show whether the values are eventually 
    rising or falling.


    The same is for weights.

    The body mass index is calculated according to the formula:
        bmi = body weight / (body height * body height)
    
    Limits for weight
    
    Category                        BMI
    underweight                    < 18.5
    normal weight                  18.5 - 24.9
    overweight                     >= 25
    pre obesity                    25 - 29.9
    obesity grade 1                30 - 34.9
    obesity grade 2                35 - 39.9
    obesity grade 3                >= 40

    source: https://adipositas-gesellschaft.de/ueber-adipositas/definition-von-adipositas/

    

## Used libraries
    The program will be implemented with python, flask and sqlite3
    database. There shall be no reference to the cs50 module. The
    sqlite3 functions shall be used directly. Transactions shall be
    used. Every function that uses the database shall connect self
    and close the connection again after using the database.
    In order to give as few data as possible to the "outside" world,
    the bootstrap code and font code from google shall be placed in
    the apps static folder.

## Structure of the program

##  The database
    It will be used a sqlite3 database. A database diastole.db will
    be created. The tables are the following:

    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        pwhash TEXT NOT NULL,
        firstname TEXT,
        lastname TEXT,
        birthday TEXT
        );

    This is the table of the users of the program.

    username  is the name with which the user logs in into the program.
    pwhash    is the encrypted password.
    firstname is the first name of the user to be printed on forms and
              the blood pressure table
    lastname  is the last name of the user to be printed on forms and
              the blood pressure table
    birthday  is the date of birth encoded as
              ISO8601 string ("YYYY-MM-DD HH:MM:SS.SSS").
              Only the date part of the string shall be used for forms
              and the blood pressure table

    It will be created a unique index on the field username to ensure
    that every username is unique.

    CREATE UNIQUE INDEX username ON users (username);

    This is the table of the blood pressure measurements

    CREATE TABLE measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        userid INTEGER NOT NULL,
        mdate  TEXT NOT NULL DEFAULT current_timestamp,
        systole INTEGER,
        diastole INTEGER,
        pulse INTEGER,
        remarks TEXT);

    The meaning of the fields are the following
    id        the unique id of the measurement
    userid    the foreign key into the user table(id)
    mdate     the date and time of the measurement, here also the time
              is important because one user can take multiple
              measurements per day. If the user enters nothing, then
              simply the current timestamp is taken as date
    systole   the systolic blood pressure value
    diastole  the diastolic blood pressure value
    pulse     the pulse during the measurement
    remarks   here one can enter a special remark concerning the
              measurement, perhaps a remark that explains a value

    To enhance the database performance there will be created the
    following indices:

    CREATE INDEX userid ON measurements (userid);
    CREATE INDEX date ON measurements(date);

    There is a diastole.sql file that contains all the sql commands
    to create the database.

    It has to be called like

    sqlite3 diastole.db <diastole.sql


### Helper functions
    All database related actions are in a separate module to keep
    the main app.py free of these things. It should be possible
    to test them separately with pytest.
    All route related actions are in the file app.py.

### Classes
    In order to have a better structure, the program uses classes
    if appropriate.

## Installing the program
    preconditions: sqlite3 is installed, python3 is installed

    copy the sources in the appropriate directories

    run the sql script to create the database diastole.db
    It has to be called with the sqlite3 CLI like

    sqlite3 diastole.db <diastole.sql


## Deploying the program on the apache2 web server with uwsgi

    Simple example installation steps

    preconditions: apache2 is installed and working

    enable mod_proxy on apache2

    a2enable mod_proxy

    enter the following line in the apache site configuration

    ProxyPass /diastole http://127.0.0.1:9090/diastole

    restart apache server

    place the static files of the python app in the static
    folder of the apache DocumentRoot Directory or modify
    the links in your templates.

    Make a new python environment

    activate the python environment
    install the needed python modules in the environment
    with pip install -r requirements.txt

    copy the python app.py to the directory

    install the uwsgi-server. also install the python3 plugin

    start the uwsgi server in the directory of the app.py file
    or modify the path of --wsgi-file

    Example for starting the uwsgi server
    #! /bin/bash
    uwsgi --plugin python3 --http-socket :9090 --callable app \
    --wsgi-file app.py -H /home/userxyz/python/env/ --master \
    --processes 2 --threads 2 &
    (modify userxyz according to your own needs)

    That should do it.

    Do not forget to adapt the firewall settings to the open
    port of uwsgi on the server.


TEST





