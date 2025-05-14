ALTER TABLE users 
ADD COLUMN body_height INTEGER DEFAULT 0;

ALTER TABLE users
ADD COLUMN last_login TEXT DEFAULT "2025-05-14 01:10";

ALTER TABLE users
ADD COLUMN retries INTEGER DEFAULT 0;

CREATE TABLE weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid INTEGER NOT NULL,
    mdate TEXT NOT NULL DEFAULT current_timestamp,
    body_weight INTEGER DEFAULT 0, 
    remarks TEXT default ""
    );

CREATE INDEX user2 ON weights (userid);
CREATE INDEX mdate2 ON weights (mdate);
