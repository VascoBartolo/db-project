CREATE TABLE runner (
    id varchar(4000) PRIMARY KEY,                    -- runner id
    name VARCHAR(64) NOT NULL,                 -- name
	sex VARCHAR (1) CHECK (sex IN ('M', 'F')), -- gender
    nation VARCHAR (2),                        -- nationality
	birth_date DATE NOT NULL,                  -- birthday FORMAT: 'MM-DD-YYYY'
    UNIQUE (name, birth_date)                  -- person with the same name on the same birthday is not allowed
);


CREATE TABLE team (
    id varchar(4000) PRIMARY KEY,   -- team id
    name VARCHAR NOT NULL     -- team name 
);


CREATE TABLE age_class (
    id varchar(4000) PRIMARY KEY,   -- age_class id
    name VARCHAR NOT NULL     -- age_class  
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY,   -- event id
    name VARCHAR NOT NULL     -- event name 
);

CREATE TABLE race (
    id varchar(4000) PRIMARY KEY,                     -- race id
	id_event INTEGER NOT NULL REFERENCES event, -- event id
	year INTEGER NOT NULL,                       -- race year
    distance INTEGER NOT NULL                  -- distance (km)
);


CREATE TABLE participation (
    par_index varchar(4000),
	id_team varchar(4000) REFERENCES team,                    -- team if of the runner (if any)
	bib varchar(4000),                                        -- bib
	id_runner varchar(4000) REFERENCES runner,                -- This runner is enrolled
    id_race varchar(4000) REFERENCES race,                    -- in this race
    id_age_class varchar(4000) REFERENCES age_class, -- in this age_class
	place_in_class varchar(4000),                             -- place in their age_class
	net_time varchar(4000),                                      -- net time to finish the race
	official_time varchar(4000),                                 -- official time to finish the race
	place_overall varchar(4000),                              -- place over all age classes
    PRIMARY KEY (id_runner, id_race),                   -- runners cannot enrole twice in the same race
    UNIQUE (id_race, bib)                               -- bib is unique within every race
);


SELECT * FROM participation;

