from Python.Final_Project.Class_Participant import *
from Python.Final_Project import Main_Program as Main


def GetInput(message, isCommand=False, inputType=str, date=False):
    if Main.state == "Cancelling":
        return None
    answer = input(message)
    while len(answer) == 0 or len(answer.split()) == 0:
        answer = input(message)
    possibleCommand = answer.upper().replace(" ", "")

    if isCommand:
        answer = possibleCommand
    elif possibleCommand == "CANCEL":
        if commandList[possibleCommand]() is True:  # cancelling
            if Main.state == "Inputting":
                Main.state = "Cancelling"
                return None
        else:
            return GetInput(message, isCommand, inputType)
    else:
        answer = answer.split()  # break into a list

    if not isCommand:
        if inputType is not str:
            try:
                answer[0] = inputType(answer[0])
            except ValueError:
                answer[0] = GetInput(
                    "{0} is an invalid input. Please enter a {1} type: ".format(answer[0], inputType.__name__),
                    inputType=inputType)
            return answer[0]
        else:
            if not date:
                for x in range(len(answer)):
                    try:
                        answer[x] = int(answer[x])
                        answer[x] = GetInput(
                            "{0} is not a string. Please enter a string: ".format(answer[x]))
                    except ValueError:
                        continue
            return " ".join(answer)

    else:
        if answer not in commandList:
            return GetInput("Invalid Command. Enter the command again or type Help for the list of command "
                            , isCommand, inputType)
        else:
            return commandList[answer]()
            # https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute


def Help():
    print("Help")


def Cancel():
    confirm = input("Are you sure you want to cancel? (Y for yes, N for No) ")
    confirm = confirm.upper()
    while confirm not in ["Y", "N"]:
        confirm = input("Enter Y for yes, N for No: ")
    if confirm == "Y":
        return True
    else:
        return False


def Add():
    allParticipants.append(Participant())


def ShowF():
    print("Show First Name")


def ShowL():
    print("Show Last Name")


def Search():
    print("Search")


def TestPrint():
    if len(allParticipants) > 0:
        print(allParticipants[-1])
    else:
        print("There's no entry")


def ExitProg():
    confirm = input("Are you sure you want to exit? (Y for yes, N for No) ")
    confirm = confirm.upper()
    while confirm not in ["Y", "N"]:
        confirm = input("Enter Y for yes, N for No: ")
    if confirm == "Y":
        return "Exiting"


commandList = {"ADD": Add,
               "HELP": Help,
               "CANCEL": Cancel,
               "SHOWF": ShowF,
               "SHOW": ShowL,
               "SEARCH": Search,
               "PRINT": TestPrint,
               "EXIT": ExitProg,
               }

allParticipants = []
