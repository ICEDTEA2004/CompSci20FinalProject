from Python.Final_Project import Functionalities as Func
from Python.Final_Project.Class_Participant import *


def Ha():
    print("ha")


def main():
    close = False
    Func.GetInput("Please enter your command ", isCommand=True)
    return close


if __name__ == '__main__':
    state = True
    while state:
        state = not main()
