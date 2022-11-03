CREATE TABLE runner (
    id INTEGER PRIMARY KEY,     -- runner id
    name VARCHAR NOT NULL,      -- name
    birth_date VARCHAR NOT NULL,     -- birthday
	sex VARCHAR,            -- gender
    nation VARCHAR  -- nationality
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY,   -- team id
    name VARCHAR NOT NULL    -- team name 
);

CREATE TABLE age_class (
    id INTEGER PRIMARY KEY,   -- age_class id
    name VARCHAR NOT NULL    -- age_class  
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY,   -- event id
    name VARCHAR NOT NULL    -- event name 
);

CREATE TABLE race (
    id INTEGER PRIMARY KEY,   -- race id
	id_event INTEGER NOT NULL REFERENCES event,
    distance VARCHAR NOT NULL,
	year VARCHAR NOT NULL
);

CREATE TABLE participation (
    id_runner INTEGER REFERENCES runner, -- This runner is enrolled
    id_race INTEGER REFERENCES race,  -- in this race
    id_age_class INTEGER REFERENCES age_class NOT NULL,
	bib VARCHAR,                     -- Grade after first exam
    id_team INTEGER REFERENCES team,                       -- Grade after second exam
	place_overall VARCHAR,
	place_in_class VARCHAR,
	official_time VARCHAR,
    net_time VARCHAR,
    PRIMARY KEY (id_runner, id_race),     -- runners cannot enrole twice in the same race
    UNIQUE (id_race, bib)
);
