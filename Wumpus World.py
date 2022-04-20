
import sys
import os
import math
from Grid import Grid


def Rerun_Random_Grid():
    while True:
        print("---------------")
        response = input("Simulate again in another random world? (y/n)\n")
        if response.lower() == "y" or response.lower() == "yes":
            print("\n\t═══╣║║║║║ W U M P U S   W O R L D ║║║║╠═══\n\n\tSimulating on a random generated world...\n\n\tB = Strong wind | P = Pit | W = Wumpus | G = Gold | S = Stinks\n")
            return True
        elif response.lower() == "n" or response.lower() == "no":
            print("Exiting...")
            return False
        else:
            print("Invalid Input: Your response must be yes or no. (y/n)")
               

def Check_Create_Tournament(val):
    while True:
        if not val:
      
                print("\n\t═══╣║║║║║ W U M P U S   W O R L D ║║║║╠═══\n\n\tSimulating on a random generated world...\n\n\tB = Strong wind | P = Pit | W = Wumpus | G = Gold | S = Stinks\n")
                return False
 
def main ( ):
    args = sys.argv
    has_directory = False
    if not Check_Create_Tournament(has_directory):
        while True:
            world = Grid(True)
            score = world.run()
            if not Rerun_Random_Grid():
                return
    while True:
        sd = Check_Directories()


    if worldFile == "":
        if folder:
            print ( "[WARNING] No folder specified; running on a random world." )
        world = Grid ( debug, randomAI, manualAI )
        score = world.run()
        print ( "The agent scored: " + str(score) )
        return
   
    try:
        if verbose:
            print ( "Running world: " + worldFile )

        newLineDelim = "\n"
        if "\r\n".encode() in open(worldFile,"rb").read():
            newLineDelim = "\r\n"
        world = Grid ( debug, randomAI, manualAI, open ( worldFile, 'rt', newline=newLineDelim ) )
        score = world.run()

        if outputFile == "":
            print ( " " )
        else:
            try:
                outFile = open ( outputFile, 'w' )
                outFile.write ( "SCORE: " + str(score) )
                outFile.close ( )
            except:
                print ( "[ERROR] Failure to write to output file." )
    except Exception:
        print ( "[ERROR] Failure to open file." )

main()
