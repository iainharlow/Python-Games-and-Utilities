"""
Implementation of classic arcade game Pong.
Can be run in a web browser using codeskulptor.
Simply visit http://www.codeskulptor.org/, 
paste the code into the browser and enjoy 
playing and then editing the game!
"""

# Import required libraries

import simplegui
import random

# Initialize global variable
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 6
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0

# Helper functions

def distance(point_a, point_b):
    """
    Returns the Euclidean distance between two points.
    """
    return ((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)**0.5

def spawn_ball(direction):
    """
    Initialize ball_pos and ball_vel for new ball in middle of table.
    If direction is RIGHT, the ball's velocity is upper right, else upper left.
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(120, 240)/60,
                -random.randrange(60, 180)/60]
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]

# Event handlers

def new_game():
    """
    Begin a new game. Resets score, ball position.
    """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    spawn_ball(LEFT)
    paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2]
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH,HEIGHT/2]
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]
    
def draw(canvas):
    """
    Updates the canvas with the game state.
    """
    
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # Draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Handle wall impacts
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if HEIGHT - ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # Update paddle positions
    if abs(paddle1_pos[1] + paddle1_vel[1] - HEIGHT/2) + HALF_PAD_HEIGHT < HEIGHT/2:
        paddle1_pos[1] += paddle1_vel[1]
    if abs(paddle2_pos[1] + paddle2_vel[1] - HEIGHT/2) + HALF_PAD_HEIGHT < HEIGHT/2:
        paddle2_pos[1] += paddle2_vel[1]
    
    # Draw paddles
    canvas.draw_line([paddle1_pos[0],paddle1_pos[1]-HALF_PAD_HEIGHT],
                     [paddle1_pos[0],paddle1_pos[1]+HALF_PAD_HEIGHT],
                     PAD_WIDTH,
                     "White")
    canvas.draw_line([paddle2_pos[0],paddle2_pos[1]-HALF_PAD_HEIGHT],
                     [paddle2_pos[0],paddle2_pos[1]+HALF_PAD_HEIGHT],
                     PAD_WIDTH,
                     "White")
    
    # Handle paddle/ball collisions    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if distance(ball_pos,paddle1_pos) < HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1*ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if WIDTH - ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if distance(ball_pos,paddle2_pos) < HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1*ball_vel[0]
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # Draw scores
    canvas.draw_text(str(score1),[WIDTH/3-25,HEIGHT/5],50,"White",monospace)
    canvas.draw_text(str(score2),[2*WIDTH/3-25,HEIGHT/5],50,"White",monospace)
                     
def keydown(key):
    """
    Handler for paddle movement when key is pressed.
    """
    global paddle1_vel, paddle2_vel
    acc = 200/60
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc
   
def keyup(key):
    """
    Handler for paddle movement when key is released.
    """
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
