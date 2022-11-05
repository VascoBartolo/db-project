import psycopg2;
import csv;
import pandas as pd;
import numpy as np;
import time

start = time.time()

# Connect to Database
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="newdb",
    user="postgres",
    password="1234",
    options='-c search_path=public')


cur = conn.cursor()

# DELETE all rows from database tables
#cur.execute('DROP TABLE IF EXISTS MyData')
cur.execute('TRUNCATE runner CASCADE')
cur.execute('TRUNCATE team CASCADE')
cur.execute('TRUNCATE age_class CASCADE')
cur.execute('TRUNCATE event CASCADE')
cur.execute('TRUNCATE race CASCADE')
cur.execute('TRUNCATE participation CASCADE')

# INSERT new rows to tables
insert_script = 'INSERT INTO runner (id, name, sex, nation, birth_date) VALUES (%s, %s, %s, %s, %s)'
insert_script2 = 'INSERT INTO team (id, name) VALUES (%s, %s)'
insert_script3 = 'INSERT INTO age_class (id, name) VALUES (%s, %s)'
insert_script4 = 'INSERT INTO event (id, name) VALUES (%s, %s)'
insert_script5 = 'INSERT INTO race (id, id_event, year, distance) VALUES (%s, %s, %s, %s)'
insert_script6 = 'INSERT INTO participation (par_index, id_team, bib, id_runner, id_race, id_age_class, place_in_class, net_time, official_time, place_overall) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'


# Reading CSV file
print ('Reading CSV file...')
df0 = pd.read_csv('/Users/farzam/Desktop/DB_Project/all_races.csv', index_col = False)

# removing duplicates
n = 146930
df2 = df0.tail(df0.shape[0] -n)

# changing type of variables
df = df2.astype({"place_in_class":"int", "bib":"int", "event_year":"int", "distance":"int"})
df3 = df.drop_duplicates(keep='first')

# Remove / Replace missing values
df3['team'] = df3['team'].fillna('Individual')

# Changing time format variable
df3['birth_date'] = pd.to_datetime(df3['birth_date'])

df3 = df3[df3['age_class'].notna()]
df3 = df3[df3['net_time'].notna()]


print ('Creating sub-tables...')
#unique runners
unique_runners = df3.drop_duplicates(subset=['name', 'birth_date'], keep='first')
unique_runners.reset_index()

#runners table
runners_table = unique_runners.filter(['name', 'sex', 'nation', 'birth_date'])
runners_table.insert(0, "runner_index", range(1, len(runners_table) + 1), True)
runners_table = runners_table.reset_index()
runners_table2 = runners_table.drop(runners_table.columns[0],axis = 1)
#unners_table2.set_index('runner_index', inplace=True)


#events
unique_events = df3.drop_duplicates(subset=['event'], keep='first')
unique_events = unique_events.filter(['event'])
unique_events.insert(0, "event_index", range(1, len(unique_events) + 1), True)
unique_events = unique_events.reset_index()
unique_events2 = unique_events.drop(unique_events.columns[0],axis = 1)
#unique_events2.set_index('event_index', inplace=True)


#races
unique_races = df3.drop_duplicates(subset=['event','event_year','distance'], keep='first')
unique_races = unique_races.filter(['event','event_year', 'distance'])
unique_races.insert(0, "race_index", range(1, len(unique_races) + 1), True)

unique_races2 = unique_races.to_numpy()
unique_events_x = unique_events2.to_numpy()
event_name = unique_races2[:,1]
event_name
for i in range(len(unique_events_x[:,0])):
    event_name = np.where(event_name == unique_events_x[i,1], unique_events_x[i,0], event_name)

unique_races2[:,1] = event_name
unique_races2 = pd.DataFrame(unique_races2, columns = ['race_index', 'event_index', 'race_year', 'distance'])

#unique_races2 = unique_races2.drop(unique_races2.columns[0],axis = 1)
#unique_races2.set_index('race_index', inplace=True)

#teams
table_team = df3.drop_duplicates(subset=['team'], keep='first')
table_team = table_team.filter(['team'])
table_team.insert(0, "team_index", range(1, len(table_team) + 1), True)
table_team = table_team.reset_index()
table_team2 = table_team.drop(table_team.columns[0],axis = 1)
#table_team2.set_index('team_index', inplace=True)


#age class
unique_age_class = df3.drop_duplicates(subset=['age_class'], keep='first')
unique_age_class = unique_age_class.filter(['age_class'])
unique_age_class.insert(0, "age_class_index", range(1, len(unique_age_class) + 1), True)
unique_age_class = unique_age_class.reset_index()
unique_age_class2 = unique_age_class.drop(unique_age_class.columns[0],axis = 1)
#unique_age_class2.set_index('age_class_index', inplace=True)
#print(unique_age_class2)
#reservation2

# Creating the tables to insert to DB
print ('Creating tables...')

reservation = df3.drop_duplicates(subset=['team', 'bib', 'name', 'event','age_class','birth_date','event_year'], keep='first')
reservation = reservation.filter(['team', 'bib', 'name', 'event','age_class','birth_date','event_year','place_in_class','net_time', 'official_time','place'])

reservation = reservation.reset_index()
reservation2 = reservation.drop(reservation.columns[0],axis = 1)

reservations3 = reservation2.copy()
reservations3
#removing columns because runner name and birthdate, and event name and year are replaced with the foreign keys
del reservations3['name']
del reservations3['event']
#del reservations3['age_class']
del reservations3['birth_date']
del reservations3['event_year']

#We are converting the dataframe to numpy to iterate faster through the rows to replace the foreign keys to the participation table

# Here we replace the team name with the respective foreign keys
#x = reservation2[0:100000].to_numpy()

x = reservation2.to_numpy()
teams = table_team2.to_numpy()
team = x[:,0]
events = unique_events2.to_numpy()
event = x[:,3]
for i in range(len(teams[:,0])):
    team = np.where(team == teams[i,1], teams[i,0], team)

x[:,0] = team

# Here we replace the event name with the respective foreign keys
events = unique_events2.to_numpy()
event = x[:,3]
for i in range(len(events[:,0])):
    event = np.where(event == events[i,1], events[i,0], event)

x[:,3] = event

# Here we replace the event name with the race index foreign key
races = unique_races2.to_numpy()
matrix = x[:,[3,6]]
race = [None] * (len(x[:,0]))

for i in range(len(races[:,0])):
    race = np.where((matrix[:,0] == races[i,1]) & (matrix[:,1] == races[i,2]), races[i,0], race)

x[:,3] = race

# Here we replace the age class name with the respective foreign keys
age_classes = unique_age_class2.to_numpy()
age_class = x[:,4]
for i in range(len(age_classes[:,0])):
    age_class = np.where(age_class == age_classes[i,1], age_classes[i,0], age_class)

x[:,4] = age_class

# Here we replace the runner name and runner birth date with the respective foreign keys
runners = runners_table2.to_numpy()
matrix = x[:,[2,5]]
runner = [None] * (len(x[:,0]))

for i in range(len(runners[:,0])):
    runner = np.where((matrix[:,0] == runners[i,1]) & (matrix[:,1] == runners[i,4]), runners[i,0], runner)

x[:,2] = runner

# Converting the numpy array list to DataFrame
x = pd.DataFrame(x, columns = ['team_index', 'bib', 'runner_index', 'race_index', 'age_class', 'birth_date', 'event_year', 'place_in_class', 'net_time', 'offical_time', 'place'])
x2 = x.drop(x.columns[[5, 6]],axis = 1)
x3 = x2.copy()
x3 = x3.drop_duplicates(subset=['runner_index','race_index'], keep='first')

#Removing the default index of the dataframe
unique_age_class2.set_index('age_class_index', inplace=True)
table_team2.set_index('team_index', inplace=True)
unique_races2.set_index('race_index', inplace=True)
unique_events2.set_index('event_index', inplace=True)
runners_table2.set_index('runner_index', inplace=True)

x3.insert(0, "par_index", range(1, len(x3) + 1), True)
x3.set_index('par_index', inplace=True)




#insert_values = pd.read_csv('/Users/farzam/Desktop/DB_Project/all_races.csv', index_col=0)
#insert_values2 = insert_values.head(555)
runners_table2 = list(runners_table2.itertuples(index=True, name=None))
table_team2 = list(table_team2.itertuples(index=True, name=None))
unique_age_class2 = list(unique_age_class2.itertuples(index=True, name=None))
unique_events2 = list(unique_events2.itertuples(index=True, name=None))
unique_races2 = list(unique_races2.itertuples(index=True, name=None))
x3 = list(x3.itertuples(index=True, name=None))
#print(x3)



#print(insert_values2)
#print(insert_script)
#insert_values = insert_values.set_index()
#df = pd.DataFrame(data=insert_values)
#insert_values =  insert_values


for record in runners_table2:
    cur.execute(insert_script, record)

for record in table_team2:
    cur.execute(insert_script2, record)

for record in unique_age_class2:
    cur.execute(insert_script3, record)

for record in unique_events2:
    cur.execute(insert_script4, record)

for record in unique_races2:
    cur.execute(insert_script5, record)

end = time.time()
print('Execution time (min):',(end-start)/60)

for record in x3:
    cur.execute(insert_script6, record)

#menu_1 = input("Please type the name of the runners you are searching for: ")

#print(menu_1)
#print(type(menu_1))
#run_scrp =
#print("SELECT name FROM runners WHERE runners.name==(\"",menu_1,"\")",sep="")

#cur.execute('SELECT name FROM runners WHERE runners.name==(\'',menu_1,''\")",sep="")

#cur.execute("""
#    SELECT name FROM runners WHERE runners.name==(%s);
#    """,
#    (menu_1))

###str1 = "SELECT name, sex FROM runners WHERE runners.name='"
###str2 = "'"
###query = str1 + menu_1 + str2


#query = "SELECT * FROM runners"
#x = cur.execute('SELECT * FROM runners')
#print(x)
#cur.execute(insert_script)
#employee = cur.fetchone()
#print(employee)
#query = "SELECT name FROM runners WHERE runners.name= \'Paulo Gomes\'"

#query = " SELECT runner.name, runner.birth_date, participation.official_time  FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 ORDER BY official_time ASC LIMIT 1"

#cur.execute(query)
#res = cur.fetchall()
#print(res)

conn.commit()

cur.close()
conn.close()

end = time.time()
print('Execution time (min):',(end-start)/60)


#id = int(input('Employee ID: '))

#cur = conn.cursor()
#cur.execute("SELECT * FROM MyData2")
#cur.fetchone()


#employee = cur.fetchone()
#print(employee)


#with open('employees.csv', 'w', newline='') as f:
  #reader = csv.reader(f)

#print(f)
print('EOF.')
