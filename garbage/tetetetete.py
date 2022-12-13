from os import system
import os

background = '.'
shapeIcon = '⯀'
ghostPiece = '□'
pieceColor = 238, 114, 3

board = [background*5]*5
RESET = '\033[0m'

def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


S = [[[1,0]]]

S = [[[1,0],[2,0]]]

S = [[[1,0],[2,0],[0,1]]]

S = [[[1,0],[2,0],[0,1],[1,1]]]




for xy in S[0]:
    llist = list(board[xy[1]])
    #set the correct coords to the shape icon
    llist[xy[0]] = shapeIcon
    board[xy[1]] = ''.join(llist)



clear()
for y in board:
    for x in y:
        if x == shapeIcon:
            print(get_color_escape(*pieceColor) + x + RESET + ' ', end='')
        elif x == ghostPiece:
            print(get_color_escape(80, 80, 80) + x + RESET + ' ', end='')
        else:
            print(x, end=' ')
    print()

print()
print()