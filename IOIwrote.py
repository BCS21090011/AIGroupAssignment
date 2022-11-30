def ReadInt(qstStr:str="",inMin:int=None,inMax:int=None)->int:
    valid:bool=False
    userInput:int

    while valid==False:
        try:
            userInput=int(input(qstStr))
            valid=True

            if inMin!=None:
                if userInput<inMin:
                    valid=False

            if inMax!=None:
                if userInput>inMax:
                    valid=False

        except ValueError:
            valid=False

        if valid==False:
            print("Invalid input!")

    return userInput

def ReadFloat(qstStr:str="",inMin:float=None,inMax:float=None)->float:
    valid:bool=False
    userInput:float

    while valid==False:
        try:
            userInput=float(input(qstStr))
            valid=True

            if inMin!=None:
                if userInput<inMin:
                    valid=False

            if inMax!=None:
                if userInput>inMax:
                    valid=False

        except ValueError:
            valid=False

        if valid==False:
            print("Invalid input!")

    return userInput

def ReadStr(qstStr:str="", validStr=['y','Y','n','N'])->str:

    if validStr is None:
        validStr = ['y', 'Y', 'n', 'N']
    valid:bool=False
    userInput:str=""

    while valid==False:

        userInput=input(qstStr)

        if userInput in validStr:
            valid=True

        else:
            print("Invalid input!")

    return userInput

def YNDecision(decisionStr:str="")->bool:

    userInput:str='n'

    userInput=ReadStr(qstStr=decisionStr)

    if userInput in ['y','Y']:
        return True

    else:
        return False

if __name__ == "__main__":

    while True:
        userInput = ReadInt("int Input: ")
        print("User's int inputed: ", userInput)
        userInput = ReadFloat("float Input: ")
        print("User's float inputed: ", userInput)

    input()