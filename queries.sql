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
-- unfinished
SELECT COUNT(*) AS num, team.name
FROM participation JOIN
     team ON id_team = team.id
GROUP BY team.id
-- HAVING num > 3

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