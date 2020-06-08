from Python.Final_Project import Functionalities as Func


def main():
    # 4 main states: Running, Exiting, Inputting, Cancelling
    Func.GetInput("Please enter your command ", isCommand=True)
    if state == "Running" and len(Func.allParticipants) > 0:
        if Func.allParticipants[-1].score is None:
            del Func.allParticipants[-1]
    print(state)

state = None
if __name__ == '__main__':
    state = "Running"
    while state != "Exiting":
        main()
