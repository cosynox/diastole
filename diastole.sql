CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    pwhash TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    birthday TEXT,
    body_height INTEGER DEFAULT 0,
    last_login TEXT DEFAULT current_timestamp,
    retries INTEGER DEFAULT 0 );

CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE measurements (
    id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid  INTEGER NOT NULL,
    mdate   TEXT NOT NULL DEFAULT current_timestamp,
    systole INTEGER,
    diastole    INTEGER,
    pulse   INTEGER,
    remarks TEXT);
CREATE INDEX userid ON measurements (userid);
CREATE INDEX date ON measurements(mdate);

CREATE TABLE weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid INTEGER NOT NULL,
    mdate TEXT NOT NULL DEFAULT current_timestamp,
    body_weight INTEGER DEFAULT 0 );

CREATE INDEX user2 ON weights (userid);
CREATE INDEX mdate2 ON weights (mdate);
