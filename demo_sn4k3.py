import random as rd
import pyray as pr


def randomize_food_position():
    food_left = rd.randint(0,CELLCOL-1)*CELLSIZE
    food_top  = rd.randint(0,CELLROW-1)*CELLSIZE
    food_rect = (food_left,food_top,CELLSIZE,CELLSIZE)
    return food_rect

CELLSIZE = 20
CELLCOL = 32
CELLROW = 24
WINW = CELLCOL*CELLSIZE
WINH = CELLROW*CELLSIZE
pr.init_window(WINW,WINH,'demo sn4k3')
pr.set_target_fps(15)


snake_pos = [(3,10),(4,10),(5,10)]

MOVE_UP    = [ 0,-1]
MOVE_DOWN  = [ 0, 1]
MOVE_LEFT  = [-1, 0]
MOVE_RIGHT = [ 1, 0]
NOT_MOVE   = [ 0, 0]
snake_direction = NOT_MOVE

add_segment = False

food_rect = randomize_food_position()

##MAIN GAME LOOP STARTED HERE!!!
while not pr.window_should_close():
    ##make snake eat food
    food_col = food_rect[0]//CELLSIZE
    food_row = food_rect[1]//CELLSIZE
    snake_head_col, snake_head_row = snake_pos[-1]
    if snake_head_col == food_col and snake_head_row == food_row:
        ##re-spawn the food at random location on the screen
        food_rect = randomize_food_position()
        ##make snake growth one segment each time
        add_segment = True

    ######################### END GAME STATE #############################
    ##snake hits wall, you also need to check for BOTH horizontal and vertical
    if not 0 <= snake_head_col < CELLCOL or\
       not 0 <= snake_head_row < CELLROW:
        print('hits wall')
        break

    ##snake hits itself
    for body_col,body_row in snake_pos[:-1]:  ##except the head
        if snake_head_col == body_col and snake_head_row == body_row:
            print('ouch!:<')
            break


    ############################ SNAKE MOVING ############################
    if snake_direction != NOT_MOVE:
        if not add_segment:
            snake_pos.pop(0)
        else:
            ##just take the entire snake position
            add_segment = False  ##to prevent our snake keep growing
        new_col = snake_pos[-1][0] + snake_direction[0]
        new_row = snake_pos[-1][1] + snake_direction[1]
        new_head = [new_col,new_row]
        snake_pos.append(new_head)

        
    if pr.is_key_down(pr.KEY_UP):
        ##[!]NOTE that our snake CANNOT moving against its current direction
        if snake_direction != MOVE_DOWN:
            snake_direction = MOVE_UP
    elif pr.is_key_down(pr.KEY_DOWN):
        if snake_direction != MOVE_UP:
            snake_direction = MOVE_DOWN
    elif pr.is_key_down(pr.KEY_LEFT):
        if snake_direction != MOVE_RIGHT:
            snake_direction = MOVE_LEFT
    elif pr.is_key_down(pr.KEY_RIGHT):
        if snake_direction != MOVE_LEFT:
            snake_direction = MOVE_RIGHT
        
    
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    ##draw the food
    pr.draw_rectangle(*food_rect,pr.RED)

    ##draw the snake entire' body by looping through it
    for col_index,row_index in snake_pos:
        snake_rect = (col_index*CELLSIZE,  ##left
                      row_index*CELLSIZE,  ##top
                      CELLSIZE,  ##width
                      CELLSIZE)  ##height
        pr.draw_rectangle(*snake_rect,pr.GREEN)
    
    ##draw the 2d grid board
    for i in range(1,CELLROW,1):
        for j in range(1,CELLCOL,1):
            x = j*CELLSIZE
            y = i*CELLSIZE
            pr.draw_line(x,0,x,WINH,pr.BLACK)
            pr.draw_line(0,y,WINW,y,pr.BLACK)
    pr.end_drawing()
pr.close_window()
