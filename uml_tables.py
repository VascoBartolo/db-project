import psycopg2;
import csv;
import pandas as pd;

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="newdb",
    user="postgres",
    password="1234",
    options='-c search_path=public')


cur = conn.cursor()


#cur.execute('DROP TABLE IF EXISTS MyData')
cur.execute('DELETE FROM runner2')
"""create_script =  '''CREATE TABLE MyData
                    (
                    id int PRIMARY KEY,
                    age_class character varying(100),
                    place_in_class character varying(100),
                    bib character varying(50),
                    name character varying(100),
	                sex character varying(100),
	                nation character varying(100),
	                team character varying(100),
	                official_time character varying(100),
	                net_time character varying(100),
	                birth_date character varying(100),
	                event character varying(100),
	                event_year character varying(100),
	                distance character varying(100)
                    ); '''"""

insert_script = 'INSERT INTO runner2 (id_runner, name, birth_date, sex, nation) VALUES (%s, %s, %s, %s, %s)'
insert_values = pd.read_excel('/Users/farzam/Desktop/runner22.xlsx', index_col=0)
insert_values2 = list(insert_values.itertuples(index=True, name=None))
#print(insert_values2)
#print(insert_script)
#insert_values = insert_values.set_index()
#df = pd.DataFrame(data=insert_values)
#insert_values =  insert_values
for record in insert_values2:
    cur.execute(insert_script, record)

#cur.execute(insert_script)
#employee = cur.fetchone()
#print(employee)

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
