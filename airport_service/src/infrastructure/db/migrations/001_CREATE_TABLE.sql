CREATE TABLE IF NOT EXISTS airports(
    airport_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    iata TEXT UNIQUE,
    icao TEXT UNIQUE,
    latitude REAL,
    longitude REAL,
    altitude_ft INTEGER,
    timezone TEXT
);