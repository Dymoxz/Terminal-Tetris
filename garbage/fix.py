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


#set RGB values for every colour
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (0, 0, 255), (255, 127, 0), (128, 0, 128), (128, 0, 128)]
shapes = [S,O,I, J, L, T, Z]

board = [background*10]*20

# create colour for reset after printing
RESET = '\033[0m'

#------------ Variables ------------#
count = 0

x = 0
abx = 0
aby = 0
y = 0

colour_list = []
shape_list = []

time_lapsed = 0
start_time = time.time()
lastTime = datetime.datetime.now()

rotation = 0
absList = []
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
            if c == background:
                print(c + ' ', end='')
            else:
                print(get_color_escape(currentColour[0], currentColour[1], currentColour[2]) + c + RESET + ' ', end='')
        print()
    print()


#converts time
def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

#moving the shape down and deleting the old one
def gravity(board, shape):
    #shape = currentShape
    for coords in shape:
        ABSshapecoords = list(board[coords[1]])
        ABSshapecoords[coords[0]] = background
        board[coords[1]] = ''.join(ABSshapecoords)
    #move the shape down by 1 for every y coordinate in it
    for s in range(0,len(shape)):
        currentABS[s][1] += 1


def on_press(key):
    global y
    global x
    global abx
    global currentShape  
    global rotation
    global leftBound
    global aby
    #check wich key is pressed
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    
    if k in ['left', 'right', 'down', 'up']:
        #if the key is right_arrow move x by 1 if it doesnt go out of bounds
        if k == 'right':
            if x + abx < 9 - width + 1:
                x += 1
        #if the key is left_arrow move x by -1 if it doesnt go out of bounds
        if k == 'left':
            if x + abx > 0:
                x -= 1
        #if the key is down_arrow do y + 1 if it doesnt go out of bounds
        if k == 'down':
            if y + aby < 20 - height:
                y += 1
        #if the key is up_arrow do rotation + 1 but if it is the 3rd make it rotate back to 0
        if k == 'up':
            pptation = copy.deepcopy(rotation)
            pptation = pptation + 1 if rotation < 3 else 0
            currentSheap = fullShape[pptation]
            minX = min([item[0] for item in currentSheap]) + x
            maxX = max([item[0] for item in currentSheap]) + x
            minY = min([item[1] for item in currentSheap]) + y
            maxY = max([item[1] for item in currentSheap]) + y
            if minX >= 0 and maxX <= 9 and minY >= 0 and maxY <= 19:
                rotation = rotation + 1 if rotation < 3 else 0
                currentShape = fullShape[pptation]
                curLeft = min([item[0] for item in currentShape])
                abx = curLeft 
                aby = min([item[1] for item in currentShape])
                getDimenstions()
            else:
                currentShape = fullShape[rotation]
        for s in currentABS:
            aaa = list(board[s[1]])
            aaa[s[0]] = background
            board[s[1]] = ''.join(aaa)
        for s in range(0,4):
            currentABS[s][0] = currentShape[s][0] + x
            currentABS[s][1] = currentShape[s][1] + y

        # for every coord in the shape set it to the icon in this case ⯀
        for coord in currentABS:
            ABSshapecoords = list(board[coord[1]]) 
            ABSshapecoords[coord[0]] = shapeIcon
            board[coord[1]] = ''.join(ABSshapecoords)
        print_board(board)

#clears the console
def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    return _

#get the width and height of the shape
def getDimenstions():
    global width
    global height
    global rightBound
    global leftBound
    global topBound
    #get most left, right, top and bottom bound of the shape
    leftBound = min([item[0] for item in currentShape])
    rightBound = max([item[0] for item in currentShape])
    topBound = min([item[1] for item in currentShape])
    bottomBound = max([item[1] for item in currentShape])
    #set the width and height of the shape
    width = rightBound - leftBound + 1
    height = bottomBound - topBound + 1


#------------------------------ Main Game ------------------------------#

randShapes = copy.copy(shapes)
random.shuffle(randShapes)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

#main game loop
while True:

    x = 0
    abx = 0
    aby = 0
    y = 0

    clear()

    try:
        fullShape = randShapes[0]
        randShapes.pop(0)
    except:
        randShapes = copy.deepcopy(shapes)
        random.shuffle(randShapes)
        fullShape = randShapes[0]
        randShapes.pop(0)
        
    currentShape = fullShape[rotation]
    
    currentABS = copy.deepcopy(currentShape)
    fullABS = copy.deepcopy(fullShape)
    currentColour = colors[shapes.index(fullShape)]
    getDimenstions()

    print_board(board)

    x = leftBound
    aby = topBound




    #loop for the current shape
    while y + aby < 20 - height:
        start = time.time()
        period = datetime.datetime.now()
        if period.second % 1 == 0 and (period - lastTime).total_seconds() >= 0:
            #do the gravity, boom, b-b-boom b-boom b-boom!
            collisions = 0
            for xy in currentABS:
                if [xy[0],xy[1] + 1] in absList:
                    collisions += 1
            if collisions == 0:
                gravity(board, currentABS)
                lastTime = period
                for coord in currentABS:
                    aaa = list(board[coord[1]]) 
                    aaa[coord[0]] = shapeIcon
                    board[coord[1]] = ''.join(aaa)
                print_board(board)
                y += 1
            else:
                break
        try:
            print(currentABS, collisions, end='\r')
            print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.   |   Rotation: {rotation}', end='\r')
            #print(f'width: {width}  |   height: {height}    |   x: {x + abx}  |   y: {y + aby}', end='\r')
            #print(colour_list, shape_list, end='\r')
            #print(f'currentShape: {currentShape}    |   currentABS: {currentABS}    |   rotation: {rotation}', end='\r')
            #print(x + abx, y, end='\r')
            #print(currentABS, f'x= {x}, y= {y}', end='\r')
        except:
            pass
        count += 1
        end_time = time.time()
        time_lapsed = end_time - start_time
        time_convert(time_lapsed)   
        
        try:
            if colour_list[-1] != currentColour:
                shape_list.append(currentABS)
                colour_list.append(currentColour)
        except:
            shape_list.append(currentABS)
            colour_list.append(currentColour)
        #limit to 60 fps instead of 20.000 fps
        time.sleep(max(1./60 - (time.time() - start), 0))

    absList.extend(currentABS)



listener.stop()

clear()
print_board(board)
print('\n\n')
print(f'FPS: {round(count/time_lapsed, 2)}   |   Frames: {count}   |   Time: {round(time_lapsed, 3)} Sec.   |   Rotation: {rotation}')
print(f'X: {x + abx}   |   Y: {y + aby}')
print(f'rotation: {rotation}')
print('\n\n')