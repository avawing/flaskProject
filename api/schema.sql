DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY autoincrement,
    first_name STRING NOT NULL,
    last_name STRING NOT NULL,
    email STRING NOT NULL,
    HAS_LOAN BOOL,
    HAS_OTHER_LOAN BOOL
);