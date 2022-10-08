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

#------------ Visuals ------------#
background = '.'
shapeIcon = '⯀'
ghostPiece = '□'
#---------------------------------#

board = [background*10]*20
RESET = '\033[0m'
main = True
board_coords = []
ghost_coords = []


#Variables needed for Time + FPS
start_time = time.time()
lastTime = datetime.datetime.now()
time_lapsed = 0.00000000000000000000000000000000000000000000001
count = 0
framelimit = 30

speed_dict = {
    0: 15.974, 
    1: 14.310,
    2: 12.646, 
    3: 10.982,
    4: 9.318, 
    5: 7.654,
    6: 5.990, 
    7: 4.326,
    8: 2.662, 
    9: 1.997,
    10: 1.664, 
    11: 1.664,
    12: 1.664, 
    13: 1.331,
    14: 1.331, 
    15: 1.331,
    16: 0.998, 
    17: 0.998,
    18: 0.998, 
    19: 0.666,
    20: 0.666, 
    21: 0.666,
    22: 0.666, 
    23: 0.666,
    24: 0.666, 
    25: 0.666,
    26: 0.666,
    27: 0.666,
    28: 0.666, 
    29: 0.333,
}

speed_dict = {
    0: {
        'time': 15.974,
        'lines': 10,
    },
    1: {
        'time': 14.310,
        'lines': 20,
    },
    2: {
        'time': 12.646,
        'lines': 30,
    },
    3: {
        'time': 10.982,
        'lines': 40,
    },
    4: {
        'time':  9.318,
        'lines': 50,
    },
    5: {
        'time': 7.654,
        'lines': 60,
    },
    6: {
        'time': 5.990,
        'lines': 70,
    },
    7: {
        'time': 4.326,
        'lines': 80,
    },
}



current_level = 0
line_clear_count = 0
speed_seconds = speed_dict[0]['time'] / 20
#------------------------------ Functions ------------------------------#
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def print_board(shape_coords, boarding, ghost):
    local_board = copy.deepcopy(boarding)
    for xy in shape_coords:
        llist = list(local_board[xy[1]])
        llist[xy[0]] = shapeIcon
        local_board[xy[1]] = ''.join(llist)
    
    for xb in ghost:
        llist = list(local_board[xb[1]])
        llist[xb[0]] = ghostPiece
        local_board[xb[1]] = ''.join(llist)
    
    clear()
    for y in local_board:
        for x in y:
            if x == shapeIcon:
                print(get_color_escape(63, 127, 176) + x + RESET + ' ', end='')
            elif x == ghostPiece:
                print(get_color_escape(80, 80, 80) + x + RESET + ' ', end='')
            else:
                print(x, end=' ')
        print()

def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

def on_press(key):
    global x, y, width, height, collisions
    global currentRotation, currentShape
    global main
    side_collisions = 0
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    
    if k in ['left', 'right', 'down', 'up', 'space']:
        left_cond = x > 0 and side_collisions == 0
        if k == 'left' and left_cond:
            for coord in currentRotation:
                if [coord[0] - 1,coord[1]] in board_coords:
                    side_collisions += 1
            if side_collisions == 0:
                x -= 1
                for rot in currentShape:
                    for xy in rot:
                        xy[0] -= 1
        
        right_cond = x < 9 - width and side_collisions == 0
        if k == 'right' and right_cond:
            for coord in currentRotation:
                if [coord[0] + 1,coord[1]] in board_coords:
                    side_collisions += 1
            if side_collisions == 0:
                x += 1
                for rot in currentShape:
                    for xy in rot:
                        xy[0] += 1
        down_cond = y < 19 - height and collisions == 0            
        if k == 'down' and down_cond:
                for coord in currentRotation:
                    if [coord[0],coord[1] + 1] in board_coords:
                        collisions += 1
                if collisions == 0:
                    y += 1
                    for rot in currentShape:
                        for xy in rot:
                            xy[1] += 1
        if k == 'up':
            currentRotation = currentShape[(currentShape.index(currentRotation) + 1) % 4]

            x = min(currentRotation, key=lambda xa: xa[0])[0]
            y = min(currentRotation, key=lambda ya: ya[1])[1]

            width = max(currentRotation, key=lambda xa: xa[0])[0] - x
            height = max(currentRotation, key=lambda ya: ya[1])[1] - y
        
        if k == 'space':
            pass

        print_board(currentRotation + board_coords, board, ghost_coords)

#------------------------------ Main ------------------------------#

listener = keyboard.Listener(on_press=on_press)
listener.start() 

while main:

    shapeList = copy.deepcopy([S, I, O, L, J, Z, T])
    currentShape = random.choice(shapeList)
    currentRotation = currentShape[0]


    #------------ Base Coords for Shape ------------#
    y = min(currentRotation, key=lambda ya: ya[1])[1]
    x = min(currentRotation, key=lambda xa: xa[0])[0]

    for coord in currentRotation:
        coord[0] -= x
        coord[1] -= y
    
    x = 0
    y = 0

    width = max(currentRotation, key=lambda xa: xa[0])[0]
    height = max(currentRotation, key=lambda ya: ya[1])[1]
    #----------------------------------------------#

    
    print_board(currentRotation + board_coords, board, ghost_coords)
    collisions = 0


    #------------ Every Piece ------------#
    while y < 20 - height - 1 and collisions == 0:
        start = time.time()
        period = datetime.datetime.now()

        #------------ Every x seconds ------------#
        if period.second % 1 == 0 and (period - lastTime).total_seconds() >= speed_seconds:
            collisions = 0
            for coord in currentRotation:
                if [coord[0],coord[1] + 1] in board_coords:
                    collisions += 1
            if collisions == 0:
                y += 1
                for rot in currentShape:
                    for coord in rot:
                        coord[1] += 1
            
            print_board(currentRotation + board_coords, board, ghost_coords)
            lastTime = period
        #------------------------------------#
        
        # print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.', end='\r')
        
        print(f'Speed: {speed_seconds}   |   Level: {current_level}   |   Lines: {line_clear_count}', end='\r')
        count += 1
        end_time = time.time()  
        time_lapsed = end_time - start_time
        time_convert(time_lapsed) 

        time.sleep(max(1./framelimit - (time.time() - start), 0))

    board_coords.extend(currentRotation)
    #------------------------------------#
    
        

    #------------ Clear Lines ------------#
    y_list = [s[1] for s in board_coords]
    for y in range(0,20):
        if y_list.count(y) == 10:
            line_clear_count += 1
            if line_clear_count % 2 == 0 and line_clear_count != 0:
                current_level += 1  
            board_coords = [s for s in board_coords if s[1] != y]
            for s in board_coords:
                if s[1] < y:
                    s[1] += 1
    #------------------------------------#
    speed_seconds = speed_dict[current_level]['time'] / 20


print_board(currentRotation + board_coords, board, ghost_coords)
print(currentRotation)
print(x,y)
print(width + 1, height + 1)