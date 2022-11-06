FEUP | MECD
FCED - Running Races Database Project

load_races.py

GROUP 4
Authors: Farzam Salimi, Vasco Bartolomeu, Rojan Aslani
All group members contributed the same amount at all parts of the project.
_____________

Before compiling the .py file, please change the following parameters:
- line 23 to 29: details about your database server

The compilation of the file can take upto 20 minutes (when done on local servers). 
	- We recommend to upload the data on a local server, cloud servers can increase the compilation time upto 6 fold.
_____________

This file does the following tasks:

a) Removes all data from the database (using the DELETE command)
   - TRUNCATE could have been an equally good command

b) Reads the all_races.csv file and prepares the data by:
   - remove duplicates
   - change data types to the ones defined in the UML diagram
   - remove NA values (when necessary)

c) Populates the database with new data (using the INSERT command)

