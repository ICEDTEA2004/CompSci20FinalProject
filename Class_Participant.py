from Python.Final_Project import Functionalities as Func
import re  # to use search() for checking email


class Participant:
    def __init__(self):
        print("----Enter participant's information----\n")
        self.Id = Func.GetInput("Please enter your Id: ",inputType=int)
        self.Age = Func.GetInput("Please enter your age: ", inputType=int)
        self.Name = Func.GetInput("Please enter your full name: ")
        self.email = Func.GetInput("Please enter your email: ")
        self.schoolDistrict = Func.GetInput("Please enter your school district: ")
        self.birthday = Func.GetInput("Please enter your birthday: ")
        self.competition = Func.GetInput("Please enter your competition: ")
        self.score = Func.GetInput("Please enter your score: ", inputType=float)
        print("----    Done Entering Information    ----\n")

    # def __del__(self):
    #     if self.Id is None:
    #         print("Deleting this participant")
    #     else:
    #         print("Deleting participant ", self.Id)

    def __str__(self):
        pass

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
        while len(str(newId)) != 8:
            print("Invalid ID")
            newId = Func.GetInput("Please enter your ID: ",inputType=int)
        self._Id = newId

    @Age.setter
    def Age(self, newAge):
        while newAge < 14:
            print("Too Young")
            newAge = Func.GetInput("Please enter your age: ", inputType=int)

        while newAge >= 19:
            print("Too Old")
            newAge = Func.GetInput("Please enter your age: ", inputType=int)
        self._Age = newAge

    @Name.setter
    def Name(self, newName):

        while len(newName.split()) <= 1:
            print("You're missing last name")
            newName = Func.GetInput("Please enter full name: ")

        newName.split()
        self._firstName = newName[0]
        self._lastName = " ".join(newName[1:])
        self._Name = newName

    @email.setter
    def email(self, newEmail):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        while re.search(regex, newEmail) is None:
            print("Invalid email.")
            print(newEmail)
            newEmail = Func.GetInput("Please enter your email: ")
        self._email = newEmail

    @schoolDistrict.setter
    def schoolDistrict(self, newSchool):
        newSchool = newSchool.upper()
        with open("schoolDistricts.md") as file:
            text = file.read()
        text = text.split()
        while newSchool not in text:
            print("Invalid school District")
            self.schoolDistrict = Func.GetInput("Please enter your school district: ")
        self._schoolDistrict = newSchool

    @birthday.setter
    def birthday(self, newBirth):
        pass

    @competition.setter
    def competition(self, newComp):
        pass

    @score.setter
    def score(self, newScore):
        while newScore < 0 or newScore > 100:
            print("Invalid score. Please enter a score between 0 and 100 (inclusively)")
            self.score = Func.GetInput("Please enter your score: ", inputType=float)
        self._score = newScore
