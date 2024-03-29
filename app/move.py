import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

UNOCCUPIED = 1
OCCUPIED   = -1
FOOD       = 25
HEAD       = -5
TAIL       = 4
HEALTHLIM = 25
game_state = ""
directions = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

# Figure out what to do next
def calculate_move(board_matrix, game_state):
    set_game_state(game_state) # Get the game state
    height = game_state["board"]["height"] # Define the size of the board
    head = game_state['you']["body"][0] # Find your head
    x = head["x"] # Head X coord
    y = head["y"] # Head Y coord
    print("Head:", x, y) # Print out to log
    health = game_state['you']["health"] # Get current health (turns since last food)

    # if game_state["turn"] < 4 :
        #if game_state["turn"] == 0 :
            #directions["up"] = 500
            #print("TURN init: ", game_state["turn"])
        #elif game_state["turn"] == 1 :
            #directions["right"] = 500
            #print("TURN init: ", game_state["turn"])
        #elif game_state["turn"] == 2 :
            #directions["down"] = 500
            #print("TURN init: ", game_state["turn"])
        #elif game_state["turn"] == 3 :
            #directions["left"] = 500
            #print("TURN init: ", game_state["turn"])

    # Check up
    if head["y"] - 1 < 0 or board_matrix[y-1][x] == OCCUPIED : 
        directions["up"] = -1000 # Heavily downweights moves if the square is occupied
        print("UP OCCUPIED")
    elif board_matrix[y-2][x]== OCCUPIED :
        directions["up"] = -10
        print("UP2 OCCUPIED")
    else:
        directions["up"] = sum(board_matrix, head["x"], head["y"] - 1, height, game_state)


    # Check down
    if head["y"] + 1 > (height - 1) or board_matrix[y+1][x] == OCCUPIED :
        directions["down"] = -1000
        print("DN OCCUPIED")
    elif head["y"] + 1 > (height - 2) or board_matrix[y+2][x]== OCCUPIED :
        directions["down"] = -10
        print("DN2 OCCUPIED")
    else:
        directions["down"] = sum(board_matrix, head["x"], head["y"] + 1, height, game_state)


    # Check Left
    if head["x"] - 1 < 0 or board_matrix[y][x-1] == OCCUPIED :
        directions["left"] = -1000
        print("L OCCUPIED")
    elif board_matrix[y][x-2]== OCCUPIED :
        directions["left"] = -10
        print("L2 OCCUPIED")
    else:
        directions["left"] = sum(board_matrix, head["x"] - 1, head["y"], height, game_state)


    # check right
    if head["x"] + 1 > (height - 1) or board_matrix[y][x+1]== OCCUPIED :
        directions["right"] = -1000
        print("R OCCUPIED")
    elif head["x"] + 1 > (height - 2) or board_matrix[y][x+2]== OCCUPIED :
        directions["right"] = -10
        print("R2 OCCUPIED")
    else:
        directions["right"] = sum(board_matrix, head["x"] + 1, head["y"], height, game_state)
	
    # check up-right
#    if board_matrix[y-1][x+1] == OCCUPIED and board_matrix[y-1][x] == OCCUPIED :
#        directions["up"] = -2
#        directions["right"] = -1
#        print("U-r OCCUPIED")
#    elif board_matrix[y-1][x+1] == OCCUPIED and board_matrix[y][x+1]== OCCUPIED :
#        directions["up"] = -1
#        directions["right"] = -2
#        print("u-R OCCUPIED")

    # check up-left
#    if board_matrix[y-1][x-1] == OCCUPIED and board_matrix[y-1][x] == OCCUPIED :
#        directions["up"] = -2
#        directions["left"] = -1
#        print("U-l OCCUPIED")
#    elif board_matrix[y-1][x-1] == OCCUPIED and board_matrix[y][x-1] == OCCUPIED :
#        directions["up"] = -1
#        directions["left"] = -2
#        print("u-L OCCUPIED")

    # check down-left
#    if board_matrix[y+1][x-1] == OCCUPIED and board_matrix[y+1][x] == OCCUPIED :
#        directions["down"] = -2
#        directions["left"] = -1
#        print("D-l OCCUPIED")
#    elif board_matrix[y+1][x-1] == OCCUPIED and board_matrix[y][x-1] == OCCUPIED :
#        directions["down"] = -1
#        directions["left"] = -2
#        print("d-L OCCUPIED")

    # check down-right
#    if board_matrix[y+1][x+1] == OCCUPIED and board_matrix[y+1][x] == OCCUPIED :
#        directions["down"] = -2
#        directions["right"] = -1
#        print("D-r OCCUPIED")
#    elif board_matrix[y+1][x+1] == OCCUPIED and board_matrix[y][x+1]== OCCUPIED :
#        directions["down"] = -1
#        directions["right"] = -2
#        print("d-R OCCUPIED")

    if( health < HEALTHLIM and len(game_state['board']['food'])>0):
        find_food(game_state, board_matrix)
        print("HUNGRY!")

    print(max(directions, key=lambda k: directions[k]))
    quad(board_matrix, game_state)
    print("UP", directions["up"])
    print("DOWN", directions["down"])
    print("LEFT", directions["left"])
    print("RIGHT", directions["right"])
    return max(directions, key=lambda k: directions[k])


def sum(matrix, x, y, height, gamestate):
    sum = 0
    if matrix[y][x] == HEAD:
        snek = get_snek(x, y , game_state)
        if is_bigger(snek, gamestate):
            sum += 1000
        else:
            sum += -100
            print(snek)

    if (x - 1) >= 0:
        sum += matrix[y][x-1]
        if matrix[y][x-1] == HEAD :
            snek = get_snek(x-1, y, game_state)
            if is_bigger(snek, gamestate):
                sum += 1000
            else:
                sum += -100
                print(snek)

    if (x + 1) < height:
        sum += matrix[y][x+1]
        if matrix[y][x+1] == HEAD :
            snek = get_snek(x+1, y, game_state)
            if(is_bigger(snek, gamestate)):
                sum += 1000
            else:
                sum += -100
                print(snek)

    if (y - 1) >= 0:
        sum += matrix[y-1][x]
        if matrix[y-1][x] == HEAD :
            snek = get_snek(x, y-1, game_state)
            if is_bigger(snek, gamestate):
                sum += 1000
            else:
                sum += -100
                print(snek)

    if (y + 1) < height:
        sum += matrix[y+1][x]
        if matrix[y+1][x] == HEAD :
            snek = get_snek(x, y+1, game_state)
            if is_bigger(snek, gamestate):
                sum += 1000
            else:
                sum += -100
                print(snek)

    if (x-1) >= 0 and (y+1) < height:
        sum += matrix[y+1][x-1]

    if (x-1) >= 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    if (x+1)< height and (y+1) < height:
        sum += matrix[y+1][x+1]

    if (x-1) > 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    return sum + matrix[y][x]


def find_food(game_state, board_matrix ):
    minsum = 1000
    y = game_state['you']["body"][0]["y"]
    x = game_state['you']["body"][0]["x"]

    for food in game_state["board"]["food"]:
        tot = abs(food['x'] - x)
        tot += abs(food['y'] - y)
        if (tot < minsum):
            goodfood = food
            minsum = tot

    find_path(game_state, board_matrix,x,y, goodfood["x"], goodfood['y'])
    print("Found food ", goodfood["x"], goodfood['y'])



def find_path(game_state, board_matrix, x, y, foodx, foody):
    height = game_state["board"]["height"]
    grid = Grid(width=height, height=height, matrix=board_matrix)
    start = grid.node(x, y)
    end = grid.node(foodx, foody)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    if (len(path) > 0):
        pathx = path[1][0]
        pathy = path[1][1]

        y = game_state['you']["body"][0]["y"]
        x = game_state['you']["body"][0]["x"]
        # go up
        if ((y - 1) == pathy) and (x == pathx):
            directions["up"] += 20
            print("Pick: UP")
        # go down
        if ((y + 1) == pathy) and (x == pathx):
            directions["down"] += 20
            print("Pick: down")
        # go left
        if ((x - 1) == pathx) and (y == pathy):
            directions["left"] += 20
            print("Pick: left")
        # go right
        if ((x + 1) == pathx) and (y == pathy):
            directions["right"] += 20
            print("Pick: right")


def quad(matrix, game_state):
    x =game_state["you"]["body"][0]["x"]
    y = game_state["you"]["body"][0]["y"]
    height = game_state['board']['height']
    quad1 = 0
    quad2 = 0
    quad3 = 0
    quad4 = 0
    for i in range(y):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad1 += 1
            if(matrix[j][i]== FOOD):
                quad1 += 5

    for i in range(y):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad2 += 1
            if(matrix[j][i]== FOOD):
                quad2 += 5
                
    for i in range(y, height):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad3 += 1
            if(matrix[j][i]== FOOD):
                quad3 += 5

    for i in range(y, height):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad4 += 1
            if(matrix[j][i]== FOOD):
                quad4 += 5

    directions['up'] += (quad1 + quad2)/height
    directions['down'] += (quad3 + quad4)/height
    directions['left'] += (quad1 + quad3)/height
    directions['right'] += (quad2 + quad4)/height
    print(quad1, quad2, quad3, quad4)

def is_bigger(snek, game):
    if len(game["you"]["body"]) > snek + 1:
        print("length**************")

        return True
    print("Snake length", snek, "our length ", len(game['you']['body']))
    return False

def get_snek(x, y, game_state):
    for snek in game_state["board"]["snakes"]:
        snake_body = snek['body']
        for xy in snake_body[0:]:
            if( xy["y"]== y and xy["x"]==x):
                return len(snake_body)


def set_game_state(new_game_state):
    global game_state
    game_state = new_game_state


def get_game_State():
    return game_state
