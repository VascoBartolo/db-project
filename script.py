from mando import command, main
import psycopg2
#go back to menu 2 after answering questions

@command
def race_script():
    conn = psycopg2.connect(
    database="fced_farzam_salimi",             # database
    user    ="fced_farzam_salimi",                 # username
    password="fced_farzam_salimi",             # password
    host    ="dbm.fe.up.pt",   
    port    ="5433",          
    options ='-c search_path=public')  # use the schema you want to connect to)


    cur = conn.cursor()
    restart = True

    while restart:
        print("")
        print("Menu:")
        print("")
        print("[1] Search runner")
        print("")
        print("[2] Search race")
        print("")
        print("[3] Ask Questions")
        print("")


        restart = False
        menu_option = input("Choose an option by typing a number: ")

        if menu_option == "1":
            restart = False
            menu_1 = input("Please type the name of the runners you are searching for: ")
            str1 = "SELECT * FROM runner WHERE runner.name='"
            str2 = "'"
            query = str1 + menu_1 + str2
            cur.execute(query)
            res = cur.fetchall()
            print(res)

            restart = True

        elif menu_option == "2":
            restart = False
            menu_1 = input("Please type the name of the race you are searching for: ")
            str1 = "SELECT race.id, event.name,  race.year, race.distance FROM race JOIN event ON event.id = id_event WHERE event.name='"
            str2 = "'"
            query = str1 + menu_1 + str2
            cur.execute(query)
            res = cur.fetchall()
            print(res)

            restart = True
        elif menu_option == "3":
            restart = False
            print("")
            print("Select one of the following options:")
            print("")
            print("[1] Who ran the fastest 10km race ever?")
            print("")
            print("[2] What 10km race had the fastest average time?")
            print("")
            print("[3] What teams had more than 3 participants in the 2016 maratona?")
            print("")
            print("[4] What are the 5 runners with more kilometers in total?")
            print("")
            print("[5] What was the best time improvement in two consecutive maratona races?")
            print("")
            print("[6] What was the best time improvement in two consecutive maratona races?")
            print("")
            print("[7] What was the best time improvement in two consecutive maratona races?")
            print("")
            print("[0] Press 0 to go to the last menu.")
            print("")
            menu_q = input("Please type number of the question you want to ask: ")
            restart_menu_2 = True

            if menu_q == "1":
                restart = False
                query = "SELECT runner.name, runner.birth_date, participation.official_time FROM participation JOIN runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 ORDER BY official_time ASC LIMIT 1"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "2":
                restart = False
                query = "SELECT event.name AS event, t.year FROM (SELECT AVG(official_time) AS average_time, race.id_event, race.year FROM participation JOIN  runner ON id_runner = runner.id JOIN race ON id_race = race.id WHERE distance = 10 GROUP BY race.id) AS t JOIN event ON id_event = event.id ORDER BY average_time ASC LIMIT 1"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "3":
                restart = False
                query = "SELECT team.name FROM (SELECT COUNT(*) AS num, team.id FROM participation JOIN team ON id_team = team.id JOIN race ON id_race = race.id JOIN event ON id_event = event.id WHERE event.name = 'maratona' AND race.year = 2016 GROUP BY team.id HAVING COUNT(*) > 2) AS t JOIN team ON team.id= t.id"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "4":
                restart = False
                query = "SELECT runner.name, runner.birth_date, SUM(distance) AS kms FROM runner JOIN participation ON id_runner = runner.id JOIN race ON id_race = race.id GROUP BY runner.id ORDER BY kms DESC LIMIT 5"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "5":
                restart = False
                query = "SELECT name, year, distance, number_of_participants FROM (SELECT COUNT (*) AS number_of_participants, race.id_event FROM participation JOIN race ON id_race = race.id JOIN event ON id_event = event.id GROUP BY race.id) AS num_part_per_raceid JOIN  event ON num_part_per_raceid.id_event = event.id JOIN race ON race.id_event = num_part_per_raceid.id_event ORDER BY number_of_participants DESC LIMIT 5"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "6":
                restart = False
                query = "SELECT name, year, distance, number_of_participants FROM (SELECT COUNT (*) AS number_of_participants, race.id_event FROM participation JOIN race ON id_race = race.id JOIN event ON id_event = event.id GROUP BY race.id) AS num_part_per_raceid JOIN  event ON num_part_per_raceid.id_event = event.id JOIN race ON race.id_event = num_part_per_raceid.id_event ORDER BY number_of_participants DESC LIMIT 5"
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "7":
                restart = False
                query = "SELECT SUM (count), nation FROM (SELECT COUNT (*),  id_runner FROM participation GROUP BY id_runner) AS repetitions JOIN runner ON id_runner = runner.id GROUP BY nation ORDER BY SUM (count) DESC LIMIT 10 "
                cur.execute(query)
                res = cur.fetchall()
                print(res)
            elif menu_q == "0":
                restart = True
            else:
                print("Invalid input")
                restart = True
        else:
            print("Invalid input")
            return


if __name__ == '__main__':
    main()

