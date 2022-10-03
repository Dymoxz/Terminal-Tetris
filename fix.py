from os import system
import os
import random
from re import X
import time
import datetime
from pynput import keyboard
import copy
#------------------------------ Initialization ------------------------------#


#------------ Shapes & Colours ------------#
S = [[[1,0],[2,0],[0,1],[1,1]],
    [[1,0],[1,1],[2,1],[2,2]],
    [[0,2],[1,1],[1,2],[2,1]],
    [[0,0],[0,1],[1,1],[1,2]]]

I = [[[0,1],[1,1],[2,1],[3,1]],
    [[2,0],[2,1],[2,2],[2,3]],
    [[0,2],[1,2],[2,2],[3,2]],
    [[1,0],[1,1],[1,2],[1,3]]]

O = [[[1,0],[2,0],[1,1],[2,1]],
    [[1,0],[2,0],[1,1],[2,1]],
    [[1,0],[2,0],[1,1],[2,1]],
    [[1,0],[2,0],[1,1],[2,1]]]

L = [[[0,1],[2,1],[1,1],[2,0]],
    [[1,0],[1,1],[1,2],[2,2]],
    [[0,1],[0,2],[1,1],[2,1]],
    [[0,0],[1,0],[1,1],[1,2]]]

J = [[[0,0],[0,1],[1,1],[2,1]],
    [[1,0],[1,1],[1,2],[2,0]],
    [[0,1],[1,1],[2,1],[2,2]],
    [[0,2],[1,0],[1,1],[1,2]]]

Z = [[[0,0],[1,0],[1,1],[2,1]],
    [[2,0],[2,1],[1,1],[1,2]],
    [[0,1],[1,1],[1,2],[2,2]],
    [[1,0],[1,1],[0,1],[0,2]]]

T = [[[0,1],[1,0],[1,1],[2,1]],
    [[1,0],[1,1],[1,2],[2,1]],
    [[0,1],[1,1],[1,2],[2,1]],
    [[1,0],[0,1],[1,1],[1,2]]]

#set RGB values for every colour
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (0, 0, 255), (255, 127, 0), (128, 0, 128), (128, 0, 128)]
shapes = [S,O,I, J, L, T, Z]

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

rotation = 0

#------------------------------ Define Functions ------------------------------#

#set RGB values for every colour
#get the color to print according to a RGB value
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

#print the current state of the board
def print_board(board):
    clear()
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

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

def gravity(board, shape):
    for coords in shape:
        ABSshapecoords = list(board[coords[1]])
        ABSshapecoords[coords[0]] = '.'
        board[coords[1]] = ''.join(ABSshapecoords)
    for s in range(0,len(shape)):
        currentABS[s][1] += 1


def on_press(key):
    global y
    global x
    global currentShape  
    global rotation
    global leftBound
    global moved
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['left', 'right', 'down', 'up']:
        if k == 'right':
            if x < 9 - width + 1:
                x += 1
        if k == 'left':
            if x > 0:
                x -= 1
        if k == 'down':
            y += 1
        for s in currentShape:
            aaa = list(board[s[1]])
            aaa[s[0]] = '.'
            board[s[1]] = ''.join(aaa)
        for s in currentShape:
                currentABS[currentShape.index(s)][0] + x
                currentABS[currentShape.index(s)][1] + y
        for coord in currentShape:
            aaa = list(board[coord[1]]) 
            aaa[coord[0]] = '0'
            board[coord[1]] = ''.join(aaa)
        print_board(board)
def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    return _

#------------------------------ Main Game ------------------------------#
clear()



currentShape = random.choice(shapes)
fullShape = currentShape
currentShape = currentShape[rotation]
currentABS = copy.deepcopy(currentShape)
fullABS = fullShape
currentColour = colors[shapes.index(fullShape)]



leftBound = min([item[0] for item in currentShape])
rightBound = max([item[0] for item in currentShape])

topBound = min([item[1] for item in currentShape])
bottomBound = max([item[1] for item in currentShape])

width = rightBound - leftBound + 1
height = bottomBound - topBound + 1

print_board(board)

x = leftBound

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

while y < 19 - height + 1:
    start = time.time()
    period = datetime.datetime.now()
    if period.second % 1 == 0 and (period - lastTime).total_seconds() >= 0.5:
        gravity(board, currentABS)
        lastTime = period
        for coord in currentABS:
            aaa = list(board[coord[1]]) 
            aaa[coord[0]] = '0'
            board[coord[1]] = ''.join(aaa)
        print_board(board)
        y += 1
    try:
        #print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.   |   Rotation: {rotation}', end='\r')
        # print(x, y, end='\r')
        print(currentABS, end='\r')
    except:
        pass
    #print(f'x: {x}   |   y: {y}', end='\r')

    count += 1
    end_time = time.time()
    time_lapsed = end_time - start_time
    time_convert(time_lapsed)   
    time.sleep(max(1./60 - (time.time() - start), 0))


listener.stop()
clear()
print_board(board)
print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.   |   Rotation: {rotation}')
print(f'X: {x}   |   Y: {y}')
print()