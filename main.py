# LogiPy 3.0
from classes import *

running = True
modules = []
while running:
    u_in = raw_input("Enter command: ").strip()

    if u_in == "run":
        file_name = raw_input("Enter description file name (Must be in the program's directory): ").strip()
        if file_name.find(".txt") > -1:
            control = Controller(file_name)
            control.out_console()
        else:
            file_name +=  ".txt"
            control = Controller(file_name)
            control.out_console()

    elif u_in == "help":
        
        print "\nrun: Provides a truth table for a given description file."
        print "exit: Exits the program."
        print "out: Outputs truth table from a given description file to a .txt file.\n"
        

    elif u_in == "exit":
        print "Exiting program ..."
        running = False

    elif u_in == "out":        
        file_name = raw_input("Enter description file name (Must be in the program's directory): ").strip() + ".txt"
        out_file = raw_input("Enter output file name (Must be in the program's directory): ").strip() + ".txt"
        control = Controller(file_name)
        control.out_file(out_file)
        print "Output file written." 

    elif u_in == "load":
        print "Enter modules to load: "
        u_in = raw_input(">").strip()
        while (u_in != ""):   
            modules.append(Controller(u_in + ".txt"))
            print u_in + " module loaded"
            u_in = raw_input(">").strip()


    else:
        print "Not valid syntax (see 'help' for commands).\n"