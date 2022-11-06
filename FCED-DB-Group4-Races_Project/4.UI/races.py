"""
FEUP | MECD
FCED - Running Races Database Project

Running Races Interface

GROUP 4
Authors: Rojan Aslani, Vasco, Farzam Salimi
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk,THEMES

import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import datetime

conn = psycopg2.connect(
    database="fced_rojan_aslani",               # database
    user    ="fced_rojan_aslani",               # username
    password="MECD1234",                        # password
    host    ="dbm.fe.up.pt",   
    port    ="5433",          
    options ='-c search_path=public'            # the schema where tables are
)
cur = conn.cursor()


class MyGUI:

    def __init__(self):
        # CREATE ROOT AND SET THEME
        self.root = ThemedTk()#themebg=True)
        self.root.set_theme("breeze")
        self.root.title('Running Races of Portugal')
        font_large = ('',18)
        font_med = ('',16)
        self.root.geometry("800x600")
            
        # MENU BARS
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label = "Close", command = self.on_closing)
        self.menubar.add_cascade(menu = self.filemenu, label = "File")
        
        self.root.config(menu=self.menubar)

        

        # CREATE FRAMES
        self.main_frame = tk.Frame(self.root)
        self.runners_frame = tk.Frame(self.root)
        self.races_frame = tk.Frame(self.root)
        self.curiosity_frame = tk.Frame(self.root)
        self.questions_curiosity_frame = tk.Frame(self.root)
        self.plots_curiosity_frame = tk.Frame(self.root)

# MAIN FRAME -------------------------------------------------------------------------------------------------------------
        self.main_frame.label = ttk.Label(self.main_frame, text = "Running Races of Portugal Database", font = font_large)
        self.main_frame.label.pack(padx = 10, pady = 10)


    #runners 
        self.main_frame.runners_button = ttk.Button(self.main_frame, text = "Search Runner", command=self.change_to_runners)
        self.main_frame.runners_button.place(x=50, y=150, height = 100, width =300)
    #races
        self.main_frame.races_button = ttk.Button(self.main_frame, text = "Search Races", command=self.change_to_races)
        self.main_frame.races_button.place(x=450, y=150, height = 100, width =300)


    #curiosities
        self.main_frame.curiosity_button = ttk.Button(self.main_frame, text = "Curiosities", command=self.change_to_curiosity)
        self.main_frame.curiosity_button.place(x=175, y=300, height = 100, width =500)   


# RUNNER FRAME -------------------------------------------------------------------------------------------------------------
        self.runners_frame.label = ttk.Label(self.runners_frame, text = "Runners of Portugal", font = font_med)
        self.runners_frame.label.pack(padx = 10, pady = 10)        
        
        self.runners_frame.entry = tk.Entry(self.runners_frame)
        self.runners_frame.entry.pack(padx=10, pady=10)

        self.runners_frame.search_button = ttk.Button(self.runners_frame, text = "Search Runner", command=self.show_runner)
        self.runners_frame.search_button.pack(padx =10, pady=10)

        #treeview Frame
        self.runners_frame.tree_frame = tk.Frame(self.runners_frame)
        self.runners_frame.tree_frame.pack(pady=20)
        #scrollbar
        self.runners_frame.tree_scroll = ttk.Scrollbar(self.runners_frame.tree_frame)
        self.runners_frame.tree_scroll.pack(side = tk.RIGHT, fill = tk.Y)

        #treeview
        self.runners_frame.my_tree = ttk.Treeview(self.runners_frame,  yscrollcommand = self.runners_frame.tree_scroll.set)

        self.runners_frame.my_tree['columns'] = ("Name", "Birthdate", "Sex", "Nation" )
        self.runners_frame.my_tree.column("#0",width = 5, minwidth=5)
        self.runners_frame.my_tree.column("Name",  width = 150)
        self.runners_frame.my_tree.column("Birthdate",  width = 80)
        self.runners_frame.my_tree.column("Sex", width = 50)
        self.runners_frame.my_tree.column("Nation", width = 80)

        self.runners_frame.my_tree.heading("#0", text = "")
        self.runners_frame.my_tree.heading("Name", anchor='center' ,text = "Runner name")
        self.runners_frame.my_tree.heading("Birthdate", text = "Birth date")
        self.runners_frame.my_tree.heading("Sex",anchor='center' , text = "Sex")
        self.runners_frame.my_tree.heading("Nation",anchor='center' , text = "Nation")
        self.runners_frame.my_tree.pack()
        self.runners_frame.tree_scroll.config(command = self.runners_frame.my_tree.yview)

        self.runners_frame.back_button = ttk.Button(self.runners_frame, text = "Back", command=self.runnerframe_to_main)
        self.runners_frame.back_button.pack(padx =10, pady=10, side='right')

# RACES FRAME -------------------------------------------------------------------------------------------------------------
        self.races_frame.label = ttk.Label(self.races_frame, text = "Races of Portugal", font = font_med)
        self.races_frame.label.pack(padx = 10, pady = 10)        
        
        self.races_frame.entry = tk.Entry(self.races_frame)
        self.races_frame.entry.pack(padx=10, pady=10)

        self.races_frame.search_button = ttk.Button(self.races_frame, text = "Search Races", command=self.show_race)
        self.races_frame.search_button.pack(padx =10, pady=10)

        # Treeview
        self.races_frame.my_tree = ttk.Treeview(self.races_frame)

        self.races_frame.my_tree['columns'] = ("Name", "Year", "Distance" )
        self.races_frame.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.races_frame.my_tree.column("Name", anchor='center' , width = 150)
        self.races_frame.my_tree.column("Year", anchor='center' , width = 80)
        self.races_frame.my_tree.column("Distance", anchor='center' , width = 100)

        self.races_frame.my_tree.heading("#0", text = "")
        self.races_frame.my_tree.heading("Name", anchor='center' ,text = "Race name")
        self.races_frame.my_tree.heading("Year",anchor='center' , text = "Year")
        self.races_frame.my_tree.heading("Distance",anchor='center' , text = "Distance")
        self.races_frame.my_tree.pack(pady=20)

        self.races_frame.back_button = ttk.Button(self.races_frame, text = "Back", command=self.raceframe_to_main)
        self.races_frame.back_button.pack(padx =10, pady=10, side='right')


# CURIOSITY FRAME -------------------------------------------------------------------------------------------------------------
        self.curiosity_frame.label = ttk.Label(self.curiosity_frame, text = "Curiousities about running races of Portugal", font = font_med) #, font = ('Arial', 18)
        self.curiosity_frame.label.pack(padx = 10, pady = 10)        

        self.curiosity_frame.questions_button = ttk.Button(self.curiosity_frame, text = "Questions and Answers",  command=self.change_to_curiosity_questions)
        self.curiosity_frame.questions_button.place(x=50, y=150, height = 100, width =300)

        self.curiosity_frame.plots_button = ttk.Button(self.curiosity_frame, text = "Visualizations", command=self.change_to_curiosity_plots)
        self.curiosity_frame.plots_button.place(x=450, y=150, height = 100, width =300)

        self.curiosity_frame.back_button = ttk.Button(self.curiosity_frame, text = "Back", command=self.curiosity_to_main)
        self.curiosity_frame.back_button.pack(padx =10, pady=10, side='right')

# QUESTIONS CURIOSITY FRAME -------------------------------------------------------------------------------------------------------------
        self.questions_curiosity_frame.label = ttk.Label(self.questions_curiosity_frame, text = "Questions and Answers", font = font_med) #, font = ('Arial', 18)
        self.questions_curiosity_frame.label.pack(padx = 10, pady = 10)        
        #Q1
        self.questions_curiosity_frame.q1_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "Who ran the fastest 10km race ever?"
                                                    , command=self.q1)
        self.questions_curiosity_frame.q1_button.pack(padx =10, pady=10)
        
        #Q2
        self.questions_curiosity_frame.q2_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "What 10km race had the fastest average time?"
                                                    , command=self.q2)
        self.questions_curiosity_frame.q2_button.pack(padx =10, pady=10)

        #Q3
        self.questions_curiosity_frame.q3_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "What teams had more than 3 participants in the 2016 maratona?"
                                                    , command=self.q3)
        self.questions_curiosity_frame.q3_button.pack(padx =10, pady=10)

        #Q4
        self.questions_curiosity_frame.q4_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "What are the 5 runners with more kilometers in total?"
                                                    , command=self.q4)
        self.questions_curiosity_frame.q4_button.pack(padx =10, pady=10)

        #Q6
        self.questions_curiosity_frame.q6_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "Top 5 races with the highest number of participants?"
                                                    , command=self.q6)
        self.questions_curiosity_frame.q6_button.pack(padx =10, pady=10)        
        
        #Q7
        self.questions_curiosity_frame.q7_button = ttk.Button(self.questions_curiosity_frame, 
                                                    text = "Top 5 nationalities with highest number of participants?"
                                                    , command=self.q7)
        self.questions_curiosity_frame.q7_button.pack(padx =10, pady=10) 

        self.questions_curiosity_frame.back_button = ttk.Button(self.questions_curiosity_frame, text = "Back", command=self.questions_to_curiosity_frame)
        self.questions_curiosity_frame.back_button.pack(padx =10, pady=10, side='right')

# PLOTS CURIOSITY FRAME -------------------------------------------------------------------------------------------------------------

        self.plots_curiosity_frame.label = ttk.Label(self.plots_curiosity_frame, text = "Visualizations", font = font_med) #, font = ('Arial', 18)
        self.plots_curiosity_frame.label.pack(padx = 10, pady = 10)        

        #Create a button to show the plot
        self.plots_curiosity_frame.plot1_button = ttk.Button(self.plots_curiosity_frame, text = "Plot speed of running vs. age",
                                                     command=self.plot_runner_speed)
        self.plots_curiosity_frame.plot1_button.place(x=200, y=100, height = 80, width =400)

        self.plots_curiosity_frame.plot2_button = ttk.Button(self.plots_curiosity_frame, text = "Plot number of races per year", 
                                                    command=self.plot_races_year)
        self.plots_curiosity_frame.plot2_button.place(x=200, y=200, height = 80, width =400)

        self.plots_curiosity_frame.plot3_button = ttk.Button(self.plots_curiosity_frame, text = "Plot number of participations per year",
                                                     command=self.plot_participation_year)
        self.plots_curiosity_frame.plot3_button.place(x=200, y=300, height = 80, width =400)


        self.plots_curiosity_frame.back_button = ttk.Button(self.plots_curiosity_frame, text = "Back", command=self.plots_to_curiosity_frame)
        self.plots_curiosity_frame.back_button.pack(padx =10, pady=10, side='right')


# START AND CLOES FRAME AND WINDOW -------------------------------------------------------------------------------------
        self.main_frame.pack(fill = 'both', expand = 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) #for closing window
        self.root.mainloop()

# FUNCTIONS -------------------------------------------------------------------------------------------------------------

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message = "Do you really want to quit?"):
            self.root.destroy()

    def change_to_runners(self):
        self.runners_frame.pack(fill = 'both', expand = 1)
        self.main_frame.forget()

    def change_to_races(self):
        self.races_frame.pack(fill = 'both', expand = 1)
        self.main_frame.forget()   

    def change_to_curiosity(self):
        self.curiosity_frame.pack(fill = 'both', expand = 1)
        self.main_frame.forget() 

    def change_to_curiosity_plots (self):
        self.plots_curiosity_frame.pack(fill = 'both', expand = 1)
        self.curiosity_frame.forget()
        
    def change_to_curiosity_questions (self):
        self.questions_curiosity_frame.pack(fill = 'both', expand = 1)
        self.curiosity_frame.forget()

    def runnerframe_to_main(self):
        self.main_frame.pack(fill = 'both', expand = 1)
        self.runners_frame.forget()
    
    def raceframe_to_main(self):
        self.main_frame.pack(fill = 'both', expand = 1)
        self.races_frame.forget() 

    def curiosity_to_main(self):
        self.main_frame.pack(fill = 'both', expand = 1)
        self.curiosity_frame.forget() 

    def plots_to_curiosity_frame(self):
        self.curiosity_frame.pack(fill = 'both', expand = 1)
        self.plots_curiosity_frame.forget() 

    def questions_to_curiosity_frame(self):
        self.curiosity_frame.pack(fill = 'both', expand = 1)
        self.questions_curiosity_frame.forget() 
        
    def show_runner (self):
        count = 1
        # remove existing data from tree
        for item in self.runners_frame.my_tree.get_children():
            self.runners_frame.my_tree.delete(item)
        
        # execute query
        query = ''
        name = self.runners_frame.entry.get()
        str1 = "SELECT name, birth_date, sex, nation FROM runner WHERE runner.name ~* '" #case insensitive
        str2 = "'"
        query = str1 + name + str2
        cur.execute(query)
        res = cur.fetchall()
        
        # show result
        for i in range (len(res)):
            self.runners_frame.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1

    def show_race (self):
        count = 1
        # remove existing data from tree
        for item in self.races_frame.my_tree.get_children():
            self.races_frame.my_tree.delete(item)
        
        # execute query
        query = ''
        name = self.races_frame.entry.get()
        str1 = "SELECT event.name,  race.year, race.distance FROM race JOIN event ON event.id = id_event WHERE event.name ~* '" #case insensitive
        str2 = "'"
        query = str1 + name + str2
        cur.execute(query)
        res = cur.fetchall()
        
        # show result
        for i in range (len(res)):
            self.races_frame.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1
    
    def q1(self):
        count = 1

        # execute query
        query = "SELECT runner.name, runner.birth_date, participation.official_time FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 ORDER BY official_time ASC LIMIT 1"
        cur.execute(query)
        res = cur.fetchall()
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q1')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("Name", "bday", "time" )
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("Name", anchor='center' , width = 300)
        self.top.my_tree.column("bday", anchor='center' , width = 100)
        self.top.my_tree.column("time", anchor='center' , width = 200)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("Name", anchor='center' ,text = "Runner name")
        self.top.my_tree.heading("bday",anchor='center' , text = "Birth day")
        self.top.my_tree.heading("time",anchor='center' , text = "Official Time")
        self.top.my_tree.pack(pady=20)

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1
   
        
    def q2(self):
        count = 1

        # execute query
        query = "SELECT event.name AS event, t.year FROM (SELECT AVG(official_time) AS average_time, race.id_event, race.year FROM participation JOIN  runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 GROUP BY race.id) AS t JOIN event ON id_event = event.id ORDER BY average_time ASC LIMIT 1"
        cur.execute(query)
        res = cur.fetchall()
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q2')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("Name", "year")
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("Name", anchor='center' , width = 250)
        self.top.my_tree.column("year", anchor='center' , width = 100)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("Name", anchor='center' ,text = "Event")
        self.top.my_tree.heading("year",anchor='center' , text = "Year")
        self.top.my_tree.pack(fill='y')

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1

    def q3(self):
        count = 1

        # execute query
        query = "SELECT team.name FROM (SELECT COUNT(*) AS num, team.id FROM participation JOIN team ON id_team = team.id JOIN race ON id_race = race.id JOIN event ON id_event = event.id WHERE event.name = 'maratona' AND race.year = 2016 GROUP BY team.id HAVING COUNT(*) > 2) AS t JOIN team ON team.id= t.id"
        cur.execute(query)
        res = cur.fetchall()
        
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q3')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("Name")
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("Name", anchor='center' , width = 500)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("Name", anchor='center' ,text = "Teams")
        self.top.my_tree.pack(fill='y')

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1

    def q4(self):
        count = 1

        # execute query
        query = "SELECT runner.name, runner.birth_date, SUM(distance) AS kms FROM runner JOIN participation ON id_runner = runner.id JOIN race ON id_race = race.id GROUP BY runner.id ORDER BY kms DESC LIMIT 5"
        cur.execute(query)
        res = cur.fetchall()
        
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q4')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("Name", "bday", "dis" )
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("Name", anchor='center' , width = 250)
        self.top.my_tree.column("bday", anchor='center' , width = 150)
        self.top.my_tree.column("dis", anchor='center' , width = 200)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("Name", anchor='center' ,text = "Runner name")
        self.top.my_tree.heading("bday",anchor='center' , text = "Birth day")
        self.top.my_tree.heading("dis",anchor='center' , text = "Distance (km)")
        self.top.my_tree.pack(pady=20)

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1


    def q6(self):
        count = 1

        # execute query
        query = """SELECT event.name, year,  distance, COUNT(*) AS num 
                FROM participation JOIN
                race ON id_race = race.id JOIN 
                event ON id_event = event.id
                GROUP BY race.id, event.id
                ORDER BY num DESC
                LIMIT 5"""         
        cur.execute(query)
        res = cur.fetchall()
        
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q6')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("Name", "year", "dis", "num" )
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("Name", anchor='center' , width = 200)
        self.top.my_tree.column("year", anchor='center' , width = 100)
        self.top.my_tree.column("dis", anchor='center' , width = 150)
        self.top.my_tree.column("num", anchor='center' , width = 150)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("Name", anchor='center' ,text = "Event")
        self.top.my_tree.heading("year",anchor='center' , text = "Year")
        self.top.my_tree.heading("dis", anchor='center' , text = "Distance")
        self.top.my_tree.heading("num",anchor='center' , text = "Number of participants")
        self.top.my_tree.pack(pady=20)

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1


    def q7(self):
        count = 1
        # execute query
        query = """SELECT SUM (count), nation
                FROM 
                (
                SELECT COUNT (*),  id_runner
                FROM participation
                GROUP BY id_runner
                ) AS repetitions JOIN 
                runner ON id_runner = runner.id
                GROUP BY nation
                ORDER BY SUM (count) DESC
                LIMIT 5"""         
        cur.execute(query)
        res = cur.fetchall()
        
        
        #create new window
        self.top = tk.Toplevel()
        self.top.title('Q7')
   
        self.top.my_tree = ttk.Treeview(self.top)

        self.top.my_tree['columns'] = ("num", "Nation" )
        self.top.my_tree.column("#0", anchor='center' ,width = 5, minwidth=5)
        self.top.my_tree.column("num", anchor='center' , width = 300)
        self.top.my_tree.column("Nation", anchor='center' , width = 300)

        self.top.my_tree.heading("#0", text = "")
        self.top.my_tree.heading("num",anchor='center' , text = "Nationality")
        self.top.my_tree.heading("Nation",anchor='center' , text = "Number of participants")

        self.top.my_tree.pack(pady=20)

        # show result
        for i in range (len(res)):
            self.top.my_tree.insert(parent ='', index = 'end', iid = count, text = "", values = res[i] )
            count +=1


    def plot_runner_speed(self):
        # Make plot of runner age vs average speed/km.
        # BDAY, TIME, DISTANCE
        query_dis_time_bday = ("SELECT distance, official_time, birth_date FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id")
        cur.execute(query_dis_time_bday)
        tables = cur.fetchall() #this is a tupple

        #initiate variables

        official_time = []
        age = []

        for i in range (len(tables)):
            distance = tables[i][0]
            tt = tables[i][1]
            time = tt.minute + tt.hour *60
            timeperkm = time / distance
            official_time.append(round(timeperkm, 2))
            date = tables[i][2]
            now = datetime.datetime.today().year
            agee = now - date.year 
            age.append(agee)

        # GRAPHS 
        x = np.arange(len(official_time))
        plt.scatter(official_time, age, s=2, alpha = 0.3, c = x, cmap='viridis')
        plt.xlabel('Speed (min/km)')
        plt.ylabel('age')
        plt.title('Runner Speed (min/km) by age')
        plt.show()

    def plot_races_year(self): 
        #Histogram of races per year
        query_races_per_year = ("SELECT year FROM race")
        cur.execute(query_races_per_year)
        tables2 = cur.fetchall() #this is a tupple

        res = list(zip(*tables2))
        
        years = res[0]

        plt.hist(years, bins = 7, edgecolor='white', color='green', alpha = 0.5)
        plt.ylabel('Frequency')
        plt.title('Number of races per year')

        plt.show()

    def plot_participation_year(self):

        # line plot of number of participations per year
        query_races_per_year = ("SELECT year FROM participation JOIN race ON id_race = race.id")
        cur.execute(query_races_per_year)
        tables2 = cur.fetchall() #this is a tupple

        res = list(zip(*tables2))
        
        years = res[0]

        plt.hist(years, bins = 7, edgecolor='white', alpha = 0.5)
        plt.ylabel('Frequency')
        plt.title('Number of participations per year')
        plt.show()

MyGUI()
conn.close()
