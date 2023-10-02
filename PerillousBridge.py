import random
from time import sleep
random.seed()

########################################################### TETRAMINOS ##########################################################

I=['1111000000000000','1000100010001000','1111000000000000','1000100010001000']
O=['1100110000000000','1100110000000000','1100110000000000','1100110000000000']
T=['1110010000000000','0100110001000000','0100111000000000','1000110010000000']
J=['1110001000000000','0100010011000000','1000111000000000','1100100010000000']
L=['1110100000000000','1100010001000000','0010111000000000','1000100011000000']
Z=['1100011000000000','0100110010000000','1100011000000000','0100110010000000']
S=['0110110000000000','1000110001000000','0110110000000000','1000110001000000']

tetraminos={'I':I,'O':O,'T':T,'J':J,'L':L,'Z':Z,'S':S}

# max length of each tetramino in each position
maxLenght={'I':[4,1,4,1],'O':[2,2,2,2],'T':[3,2,3,2],'J':[3,2,3,2],'L':[3,2,3,2],'Z':[3,2,3,2],'S':[3,2,3,2]}


########################################################### DISPLAY ##########################################################

def displayBoard(board,start,goal):
    value = ' '
    print('\n         0 1 2 3 4 5 6 7 8 9')
    for i in range(len(board)):
        display = ''
        print('        ---------------------')
        if start == len(board)-i-1 :
            display += 'start'
        else:
            display += '     '
        display += ' ' + str(9-i) + ' |'

        # each case can be empty, a tetramino, a locked tetramino or the player
        for j in range (10):
            
            # if the case is empty
            if board[i][j] == 0:
                value = ' '
            
            # if the case is a tetramino, locked or not
            elif board[i][j] == 1 or board[i][j] == 2:
                value = '█'
            
            # if the case is the player
            elif board[i][j] == 3:
                value = '🧍'

            display += value + '|'

        if goal == len(board)-i-1 :
            display += ' goal'

        print(display)
    print('        ---------------------')
    return 0


def displayTetramino(tetramino):
    randomTetraminoStr=''
    for i in range (len(tetramino)):
        if tetramino[i]=='1':
            randomTetraminoStr += "■ "
        else:
            randomTetraminoStr += "  "
        if (i+1)%4==0 and i+1 != len(tetramino):
            randomTetraminoStr += '\n'
    print(randomTetraminoStr)


########################################################### BACK ##########################################################

# if we can't slide, we have to lock the board
def doILock(board):
    shouldILock = False
    for i in range (9):
        for j in range (10):
            if board[i+1][j] == 2 and board[i][j] == 1:
                shouldILock = True
    for j in range (10):
        if board[9][j] != 2 and board[9][j] == 1:
            shouldILock = True

    return shouldILock


def lockBoard(board):
    for i in range (10):
        for j in range (10):
            if board[i][j] == 1 :
                board[i][j] = 2
    return 0


def slide(board):
    for i in range (9):
        currentLine = 8-i
        for j in range (10):
            # start from top
            stateCaseUnder = board[currentLine+1][j]
            
            # if the case under is empty
            if stateCaseUnder != 2 and board[currentLine][j] == 1:
                # change the state of the case under
                board[currentLine+1][j] = 1
                # change the state of the case
                board[currentLine][j] = 0


def canIInsertTetramino(board,tetraminos,tetramino,column,position):
    returnValue=True
    column = int(column)

    # if the tetramino is out of the board
    if column == 7 and maxLenght[tetramino][position] >= 4 :
        returnValue=False
    elif column == 8 and maxLenght[tetramino][position] >= 3 :
        returnValue=False
    elif column == 9 and maxLenght[tetramino][position] >= 2:
        returnValue=False

    # else
    if returnValue==True:
        # for each column of the tetramino
        for i in range (maxLenght[tetramino][position]):
            # for each line of the tetramino
            for j in range (4):
                # target case must be empty
                if int(board[j][column+i]) != 0 and int(tetraminos[tetramino][position][i+4*j]) == 1:
                    returnValue=False
    return returnValue


def insertTetramino(board,tetraminos,tetramino,column,position):
    counter = 0
    column = int (column)
    # for each line of the tetramino
    for i in range (4):
        # for each column of the tetramino
        for j in range (4-(4-maxLenght[tetramino][position%4])):
            if board[i][column+j] != 2:
                board[i][column+j] = int(tetraminos[tetramino][position][counter])
            counter += 1
        counter += (4-maxLenght[tetramino][position%4])

    return 0


def isGameWin(board,start,goal):
    returnValue = False
    startHeight = 9-start
    goalHeight = 9-goal
    bridgeLength=0
    bridgeHeight=0
    
    # if the start is not empty
    if board[startHeight][0]!=0:
        bridgeLength += 1
        bridgeHeight=startHeight

        # we check the next cases (1-8)
        for i in range (8):
            #special case : bridge is on the bottom
            if bridgeHeight == 9 :
                # go up
                if board[bridgeHeight-1][i+1]!=0:
                    bridgeHeight=bridgeHeight-1
                    bridgeLength += 1
                # go ahead
                elif board[bridgeHeight][i+1]!=0:
                    bridgeLength += 1

            #special case : bridge is on the top
            elif bridgeHeight == 0 :
                # go ahead
                if board[bridgeHeight][i+1]!=0:
                    bridgeLength += 1
                # go down
                elif board[bridgeHeight+1][i+1]!=0:
                    bridgeHeight=bridgeHeight+1
                    bridgeLength += 1
            else:
                #special case : bridge is near the top
                if bridgeHeight == 1:
                    # go up
                    if board[bridgeHeight-1][i+1]!=0:
                        bridgeHeight=bridgeHeight-1
                        bridgeLength += 1
                    # go ahead
                    elif board[bridgeHeight][i+1]!=0:
                        bridgeLength += 1
                    # go down
                    elif board[bridgeHeight+1][i+1]!=0:
                        bridgeHeight=bridgeHeight+1
                        bridgeLength += 1
                else :
                    if board[bridgeHeight-2][i+1]==0:
                        # go up
                        if board[bridgeHeight-1][i+1]!=0:
                            bridgeHeight=bridgeHeight-1
                            bridgeLength += 1
                        # go ahead
                        elif board[bridgeHeight][i+1]!=0:
                            bridgeLength += 1
                        # go down
                        elif board[bridgeHeight+1][i+1]!=0:
                            bridgeHeight=bridgeHeight+1
                            bridgeLength += 1

        # the bridge is complete from 0 to 8, we check the last case
        if bridgeLength == 9 and board[goalHeight][9]!=0:
            returnValue = True
    return returnValue


def isGameLose(board,start,goal,stockedTetramino,generatedTetraminos):
    returnValue = 0
    canIContinue = False

    # We first check that we can insert a tetramino (current or stocked) somewhere (if not, we lose)
    # for each column
    for i in range (10):
        # for each position
        for j in range (4):
            # current tetramino
            if canIInsertTetramino(board,tetraminos,generatedTetraminos[0][0],i,j) == True:
                canIContinue=True
            # stocked tetramino
            elif stockedTetramino[0] != '':
                 if canIInsertTetramino(board,tetraminos,stockedTetramino[0],i,j) == True:
                    canIContinue=True

    # if not lose, we check for forbidden cases (top left and right triangles)
    if canIContinue == True:
        # top left
        # for each column of the triangle
        for j in range (9-start):
            # for each line of the triangle
            for i in range (9-start-j):
                if board[9-start-i-j-1][j] == 2 :
                    returnValue = 1

        # top right
        # for each column of the triangle
        for j in range (9-goal):
            # for each line of the triangle
            for i in range (9-goal-j):
                if board[9-goal-i-j-1][9-j] == 2 :
                    returnValue = 1
    return returnValue


def printMyBoy(board,start,goal):

    # for each column
    for i in range (10):
        j=0
        while board[j][i] != 2:
            j=j+1
        if j != 0:
            board[j-1][i] = 3
            sleep(0.3)
            displayBoard(board,start,goal)
            board[j-1][i] = 0
    return 0


########################################################### APP ##########################################################

# start " a " game
def startGame(board,start,goal):
    gameIsQuitted = False
    generatedTetraminos = [[random.choice(list(tetraminos.keys())),random.randint(0,3)] for i in range(4)]
    stockedTetramino = ['',0]

    # game is not won or lost
    while (isGameLose(board,start,goal,stockedTetramino,generatedTetraminos)==0 and isGameWin(board,start,goal)==0 and gameIsQuitted==False):
        tetraminoIsDown = False
        columnIsChoosed = False
        tetraminoIsStocked = False

        # new piece is generated
        randomTetramino = random.choice(list(tetraminos.keys()))
        randomPosition = random.randint(0,3)

        # slide the next tetraminos array
        for i in range (3):
            generatedTetraminos[i][0] = generatedTetraminos[i+1][0]
            generatedTetraminos[i][1] = generatedTetraminos[i+1][1]

        # add the new tetramino
        generatedTetraminos[3][0] = randomTetramino
        generatedTetraminos[3][1] = randomPosition
        
        # while no valid action is done
        while columnIsChoosed == False and tetraminoIsStocked == False and gameIsQuitted == False:
            print('\n'*20)
            print("Next tetraminos :\nIn 3 turns : ",generatedTetraminos[3][0],
            "\nIn 2 turns : ",generatedTetraminos[2][0],
            "\nNext turn  : ",generatedTetraminos[1][0],"\n")

            # if there is a stocked tetramino
            if stockedTetramino[0] != '':
                print("Tetramino stocké :")
                displayTetramino(tetraminos[stockedTetramino[0]][stockedTetramino[1]])

            print("Now :")
            displayTetramino(tetraminos[generatedTetraminos[0][0]][generatedTetraminos[0][1]])

            displayBoard(board,start,goal)

            # print the action menu
            print("\nYour action :\nChoose column for your tetramino : 0-9\nTurn your tetramino : L-R\nStock your tetramino : S\nQuit the game : Q")
            action = input()
            
            # up action character (q --> Q, s --> S, l --> L, r --> R)
            if action.isnumeric() == False:
                action = action.upper()

            # we want to stock the tetramino and there is no tetramino stocked
            if action == 'S' and stockedTetramino[0] == '':
                stockedTetramino[0] = generatedTetraminos[0][0]
                stockedTetramino[1] = generatedTetraminos[0][1]
                tetraminoIsStocked = True

            # we want to swap the current tetramino and the stocked tetramino
            if action == 'S' and stockedTetramino[0] != '':
                tempTetramino = generatedTetraminos[0][0]
                tempPosition = generatedTetraminos[0][1]

                generatedTetraminos[0][0] = stockedTetramino[0]
                generatedTetraminos[0][1] = stockedTetramino[1]

                stockedTetramino[0] = tempTetramino
                stockedTetramino[1] = tempPosition

            # we want to insert the tetramino in a column
            elif action.isnumeric() == True:
                # we make sure the column is valid
                if int(action) >=0 and int(action) <=9 :
                    if canIInsertTetramino(board,tetraminos,generatedTetraminos[0][0],int(action),generatedTetraminos[0][1]) == True :
                        insertTetramino(board,tetraminos,generatedTetraminos[0][0],int(action),generatedTetraminos[0][1])
                        columnIsChoosed = True
                    else:
                        print("\nEntrez une colonne valide par rapport au tetramino")
                else:
                    print("\nEntrez une colonne entre 0 et 9")

            # we want to rotate the tetramino in clockwise direction
            elif action == 'R' :
                generatedTetraminos[0][1] = (generatedTetraminos[0][1] + 1)%4

            # we want to rotate the tetramino in trigonometric direction
            elif action == 'L' :
                generatedTetraminos[0][1] = (generatedTetraminos[0][1] - 1)%4

            # we want to quit the game
            elif action == 'Q' :
                gameIsQuitted = True

        # we wanted to insert the tetramino in a column and the colmun is valid
        if columnIsChoosed == True:
            # slide the tetramino until it can't slide anymore
            while tetraminoIsDown == False and action:
                if doILock(board) == True:
                    lockBoard(board)
                    tetraminoIsDown = True
                if tetraminoIsDown == False :
                    slide(board)
            print('\n'*30)
                    
    # print the victory message and animation if the game is won
    if isGameWin(board,start,goal) == True:
        printMyBoy(board,start,goal)
        print("\nGG !\n")            

    # print the defeat message if the game is lost
    elif isGameLose(board,start,goal,stockedTetramino,generatedTetraminos) == True:
        displayBoard(board,start,goal)
        print("\nYou lost !\n")

    # print the message if the game is quitted
    elif gameIsQuitted == True:
        print("\nGame dropped out !\n")


# main function
def goToMenu():
    start = 5
    goal = 8
    LeaveGame = False

    # while the player doesn't want to quit the game
    while LeaveGame==False:
        print("1 - Nouvelle partie\n2 - Options\n3 - Credits\n4 - Quitter le jeu\n")
        action = input()

        # we want to start a new game
        if action == '1':
            board = [[0 for j in range(10)] for i in range(10)]
            startGame(board,start,goal)
            print('\n'*5)

        # we want to change the options
        elif action == '2':
            newOptions = changeOptions(start,goal)
            
            # save the new options
            start = newOptions[0]
            goal = newOptions[1]
        
        # we want to see the credits
        elif action == '3':
            print("\CREDITS\n\nProducer/Designer\nMathieu Bedez\n\nArtist\nMathieu Bedez\n\nProgrammer\nMathieu Bedez\n\n")
        
        # we want to quit the game
        elif action == '4':
            print("\nGood Bye !")
            LeaveGame = True


def changeOptions(newStart,newGoal):
    stayToOptions = True

    # while the player doesn't want to quit the options menu
    while stayToOptions == True:
        print("\n1 - Départ\n2 - Arrivée\n3 - returnValue\n")
        action = input()

        # we want to change the start position
        if action == '1':
            print('\nDépart :')
            start = input()
            if start.isnumeric() == True:
                if int(start) >=0 and int(start) <=9 :
                    newStart = int(start)
                    print(f'\nStart set to {newStart} !')
                else:
                    print(f'\nIncorrect input !')
            else:
                print(f'\nIncorrect input !')

         # we want to change the goal position
        elif action == '2':
            print('\nArrivée :')
            goal = input()
            if str(goal).isnumeric() == True:
                if int(goal) >=0 and int(goal) <=9 :
                    newGoal = int(goal)
                    print(f'\nGoal set to {newGoal} !')
                else:
                    print(f'\nIncorrect input !')
            else:
                print(f'\nIncorrect input !')

        # we want to quit the options menu
        elif action == '3':
            stayToOptions = False
    print('\n')
    return [newStart,newGoal]

goToMenu()