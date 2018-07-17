import random
import sys
class Tile:
    def __init__(self, mine):
        self.revealed = False
        self.mine = mine
        self.value = 0
        self.flagged = False


def createBoard(width, height, mines):
    board = []
    x = 0
    y = 0
    for i in range(width):
        board.append([])
        for j in range(height):
            board[i].append(Tile(False))

    for i in range(mines):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        board[x][y] = Tile(True)

    for i in range(width):
        for j in range(height):
            for dx in range (-1, 2):
                if i + dx >= 0 and i + dx < width:
                    for dy in range(-1, 2):
                        if j + dy >= 0 and j + dy < height:
                            if board[i + dx][j + dy].mine:
                                board[i][j].value = board[i][j].value + 1
    return board

def gameIsOver(board):
    all_revealed = True
    mine_struck = True
    width = len(board)
    height = len(board[0])
    for i in range(width):
        for j in range(height):
            if board[i][j].mine and board[i][j].revealed:
                return True
            if not board[i][j].revealed:
                all_revealed = False

def showBoard(board):
    dead = False
    print("      ", end = "")

    for c in range(len(board[0])):
        print("-%2d -" % (c + 1), end = "")
    print ("")

    for r in range(len(board)):
        print(" %3d " % (r + 1), end = "|")

        for c in range(len(board[0])):
            ch = "."
            tile = board[r][c]

            if tile.flagged:
                ch = "#"
            elif tile.revealed:
                if tile.mine:
                    ch = "X"
                    dead = True
                else:
                    ch = str(tile.value)
            print("  " + ch + "  ", end = "")
        print("")

    if dead:
        print("💥 Oh no! You stepped on a mine! 💥")

def selectSquare(board):
    col = int(input("Pick a column: ")) - 1
    row = int(input("Pick a row:    ")) - 1
    return (row, col)

def updateBoard(board, square):
    reveal(board, square[0], square[1])

def reveal(board, row, col):
    if illegalSquare(board, row, col):
        return
    elif board[row][col].revealed:
        return
    else:
        board[row][col].revealed = True

        if board[row][col].mine:
            return
        elif board[row][col].value > 0:
            return
        else:
            for hor in range(-1, 2):
                for ver in range(-1, 2):
                    reveal(board, row + ver, col + hor)

def illegalSquare(board, row, col):
    print("Checking: %d, %d" % (row, col))
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return True
    else:
        return False


b = createBoard(15, 10, 10)

while True: #This is where the fun begins
    showBoard(b)

    if gameIsOver(b): #Detects if the game is over
        print("GAME OVER")
        break

    s = selectSquare(b)
    updateBoard(b, s)