from Final_Project.Class_Participant import *
from Final_Project import Main_Program as Main


def GetInput(message, isCommand=False, inputType=str, date=False, searching=False):
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
            if not date and not searching:
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


def Add(data=None):
    if data is None:
        allParticipants.append(Participant())
    else:
        allParticipants.append(Participant(data))
        allId[allParticipants[-1].Id] = allParticipants[-1]


def ShowF():
    def Comp(entry):
        return entry.firstName

    if len(allParticipants) == 0:
        print("There's no entry")
        return
    allParticipants.sort(key=Comp)
    ListPrint(allParticipants)
    # print([x for x in allParticipants])


def ShowL():
    def Comp(entry):
        return entry.lastName

    if len(allParticipants) == 0:
        print("There's no entry")
        return
    allParticipants.sort(key=Comp)
    ListPrint(allParticipants)


def Search():
    def FilterSchool(entry):
        if entry.schoolDistrict == searchFor:
            return True
        else:
            return False

    def FilterFirstName(entry):
        if entry.firstName.upper() == searchFor:
            return True
        else:
            return False

    def FilterLastName(entry):
        if entry.lastName.upper() == searchFor:
            return True
        else:
            return False

    def FilterComp(entry):
        if entry.competition == searchFor:
            return True
        else:
            return False

    if len(allParticipants) == 0:
        print("There's no entry")
        return
    searchFor = GetInput("What entry do you want to search for? ", searching=True)
    if searchFor is None:
        return
    try:
        searchFor = int(searchFor)
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

    with open("Schools_And_Competitions/schoolDistricts.md") as file:
        text = file.read()
    text = text.split("\n\n")
    if searchFor in text:
        schoolEntries = list(filter(FilterSchool, allParticipants))

        if len(schoolEntries) > 0:
            ListPrint(schoolEntries, True)
            return

    with open("Schools_And_Competitions/Competitions.md") as file:
        text = file.read()
    text = text.split("\n")
    if searchFor in text:
        competitions = list(filter(FilterComp, allParticipants))
        if len(competitions) > 0:
            ListPrint(competitions, True)
            return
    firstNameEntries = list(filter(FilterFirstName, allParticipants))
    if len(firstNameEntries) == 0:
        lastNameEntries = list(filter(FilterLastName, allParticipants))
        if len(lastNameEntries) > 0:
            ListPrint(lastNameEntries, True)
            return
    else:
        ListPrint(firstNameEntries, True)
        return
    print("Can't find '{0}'".format(org))
    Search()


def ListPrint(listOFEntries=None, search=False):
    def SortId(entry):
        return entry.Id

    if Main.state == "Exiting":
        if len(allParticipants) > 0:
            return sorted(allParticipants,key=SortId)
        else:
            return None

    if listOFEntries is None:
        if len(allParticipants) > 0:
            print(allParticipants[-1])
        else:
            print("There's no entry")
    else:
        if search:
            listOFEntries.sort(key=SortId)
        for x in listOFEntries:
            print(x)


def ExitProg():
    confirm = input("Are you sure you want to exit? (Y for yes, N for No) ")
    confirm = confirm.upper()
    while confirm not in ["Y", "N", 'y', 'n']:
        confirm = input("Enter Y for yes, N for No: ")
    if confirm == "Y":
        Main.state = "Exiting"
        UpdateFile()
        return "Exiting"


def UpdateFile():
    if currentFile is None:
        fileName = GetInput("Please enter the name of the file you want to save as: ")
        if fileName is None:  # cancelling
            return
        while Open(fileName):
            if fileName is None:  # cancelling
                return
            print(fileName + " already exists")
            confirm = GetInput("Are you sure to overwrite this file? ")
            while confirm not in ["y","Y","N","n"]:
                print("Invalid input")
                confirm = GetInput("Please enter y for Yes and n for No: ")
            if confirm in ["N","n"]:
                fileName = GetInput("Please enter the name of the file you want to save as: ")
                continue
            break
        with open("Saved Database/" + fileName, "w") as file:
            newData = ListPrint()
            for x in newData:
                print(x, file=file)
    else:
        with open("Saved Database/" + currentFile, "w") as file:
            newData = ListPrint()
            for x in newData:
                print(x, file=file)
    return


def Open(fileName=None):
    global currentFile
    if currentFile is not None:
        print(currentFile + " is open")
        return
    checking = False
    if fileName is None:
        fileName = GetInput("Please enter the file name: ")
        if fileName is None:
            return None
    else:
        checking = True

    try:
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


commandList = {"ADD": Add,
               "HELP": Help,
               "CANCEL": Cancel,
               "SHOWF": ShowF,
               "SHOW": ShowL,
               "SEARCH": Search,
               "PRINT": ListPrint,
               "EXIT": ExitProg,
               "OPEN": Open,
               }
currentFile = None

allParticipants = []
allId = dict()
