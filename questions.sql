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

-- e) What was the best time improvement in two consecutive maratona races (name,
birthdate, improvement)?
-- UNFINISHED:
SELECT *--MIN (p.official_time) - MIN(pp.official_time) AS time_dif
FROM participation AS p JOIN 
     participation AS pp ON pp.id_runner= p.id_runner JOIN 
     race ON p.id_race = race.id JOIN 
     event ON race.id_event = event.id
WHERE event.name = 'maratona'
--GROUP BY year

-- EXTRAS:

-- f) Top 5 races with the highest number of participants? (name, year, distance, numberofparticipations)
SELECT name, year, distance, number_of_participants
FROM (
   SELECT COUNT (*) AS number_of_participants, race.id_event
   FROM participation JOIN
        race ON id_race = race.id JOIN 
        event ON id_event = event.id
   GROUP BY race.id
) AS num_part_per_raceid JOIN 
   event ON num_part_per_raceid.id_event = event.id JOIN
   race ON race.id_event = num_part_per_raceid.id_event
ORDER BY number_of_participants DESC
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