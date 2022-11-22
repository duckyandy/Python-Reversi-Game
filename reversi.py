alphabetList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
x_change_list = [-1, 0, 1]
# list needed to scan through all directions x,y vector
y_change_list = [-1, 0, 1]


def askBoardLength():  # ask board length and handles input scope
    while True:
        boardLength = int(input("Enter board size: "))

        if (boardLength < 4):
            print("Too little blocks!")
            continue
        if (boardLength > 26):
            print("Too many blocks!")
            continue
        if (boardLength % 2 == 1):
            print("Enter a even board length.")
            continue
        else:
            break

    return boardLength


def getInitialBoard(n):  # sets initial board with the intial pieces

    initialBoard = [["." for i in range(n)] for j in range(n)]

    initialBoard[int((n/2)-1)][int((n/2)-1)] = "X"
    initialBoard[int(n/2)][int(n/2)] = "X"
    initialBoard[int((n/2)-1)][int(n/2)] = "O"
    initialBoard[int(n/2)][int((n/2)-1)] = "O"

    return initialBoard


def printBoard(nestedArray):  # print nested array board to formatted board
    startSpace = "  "

    for i in range(len(nestedArray[0])):
        startSpace += f" {alphabetList[i]}"

    print(startSpace)

    for i in range(len(nestedArray[0])):
        if len(str(i+1)) == 1:
            stringBlock = f" {i+1}"
        else:
            stringBlock = f"{i+1}"

        for j in range(len(nestedArray[0])):
            stringBlock += f" {nestedArray[i][j]}"
        print(stringBlock)


def placeBlock(board, blockType, x, y):  # places block on position y, x

    board[y][x] = blockType

    return (board)


def getOtherPlayer(player):  # get opponent block(x or o)
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    else:
        return None


def valid_moves(board: list[list[str]], p: str, y: int, x: int,
                flip: bool = False):

    N = int(len(board[0]) - 1)

    if (y > N or y < 0 or x > N or x < 0):  # if position is out of bound

        return False

    elif (board[y][x] != "."):  # if position is not an empty cell

        return False

    EatenX = []  # eaten x,y needed to later append eaten pieces after checking
    EatenY = []
    row = 0
    col = 0
    valid_move_N = 0

    for x_change in x_change_list:  # loops through all direction vector combinations
        for y_change in y_change_list:
            if ((x_change == 0 and y_change == 0) or (y + y_change < 0) or (y + y_change > N)
                    or (x + x_change < 0) or (x + x_change > N)):  # passing when direction vector is 0,0
                continue  # also checking so that it stays in bound
            if (board[y + y_change][x + x_change] == getOtherPlayer(p)):  # if found opponent piece
                # continues to check
                row = x + x_change
                col = y + y_change
                count = 1
                while True:
                    row += x_change
                    col += y_change
                    count += 1
                    if (row < 0 or row >= N or col < 0 or col >= N):
                        break
                    if (board[col][row] == "." or board[col][row] == "#"):
                        break
                    if (board[col][row] == p):

                        valid_move_N += 1

                        for number in range(0, count):
                            EatenX.append(x+(x_change * number))
                            EatenY.append(y+(y_change * number))
                        # eaten x y has coordinates of pieces to eat

                        break

    if (valid_move_N >= 1 and flip == True):

        for element in range(len(EatenX)):
            placeBlock(board, p, EatenX[element], EatenY[element])
        # places the blocks for the eaten pieces

    if (valid_move_N >= 1 and flip == False):
        return True

    if (valid_move_N == 0):

        return False


def has_valid_moves(board: list[list[str]], p: str):
    boardL = len(board[0])

    for yval in range(boardL):
        for xval in range(boardL):
            if (valid_moves(board, p, yval, xval, False) == True):
                return True

    return False


def has_empty_cells(board: list[list[str]]):
    boardL = len(board[0])

    for yval in range(boardL):
        for xval in range(boardL):
            if board[yval][xval] == ".":
                return True
    return False


def count_board_end_game(board: list[list[str]]):
    boardL = len(board[0])
    XCount = 0
    OCount = 0

    for yval in range(boardL):
        for xval in range(boardL):
            if board[yval][xval] == "X":
                XCount += 1
            elif board[yval][xval] == "O":
                OCount += 1
            else:
                continue
    if (XCount > OCount):
        print("Player X wins!")

    elif (OCount > XCount):
        print("Player O wins!")
    else:
        print("Draw game!")


def main():
    blocksPlaced = []
    allowedX = []
    allowedY = []
    boardSize = int(askBoardLength())
    roundNum = 1
    PlayerXHasMove = True
    PlayerOHasMove = True
    consecutivePassCount = 0

    for i in range(0, boardSize):
        allowedX.append(alphabetList[i].upper())
        allowedY.append(i+1)

    maxNumBlocks = int((boardSize ** 2)/2)
    print(maxNumBlocks)
    while True:
        NumBlocksToPlace = int(input("Enter number of blocks: "))

        if (NumBlocksToPlace > maxNumBlocks):
            print("Too many blocks!")
            continue
        else:
            break
    print(NumBlocksToPlace)

    gameBoard = getInitialBoard(boardSize)
    printBoard(gameBoard)

    n = 1
    while n <= NumBlocksToPlace:

        blockLoc = input(f"Enter position for block {n}: ")

        locationModified = blockLoc.upper()

        if (len(locationModified) == 3):
            y = int(locationModified[1] + locationModified[2]) - 1
        else:
            y = int(locationModified[1]) - 1

        XLetter = locationModified[0]
        x = alphabetList.index(XLetter)

        if (XLetter in allowedX and y+1 in allowedY):  # checks if valid x and y
            pass
        else:
            print("Invalid position!")
            continue

        if (gameBoard[y][x] == "."):
            placeBlock(gameBoard, "#", x, y)
            n += 1
        else:
            print("Invalid position!")
            continue

    while True:

        if (PlayerXHasMove and PlayerOHasMove):
            if (roundNum % 2 == 1):
                Player = "X"
            else:
                Player = "O"
        elif (PlayerXHasMove and PlayerOHasMove == False):
            Player = "X"
        else:
            Player = "O"

        print(f"Round {roundNum}: ")
        printBoard(gameBoard)

        if (has_valid_moves(gameBoard, Player) == True):

            # gets x, y based on input
            turnPlace = input(f"Player {Player}'s turn: ")

            locationModified2 = turnPlace.upper()

            # B2
            if (len(locationModified2) == 3):
                y = int(locationModified2[1] + locationModified2[2]) - 1
            else:
                y = int(locationModified2[1]) - 1

            XLetter = locationModified2[0]
            x = alphabetList.index(XLetter)

            if (XLetter in allowedX and y+1 in allowedY):  # again checks x y input
                pass
            else:
                print("Invalid position!")
                continue

            if (valid_moves(gameBoard, Player, y, x, False) == True):
                valid_moves(gameBoard, Player, y, x, True)

                if (has_empty_cells == False):  # if no more empty places counts board
                    print("Game over:")
                    printBoard(gameBoard)
                    count_board_end_game(gameBoard)
                    return

            else:
                print("Invalid position!")
                continue

        else:
            print(f"Player {Player} has no valid moves! Pass!")
            consecutivePassCount += 1

            if (consecutivePassCount == 2):  # when consecutive pass is 2 counts board to get winner
                print("Game over:")
                printBoard(gameBoard)
                count_board_end_game(gameBoard)
                return

            if (Player == "X"):
                PlayerXHasMove = False
            else:
                PlayerOHasMove = False

        roundNum += 1


if __name__ == "__main__":
    main()
