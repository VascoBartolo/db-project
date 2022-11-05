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



print("")
print("Menu:")
print("")
print("[1] Search runner")
print("")
print("[2] Search race")
print("")
print("[3] Ask Questions")
print("")


print("[1] Who ran the fastest 10km race ever?")


query = "SELECT runner.name, runner.birth_date, participation.official_time FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 ORDER BY official_time ASC LIMIT 1"
cur.execute(query)
res = cur.fetchall()
print(res)




#print(res)

conn.commit()

cur.close()
conn.close()




#id = int(input('Employee ID: '))

#cur = conn.cursor()
#cur.execute("SELECT * FROM MyData2")
#cur.fetchone()


#employee = cur.fetchone()
#print(employee)


#with open('employees.csv', 'w', newline='') as f:
  #reader = csv.reader(f)

#print(f)
