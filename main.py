from os import system
import random
import time
from twisted.internet import task, reactor
import datetime
system('clear')


#------------------------------ Initialization ------------------------------#


#------------ Shapes & Colours ------------#
S = [[0,0],[0,1],[1,1],[1,2]]
O = [[0,0],[0,1],[1,0],[1,1]]
I = [[0,0],[0,1],[0,2],[0,3]]
J = [[0,0],[0,1],[0,2],[1,2]]
L = [[0,0],[0,1],[0,2],[1,0]]
T = [[0,0],[0,1],[0,2],[1,1]]
Z = [[0,0],[0,1],[1,1],[1,2]]

#set RGB values for every colour
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 127, 0), (0, 0, 255), (128, 0, 128), (128, 0, 128)]
shapes = [S,O,I, J, L, T, Z]#
absShapes = shapes

board = ['..........']*20

# create colour for reset after printing
RESET = '\033[0m'

#------------ Variables ------------#
count = 0
moved = False

x = 0
y = 0

time_lapsed = 0
start_time = time.time()
lastTime = datetime.datetime.now()


#------------------------------ Define Functions ------------------------------#


#get the color to print according to a RGB value
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

#print the current state of the board
def print_board(board):
    system('clear')
    for b in board:
        for c in b:
            # if spot is empty
            if c == '.':
                print(c + ' ', end='')
            else:
                # if spot is occupied print the shape wtih the correct color
                print(get_color_escape(currentColour[0], currentColour[1], currentColour[2]) + c + RESET + ' ', end='')
        print()
    print()
    try:
        print(f'Width: {width} Height: {height}')
        print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.', end='\n\n')
    except:
        pass


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
 

def gravity(board, shape):
    for s in shape:
        aaa = list(board[s[1]])
        aaa[s[0]] = '.'
        board[s[1]] = ''.join(aaa)
    for s in shape:
        absShapes[shapes.index(shape)][shape.index(s)][1] += 1
































currentShape = random.choice(shapes)
currentColour = colors[shapes.index(currentShape)]

width = max([item[0] for item in currentShape]) + min([item[0] for item in currentShape]) + 1
height = max([item[1] for item in currentShape]) + min([item[1] for item in currentShape]) + 1






while y < 19 - height + 1:
    start = time.time()
    period = datetime.datetime.now()
    if period.second % 0.5 == 0 and (period - lastTime).total_seconds() >= 1:
        y += 1
        gravity(board, currentShape)
        lastTime = period
        for coord in currentShape:
            aaa = list(board[coord[1]])
            aaa[coord[0]] = '0'
            board[coord[1]] = ''.join(aaa)

    print_board(board)



    count += 1
    end_time = time.time()
    time_lapsed = end_time - start_time
    time_convert(time_lapsed)   
    time.sleep(max(1./60 - (time.time() - start), 0))