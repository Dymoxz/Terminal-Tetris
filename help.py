from os import system
import os
import random
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

O = [[[0,0],[1,0],[0,1],[1,1]],
    [[0,0],[1,0],[0,1],[1,1]],
    [[0,0],[1,0],[0,1],[1,1]],
    [[0,0],[1,0],[0,1],[1,1]]]

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

background = '.'
shapeIcon = '⯀'

board = [background*10]*20
RESET = '\033[0m'

start_time = time.time()
lastTime = datetime.datetime.now()

def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


def print_board(shape_coords, boarding):
    local_board = copy.deepcopy(boarding)
    for xy in shape_coords:
        llist = list(local_board[xy[1]])
        llist[xy[0]] = shapeIcon
        local_board[xy[1]] = ''.join(llist)
    
    for y in local_board:
        for x in y:
            if x == shapeIcon:
                print(get_color_escape(63, 127, 176) + x + RESET + ' ', end='')
            else:
                print(x, end=' ')
        print()

def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

clear()
print_board([], board)

#------------------------------ Main ------------------------------#

currentShape = random.choice([S, I, O, L, J, Z, T])
# currentShape = I
currentRotation = currentShape[1]

real_y = min([xy[1] for xy in currentRotation])
real_x = min([xy[0] for xy in currentRotation])

y = 0
x = 0

height = max([xy[1] for xy in currentRotation]) - real_y + 1
width = max([xy[0] for xy in currentRotation]) - real_x + 1

absolute_rotation = [[xy[0] + x, xy[1] + y] for xy in currentRotation]


while real_y < 20 - height:
    start = time.time()
    period = datetime.datetime.now()
    if period.second % 1 == 0 and (period - lastTime).total_seconds() >= 0.2:
        lastTime = period
        clear()
        print_board(absolute_rotation, board)
        print(f'x: {x}, y: {y}, h: {height}, w: {width}, r_x: {real_x}, r_y: {real_y}', end='\r')
        real_y += 1
    absolute_rotation = [[xy[0] + x, xy[1] + real_y] for xy in currentRotation]

print()
print(f'x: {x}, y: {y}, h: {height}, w: {width}, r_x: {real_x}, r_y: {real_y}')
print()