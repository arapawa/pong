# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
paddle1_pos = 180
paddle1_vel = 0
paddle2_pos = 180
paddle2_vel = 0
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
# score
score1 = 0
score2 = 0
# initial ball position
init_pos = [WIDTH / 2, HEIGHT / 2]
# ball position
ball_pos = [0, 0]
# ball velocity
ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, init_pos  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    init_pos = [WIDTH / 2, HEIGHT / 2]
    ball_pos = init_pos
    ball_vel[0] = random.randrange(120, 240) / 60
    ball_vel[1] = random.randrange(60, 180) / 60
    if direction == LEFT:
        ball_vel = [-ball_vel[0], ball_vel[1]]
    elif direction == RIGHT:    
        ball_vel = [ball_vel[0], ball_vel[1]]
    else:
        new_game()

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    # reset paddles
    paddle1_pos = 180
    paddle1_vel = 0
    paddle2_pos = 180
    paddle2_vel = 0
    # reset ball
    ball_vel = [0, 0]   
    # reset score
    score1 = 0
    score2 = 0
    spawn_direction = random.randrange(0, 3)
    if spawn_direction <= 1:
        spawn_ball(LEFT)
    elif spawn_direction >= 2:
        spawn_ball(RIGHT)    

# reset button    
def restart():
    new_game()

# keep paddles on canvas    
def constrain(value, lower_bound, upper_bound):
    return min(max(lower_bound, value), upper_bound)
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, time, paddle1_vel, paddle2_vel         
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")        
    # update ball
    # x position
    ball_pos[0] = init_pos[0] + ball_vel[0]
    # y position
    ball_pos[1] = init_pos[1] + ball_vel[1]    
    # wall bouncing
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    else:    
        pass
    # ball hitting paddle (and accelerating) or gutter
    # left gutter
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:    
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + 80:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] + ball_vel[0] * 0.1
            ball_vel[1] = ball_vel[1] + ball_vel[1] * 0.1
        else:
            score2 += 1
            spawn_ball(RIGHT) 
    # right gutter
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):    
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + 80:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] + ball_vel[0] * 0.1
            ball_vel[1] = ball_vel[1] + ball_vel[1] * 0.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    else:
        pass
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    paddle1_pos = constrain(paddle1_pos + paddle1_vel, 0, HEIGHT - PAD_HEIGHT)
    paddle2_pos = constrain(paddle2_pos + paddle2_vel, 0, HEIGHT - PAD_HEIGHT)    
    # draw paddles
    c.draw_line([5, paddle1_pos], [5, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, 'Blue')
    c.draw_line([595, paddle2_pos], [595, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, 'Red')        
    # draw scores
    c.draw_text(str(score1) + " " + str(score2), [284, 50], 25, "White")
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 2
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 0
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = acc  


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart)


# start frame
new_game()
frame.start()