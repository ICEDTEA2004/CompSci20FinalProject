# Minh Au       #
# Comp Sci 20   #
# 20/06/2020    #
#################
from Final_Project import Functionalities as Func


#################################################
# This project is based on the competition’s    #
# Coding category’s instructions                #
# see more in the file called                   #
# 2020 Online Skills Sask Coding exam 2020.pdf  #
#################################################

def main():
    '''This is the main function that runs the program'''
    # 4 main states: Running, Exiting, Inputting, Cancelling
    global state
    answer = Func.GetInput("Please enter your command ", isCommand=True)  # Ask for command
    if state == "Running" and len(Func.allParticipants) > 0:
        if Func.allParticipants[-1].score is None:  # Inputting information is canceled
            if Func.allParticipants[-1].Id is not None:
                Func.allId.pop(Func.allParticipants[-1].Id)
            del Func.allParticipants[-1]  # delete the entry
    print()
    if answer is not None and answer == "Exiting":  # Exit the program
        state = answer


state = None # the state of the program
if __name__ == '__main__': # The program will only run when this file is executed
    state = "Running"
    while state != "Exiting":
        main()
