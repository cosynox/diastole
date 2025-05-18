CREATE TABLE temperatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid INTEGER NOT NULL,
    mdate TEXT NOT NULL DEFAULT current_timestamp,
    body_temperature INTEGER DEFAULT 0, 
    remarks TEXT default ""
    );

CREATE INDEX user3 ON temperatures (userid);
CREATE INDEX mdate3 ON temperatures (mdate);
