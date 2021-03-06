# Minh Au       #
# Comp Sci 20   #
# 20/06/2020    #
#################
from Final_Project import Functionalities as Func
from Final_Project import Main_Program as Main
import re  # to use search() for checking email
import datetime  # to check date


############################
# Contestant's information #
############################

class Participant:
    def __init__(self, loadData=None): # constructor
        '''Input all the information of the contestant
        Key Arguments:
            - loadData:
                + None if the user enters information manually
                + str if reading from a file
        '''
        Main.state = "Inputting" # set the state of the program

        if loadData is None: # enter the information manually
            print("----Enter participant's information----\n")
            self.Id = Func.GetInput("Please enter your Id: ", inputType=int)
            self.Name = Func.GetInput("Please enter your full name: ")
            self.Age = Func.GetInput("Please enter your age: ", inputType=int)
            self.birthday = Func.GetInput("Please enter your birthday (mm/dd/yyyy): ", date=True)
            self.schoolDistrict = Func.GetInput("Please enter your school district: ")
            self.email = Func.GetInput("Please enter your email: ")
            self.competition = Func.GetInput("Please enter your competition: ")
            self.score = Func.GetInput("Please enter your score: ", inputType=float)
            print("----    Done Entering Information    ----\n")
        else:
            # dissect the string and analyze the information
            information = loadData.split()
            try:
                self.Id = int(information[0])
            except ValueError:
                print(information[0] + " is not a valid ID")
                self.Id = Func.GetInput("Please enter your Id: ", inputType=int)
            dummyName = ""
            lastIndex = 1
            for x in information[1:]:
                try:
                    int(x)
                    break
                except ValueError:
                    dummyName += x + " "
                    lastIndex += 1

            self.Name = dummyName
            try:
                self.Age = int(information[lastIndex])
            except ValueError:
                print(information[lastIndex] + " is not a valid age.")
                self.Age = Func.GetInput("Please enter your age: ", inputType=int)
            lastIndex += 1
            self.birthday = information[lastIndex]
            lastIndex += 1
            self.schoolDistrict = information[lastIndex]
            lastIndex += 1
            self.email = information[lastIndex]
            lastIndex += 1
            try:
                self.score = float(information[-1])
            except ValueError:
                print(information[-1] + " is an invalid score")
                self.score = Func.GetInput("Please enter your score: ", inputType=float)
            self.competition = " ".join(information[lastIndex:-1])
        Main.state = "Running"

    def __del__(self):
        if Main.state == "Exiting":
            return
        if self.Id is None:
            print("Deleting this participant\n")
        else:
            print("Deleting participant ", self.Id, "\n")

    def __str__(self):
        allInformation = \
            [str(self.Id), self.Name,
             str(self.Age), str(self.birthday.date()), self.schoolDistrict,
             self.email, self.competition, str(self.score)]
        return " ".join(allInformation)

    def CalculateAge(self, birth):
        '''Calculate the age of the contestant based on birthdate
        Key Argument:
            - birth: contestant birthdate, format: mm/dd/yyyy (date)
        '''
        today = datetime.datetime.today()
        if today.month < birth.month or \
                (today.month == birth.month and today.day < birth.day):
            return today.year - birth.year - 1
        else:
            return today.year - birth.year

    def CheckBirthAndAge(self):
        '''Check if the birthday and age are correlated'''
        try:
            birth = self.birthday
        except AttributeError:
            return

        if self.CalculateAge(birth) != self.Age:
            print("Birthday and age are not correlated. Please check your birthday or age.")
            confirmation = Func.GetInput("Do you want to change birthday or age? ")
            if confirmation is None:
                return "Canceled"
            while confirmation.upper() not in ["BIRTHDAY", "AGE"]:
                print("Invalid input. Please enter 'birthday' or 'age'")
                confirmation = Func.GetInput("Do you want to change birthday or age?")
            if confirmation.upper() == "BIRTHDAY":
                self.birthday = Func.GetInput("Please enter your birthday (mm/dd/yyyy): ", date=True)
            else:
                self.Age = Func.GetInput("Please enter your age: ", inputType=int)

    # Getter functions of all the information
    @property
    def Id(self):
        return self._Id

    @property
    def Age(self):
        return self._Age

    @property
    def Name(self):
        return self._Name

    @property
    def firstName(self):
        return self._firstName

    @property
    def lastName(self):
        return self._lastName

    @property
    def email(self):
        return self._email

    @property
    def schoolDistrict(self):
        return self._schoolDistrict

    @property
    def birthday(self):
        return self._birthday

    @property
    def competition(self):
        return self._competition

    @property
    def score(self):
        return self._score

    @Id.setter
    def Id(self, newId):
        '''Check the validity of the ID'''
        if newId is None:
            self._Id = None
            return
        while len(str(newId)) != 8 or newId in Func.allId: # check if it's the right format and if it's unique
            if newId in Func.allId:
                print("{0} already exists. Please enter another one.".format(newId))
            else:
                print("Invalid ID")
            newId = Func.GetInput("Please enter your ID: ", inputType=int)
            if newId is None:
                self._Id = None
                return
        self._Id = newId

    @Age.setter
    def Age(self, newAge):
        '''Check the age of the contestant. The range is from 14 to 19 years old'''
        if newAge is None:
            return
        while newAge < 14:
            print("Too Young")
            newAge = Func.GetInput("Please enter your age: ", inputType=int)

        while newAge > 19:
            print("Too Old")
            newAge = Func.GetInput("Please enter your age: ", inputType=int)
        self._Age = newAge
        confirmation = self.CheckBirthAndAge() # check if it correlates with the birthday
        if type(confirmation) is str:
            if confirmation == "Canceled":
                Main.state = "Inputting"
                self.Age = Func.GetInput("Please enter your age: ", inputType=int)

    @Name.setter
    def Name(self, newName):
        '''Split the name to first name and last name'''
        if newName is None:
            return
        while len(newName.split()) <= 1:
            print("You're missing last name")
            newName = Func.GetInput("Please enter full name: ")

        newName = newName.split()
        self._firstName = newName[0]
        self._lastName = " ".join(newName[1:])
        self._Name = self.firstName + " " + self.lastName

    @email.setter
    def email(self, newEmail):
        '''check the validity of the email'''
        if newEmail is None:
            return
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        while re.search(regex, newEmail) is None:
            print("Invalid email.")
            newEmail = Func.GetInput("Please enter your email: ")
        self._email = newEmail

    @schoolDistrict.setter
    def schoolDistrict(self, newSchool):
        '''Check the validity of the school district'''
        if newSchool is None:
            return
        with open("Schools_And_Competitions/schoolDistricts.md") as file:
            text = file.read()
        text = text.split("\n\n")
        while True:
            dummySchool = newSchool.upper().replace(" ", "_")
            if dummySchool in text:
                break
            print("Invalid school District. Type help for the list")
            newSchool = Func.GetInput("Please enter your school district: ")
        self._schoolDistrict = newSchool.upper()

    @birthday.setter
    def birthday(self, newBirth):
        '''Check the validity of the birthdate'''

        if newBirth is None:
            return
        patterns = ['%m/%d/%Y', '%m %d %Y', '%m-%d-%Y', '%Y-%m-%d'] # different valid birthdate input
        while type(newBirth) is str:
            for x in range(len(patterns)):
                try:
                    newBirth = datetime.datetime.strptime(newBirth, patterns[x])
                    break
                except ValueError:
                    if x == len(patterns) - 1:
                        print("Invalid birthday. Type help for valid formats")
                        newBirth = Func.GetInput("Please enter your birthday (mm/dd/yyyy): ", date=True)
        self._birthday = newBirth
        confirmation = self.CheckBirthAndAge() # check if it correlates with the age
        if type(confirmation) is str:
            if confirmation == "Canceled":
                Main.state = "Inputting"
                self.birthday = Func.GetInput("Please enter your birthday (mm/dd/yyyy): ", date=True)

    @competition.setter
    def competition(self, newComp):
        '''Check the validity of the competition'''
        if newComp is None:
            return
        with open("Schools_And_Competitions\\Competitions.md") as file:
            text = file.read()
        text = text.split("\n")
        newComp = newComp.upper()
        while newComp not in text:
            print("Invalid competition. Type help for the list")
            newComp = Func.GetInput("Please enter your competition: ")
            newComp = newComp.upper()

        self._competition = newComp

    @score.setter
    def score(self, newScore):
        '''Check the validity of the score (percentage)'''

        if newScore is None:
            self._score = None
            return
        while newScore < 0 or newScore > 100:
            print("Invalid score. Please enter a score between 0 and 100 (inclusively)")
            self.score = Func.GetInput("Please enter your score: ", inputType=float)
        self._score = newScore
