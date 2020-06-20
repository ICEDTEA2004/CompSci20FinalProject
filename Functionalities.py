# Minh Au       #
# Comp Sci 20   #
# 20/06/2020    #
#################
from Final_Project.Class_Participant import *
from Final_Project import Main_Program as Main


#####################################
# Contains all the functionalities, #
# commands and database             #
# NOTE: the program won't run if    #
# this file is executed. Please run #
# the Main_Program.py instead       #
#####################################

def GetInput(message, isCommand=False, inputType=str, date=False, searching=False):
    '''This function gets input from the user and briefly check the input

    Key arguments:
        - message: the output message (str)
        - isCommand: if the input is a command (bool)
        - inputType: used to check the type of the input (str,int,float)
        - date: if the input is a date (bool)
        - searching: if the user is searching for entries (bool)
    Return:
        - None: when the cancel command is called
        - The user's input after checking its type
    '''
    if Main.state == "Cancelling":  # if the cancel command is called return None
        return None
    answer = input(message)
    while len(answer) == 0 or len(answer.split()) == 0:
        answer = input(message)
    possibleCommand = answer.upper().replace(" ", "")  # it could be cancel command

    if isCommand:
        answer = possibleCommand
    elif possibleCommand == "CANCEL":  # allow the user to call cancel command at any time
        if commandList[possibleCommand]() is True:  # cancelling
            if Main.state == "Inputting":
                Main.state = "Cancelling"
            return None
        else:
            return GetInput(message, isCommand, inputType)  # ask for the same input
    else:
        answer = answer.split()  # break into a list

    if not isCommand:
        if inputType is not str:
            # if the input type must be int, check the input and take only the first number
            # for example, if the user inputs 23 100, only 23 is taken
            try:
                answer[0] = inputType(answer[0])
            except ValueError:
                answer[0] = GetInput(
                    "{0} is an invalid input. Please enter a {1} type: ".format(answer[0], inputType.__name__),
                    inputType=inputType)
            return answer[0]
        else:
            if not date and not searching:  # This is used to check name, school district, competitions
                for x in range(len(answer)):
                    try:
                        answer[x] = int(answer[x])
                        answer[x] = GetInput(
                            "{0} is not a string. Please enter a string: ".format(answer[x]))
                    except ValueError:
                        continue
            return " ".join(answer)

    else:
        if answer not in commandList:  # Unknown command
            return GetInput("Invalid Command. Enter the command again or type Help for the list of command "
                            , isCommand, inputType)
        else:
            return commandList[answer]()  # execute the command
            # https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute


def Help():
    '''Show the user instructions'''
    with open("README.md") as file:  #
        text = file.read()
    print(text)


def Cancel():
    '''Check if the user wants to cancel the current command'''
    confirm = input("Are you sure you want to cancel? (Y for yes, N for No) ")
    confirm = confirm.upper()
    while confirm not in ["Y", "N"]:
        confirm = input("Enter Y for yes, N for No: ")
    if confirm == "Y":
        return True
    else:
        return False


def DeleteEntry():
    '''Delete a specific entry based on ID'''
    idToDel = GetInput("What entry do you want to delete? (Enter an ID) ", inputType=int)
    if idToDel is None:  # cancelling
        return
    while len(str(idToDel)) < 8:  # check the validity of the ID
        idToDel = GetInput("Invalid ID")
    if idToDel not in allId:  # check if the ID exists
        print("This ID does not exist")
    else:
        dummy = allId.pop(idToDel)  # delete the ID

        for x in range(len(allParticipants)):
            if allParticipants[x] == dummy:  # delete the entry
                del allParticipants[x]
                break


def Add(data=None):
    '''Add contestant to the datatbase
    Key arguments:
        - data: data from a file (str or None)
    '''
    if data is None:  # Manually input the entry
        allParticipants.append(Participant())
        allId[allParticipants[-1].Id] = allParticipants[-1]
    else:  # Get data from a file
        allParticipants.append(Participant(data))
        if allParticipants[-1].Id is not None:
            allId[allParticipants[-1].Id] = allParticipants[-1]


def ShowF():
    '''Display the database sorted by first name'''

    def Comp(entry):
        '''Used with the sort() to sort first name'''
        return entry.firstName

    if len(allParticipants) == 0:
        print("There's no entry")
        return
    allParticipants.sort(key=Comp)
    ListPrint(allParticipants)


def ShowL():
    '''Display the database sorted by last name'''

    def Comp(entry):
        '''Used with the sort() to sort last name'''
        return entry.lastName

    if len(allParticipants) == 0:
        print("There's no entry")
        return
    allParticipants.sort(key=Comp)
    ListPrint(allParticipants)


def ShowTop():
    '''Display the top 3 contestant of a particular event'''

    def Score(entry):
        '''Used with the sort() to sort the scores'''
        return entry.score

    filteredList = Search(True)  # ask for the particular event

    if filteredList is not None:  # there's at leat one contestant in the event
        filteredList.sort(key=Score, reverse=True)
        for x in range(len(filteredList)):
            if x == 3:
                return
            else:
                print(filteredList[x])
    return


def Search(top=False):
    '''Search for a specific contest or a list of relevant contestants
    Key arguments:
        - top: if the user wants to display the top 3 contestant in the event (bool)
    Return: list of contestants in an event when top = True otherwise, return NOne
    '''

    def FilterSchool(entry):
        '''User with filter() to get search for contestants with the specific school district'''
        if entry.schoolDistrict == searchFor:
            return True
        else:
            return False

    def FilterFirstName(entry):
        '''User with filter() to get search for contestants with the specific first name'''

        if entry.firstName.upper() == searchFor:
            return True
        else:
            return False

    def FilterLastName(entry):
        '''User with filter() to get search for contestants with the specific last name'''

        if entry.lastName.upper() == searchFor:
            return True
        else:
            return False

    def FilterComp(entry):
        '''User with filter() to get search for contestants with the specific competition'''

        if entry.competition == searchFor:
            return True
        else:
            return False

    if len(allParticipants) == 0:  # the database is empty
        print("There's no entry")
        return
    if top:  # search for a particular event
        searchFor = GetInput("Top 3 of which competition? ")
    else:  # the user can input ID, school district, first name, last name or competition
        searchFor = GetInput("What entry do you want to search for? ", searching=True)
    if searchFor is None:  # cancelling
        return
    if not top:
        try:
            searchFor = int(searchFor)  # check if the input is an ID
            if searchFor in allId:
                print(allId[searchFor])
            else:
                print("There's no ID like ", searchFor)
                Search()
            return
        except ValueError:
            pass
    org = searchFor
    searchFor = searchFor.upper()

    with open("Schools_And_Competitions/Competitions.md") as file:  # search for competition
        text = file.read()
    text = text.split("\n")
    if searchFor in text:
        competitions = list(filter(FilterComp, allParticipants))
        if top:
            return competitions
        if len(competitions) > 0:  # print all the contestants in this competition
            ListPrint(competitions, True)
            return
    else:
        if top:
            print("There's no " + searchFor + " in current database")
            return

    with open("Schools_And_Competitions/schoolDistricts.md") as file:  # search for school districts
        text = file.read()
    text = text.split("\n\n")
    if searchFor in text:
        schoolEntries = list(filter(FilterSchool, allParticipants))

        if len(schoolEntries) > 0:  # print all the contestants in this school district
            ListPrint(schoolEntries, True)
            return

    firstNameEntries = list(filter(FilterFirstName, allParticipants))
    if len(firstNameEntries) == 0:  # search for contestants with this first name
        lastNameEntries = list(filter(FilterLastName, allParticipants))
        if len(lastNameEntries) > 0:  # search for contestants with this last name
            ListPrint(lastNameEntries, True)
            return
    else:
        ListPrint(firstNameEntries, True)
        return
    print("Can't find '{0}'".format(org))  # can't be found
    Search()


def ListPrint(listOFEntries=None, search=False):
    '''Used to print the list of entries
    Key arguments:
        - listOfEntries: a list of entries (list)
        - search: display the searched contestants sorted by ID
    '''

    def SortId(entry):
        '''Used with sort() to sort the list by ID'''
        return entry.Id

    if Main.state == "Exiting":  # the program is exiting
        if len(allParticipants) > 0:
            return sorted(allParticipants, key=SortId)  # return the database sorted by ID
        else:
            return None

    if listOFEntries is None:
        if len(allParticipants) > 0:  # print the last contestant in the database
            print(allParticipants[-1])
        else:
            print("There's no entry")
    else:
        if search:  # display the searched contestants sorted by ID
            listOFEntries.sort(key=SortId)
        for x in listOFEntries:
            print(x)


def ExitProg():
    '''Exit the program'''
    confirm = input("Are you sure you want to exit? (Y for yes, N for No) ")  # Confirm with the user
    confirm = confirm.upper()
    while confirm not in ["Y", "N", 'y', 'n']:
        confirm = input("Enter Y for yes, N for No: ")
    if confirm == "Y":
        Main.state = "Exiting"
        UpdateFile()
        return "Exiting"


def UpdateFile():
    '''Save the current database to a file'''
    if currentFile is None:
        fileName = GetInput("Please enter the name of the file you want to save as: ")
        if fileName is None:  # cancelling
            return
        while Open(fileName):  # check if the file already exists
            if fileName is None:  # cancelling
                return
            print(fileName + " already exists")
            confirm = GetInput("Are you sure to overwrite this file? ")
            while confirm not in ["y", "Y", "N", "n"]:
                print("Invalid input")
                confirm = GetInput("Please enter y for Yes and n for No: ")
            if confirm in ["N", "n"]:  # save as a new file
                # if the command cancel is called, the program will not save the database
                fileName = GetInput("Please enter the name of the file you want to save as: ")
                continue
            break
        with open("Saved Database/" + fileName, "w") as file:
            newData = ListPrint()
            for x in newData:
                print(x, file=file)
    else:
        confirm = GetInput("Are you sure to overwrite this file? ")  # update the opened file
        while confirm not in ["y", "Y", "N", "n"]:
            print("Invalid input")
            confirm = GetInput("Please enter y for Yes and n for No: ")
        if confirm in ["N", "n"]:
            return
        with open("Saved Database/" + currentFile, "w") as file:
            newData = ListPrint()
            for x in newData:
                print(x, file=file)
    return


def Open(fileName=None):
    '''Open a particular file
    Key Argument:
        - fileName: used to check if the file already exists (str)
    '''
    global currentFile
    if currentFile is not None:  # check if there's already an opened file
        print(currentFile + " is open")
        return
    checking = False
    if fileName is None:
        fileName = GetInput("Please enter the file name: ")
        if fileName is None:
            return None
    else:
        checking = True

    try:  # check if the file exists
        if checking:
            return False
        with open("Saved Database/" + fileName) as file:
            text = file.read()
        text = text.split("\n")
        if len(text) != 0:
            for x in text:
                if len(x) == 0:
                    continue
                Add(x)
        currentFile = fileName
    except FileNotFoundError:
        if checking:
            return True
        else:
            print("There's no file called " + fileName + ". Please try again")
        Open()


commandList = {"ADD": Add,  # all valid command
               "HELP": Help,
               "CANCEL": Cancel,
               "SHOWF": ShowF,
               "SHOW": ShowL,
               "SEARCH": Search,
               "EXIT": ExitProg,
               "OPEN": Open,
               "DEL": DeleteEntry,
               "TOP": ShowTop,
               }
currentFile = None  # name of the current opened file

allParticipants = []  # list of all contestants
allId = dict()  # dict of all IDs
