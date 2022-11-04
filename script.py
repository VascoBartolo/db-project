from mando import command, main
import psycopg2

@command
def race_script():
    conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="faculade",
    username="postgres",
    password="2003",
    options='-c search_path=public')


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
        
        restart = False
        menu_option = input("Choose an option by typing a number: ")
        
        if menu_option == "1":
            restart = False
            menu_1 = input("Please type the name of the runner you are searching for: ")
            
            result = cursor.execute("SELECT name FROM runner WHERE runner.name==(%s)", (menu_1))
            print(result)
            
            restart = True

        elif menu_option == "2":
            restart = False
            menu_1 = input("Please type the name of the race you are searching for: ")
            
            cursor.execute("SELECT name FROM race WHERE race.name==(%s)", (menu_1))
            restart = True
        else:
            return
        
    
if __name__ == '__main__':
    main()