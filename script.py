from mando import command, main

@command
def race_script():
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
            if menu_1 == "Vasco":
                print("He didnt run he is fat")
                print("")
                restart = True

        elif menu_option == "2":
            restart = False
            menu_1 = input("Please type the name of the race you are searching for: ")
            print("")
            menu_0 = "0"
        else:
            return
    
    
if __name__ == '__main__':
    main()