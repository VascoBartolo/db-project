-- FEUP | MECD
-- FCED - Running Races Database Project

-- GROUP 4
-- Authors:  Rojan Aslani, Farzam Salimi, Vasco Bartolomeu

-- SQL code for creating tables for running races database
------------------------------------------------------------------------
-- DETAILS REGARDING THE UML DESIGN:
-- Nation: 
--    added as a class to the diagram because it repeats often. 
--    However, in the project this class was not added and it can be redesigned for future improvements. 

-- Race and Event:
--    initially we intended to add distance to event, but there were examples where the event had different length in different years. 
--    Hence, it was added to race table.
------------------------------------------------------------------------

CREATE TABLE runner (
    id INTEGER PRIMARY KEY,                    -- runner id
    name VARCHAR(64) NOT NULL,                 -- name  
	sex VARCHAR (1) CHECK (sex IN ('M', 'F')), -- gender
    nation VARCHAR (2),                        -- nationality
    birth_date DATE NOT NULL,                  -- birthday FORMAT: 'MM-DD-YYYY'
    UNIQUE (name, birth_date)                  -- person with the same name on the same birthday is not allowed
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY,   -- team id
    name VARCHAR NOT NULL     -- team name 
);

CREATE TABLE age_class (
    id INTEGER PRIMARY KEY,   -- age_class id
    name VARCHAR NOT NULL     -- age_class  
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY,   -- event id
    name VARCHAR NOT NULL     -- event name 
);

CREATE TABLE race (
    id INTEGER PRIMARY KEY,                                       -- race id
	id_event INTEGER NOT NULL REFERENCES event ON DELETE CASCADE, -- event id
	year INTEGER NOT NULL,                                        -- race year
    distance INTEGER NOT NULL                                     -- distance (km)

);

CREATE TABLE participation (
    par_index INTEGER,
    id_team INTEGER REFERENCES team ON DELETE CASCADE,                    -- team if of the runner (if any)
	bib INTEGER,                                                          -- bib
    id_runner INTEGER REFERENCES runner ON DELETE CASCADE,                -- This runner is enrolled
    id_race INTEGER REFERENCES race ON DELETE CASCADE,                    -- in this race
    id_age_class INTEGER NOT NULL REFERENCES age_class ON DELETE CASCADE, -- in this age_class
	place_in_class INTEGER,                                               -- place in their age_class
    net_time TIME,                                                        -- net time to finish the race
	official_time TIME,                                                   -- official time to finish the race
    place_overall INTEGER,                                                -- place over all age classes
    PRIMARY KEY (id_runner, id_race),                                     -- runners cannot enrole twice in the same race
    UNIQUE (id_race, bib)                                                 -- bib is unique within every race
);