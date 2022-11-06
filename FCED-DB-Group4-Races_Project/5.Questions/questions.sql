-- FEUP | MECD
-- FCED - Running Races Database Project

-- GROUP 4
-- Authors:  Rojan Aslani, Farzam Salimi, Vasco Bartolomeu

-- SQL code for answering to questions
------------------------------------------------------------------------

-- a) Who run the fastest 10K race ever (name, birthdate, time)?
SELECT runner.name, runner.birth_date, participation.official_time 
FROM participation JOIN 
     runner ON id_runner = runner.id JOIN
     race ON id_race = race.id
WHERE distance = 10
ORDER BY official_time ASC
LIMIT 1

-- b) What 10K race had the fastest average time (event, event date)?
SELECT event.name AS event, t.year
FROM (
  SELECT AVG(official_time) AS average_time, race.id_event, race.year
  FROM participation JOIN 
     runner ON id_runner = runner.id JOIN
     race ON id_race = race.id
  WHERE distance = 10
  GROUP BY race.id
) AS t JOIN
event ON id_event = event.id

ORDER BY average_time ASC
LIMIT 1

-- SELECT event.name AS event, t.year FROM ( SELECT AVG(official_time) AS average_time, race.id_event, race.year FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 GROUP BY race.id ) AS t JOIN event ON id_event = event.id ORDER BY average_time ASC LIMIT 1

-- c) What teams had more than 3 participants in the 2016 maratona (team)?
SELECT team.name
FROM (
  SELECT COUNT(*) AS num, team.id
  FROM participation JOIN
     team ON id_team = team.id JOIN 
     race ON id_race = race.id JOIN
     event ON id_event = event.id
  WHERE event.name = 'maratona' AND race.year = 2016
  GROUP BY team.id
  HAVING COUNT(*) > 2
) AS t JOIN 
   team ON team.id= t.id

-- d) What are the 5 runners with more kilometers in total (name, birthdate, kms)?
SELECT runner.name, runner.birth_date, SUM(distance) AS kms
FROM runner JOIN
     participation ON id_runner = runner.id JOIN
     race ON id_race = race.id
GROUP BY runner.id
ORDER BY kms DESC
LIMIT 5

-- SELECT runner.name, runner.birth_date, SUM(distance) AS kms FROM runner JOIN participation ON id_runner = runner.id JOIN race ON id_race = race.id GROUP BY runner.id ORDER BY kms DESC LIMIT 5

-- e) What was the best time improvement in two consecutive maratona races (name, birthdate, improvement)?
-- UNFINISHED -- 

SELECT *
FROM (
    SELECT id_runner, p1.id_race, p2.id_race, p1.official_time, p2.official_time, year
    FROM participation AS p1 JOIN 
         race ON id_race = race.id JOIN
         event ON id_event = event.id JOIN
         participation AS p2 USING (id_runner)
    WHERE event.name = 'maratona'
) AS p1 
-- JOIN itself AS p2
-- WHERE p1.year - p2.year = 1
-- SELECT p1.official_time - p2.official_time AS dif
-- ORDER BY dif DESC
-- LIMIT 1

-- EXTRAS:

-- f) Top 5 races with the highest number of participants? (name, year, distance, numberofparticipations)
SELECT COUNT(*) AS num, distance, year, event.name
FROM participation JOIN
  race ON id_race = race.id JOIN 
  event ON id_event = event.id
GROUP BY race.id, event.id
ORDER BY num DESC
LIMIT 5

-- g) TOP 10 number of participants from each nationality (nation, number)
SELECT SUM (count), nation
FROM 
(
SELECT COUNT (*),  id_runner
FROM participation
GROUP BY id_runner
) AS repetitions JOIN 
runner ON id_runner = runner.id
GROUP BY nation
ORDER BY SUM (count) DESC
LIMIT 10 

-- scatter plot of age vs speed (official_time/distance)
SELECT distance, official_time, birth_date FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id

-- histogram of number of races per year
SELECT COUNT(*) as num, year FROM race GROUP BY year ORDER BY num  DESC
