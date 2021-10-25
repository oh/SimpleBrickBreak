"""
    Project name: SimpleBrickBreak
    File name: main.py
    Author: Hunter Webb
    Date created: 10/18/2021
    Date last modified: 10/24/2021
    Python Version: 3.9.5
"""

# Module Imports

import random
import pygame
import sys
from pygame.locals import *
from pygame import gfxdraw

# Constants

GAME_OVER = 0

SOLID = 0
SINGLE = 1
DOUBLE = 2
TRAIL = 3
EXTRA_LIFE = 4

COLORS = [
    pygame.Color("#272727"),  # 0 SOLID
    pygame.Color("#28AFB0"),  # 1 SINGLE
    pygame.Color("#A11692"),  # 2 DOUBLE
    pygame.Color("#FF4F79"),  # 3 TRAIL / +1 BALL
    pygame.Color("#5CF64A"),  # 4 EXTRA_LIFE
    pygame.Color("#E4FF1A"),  # 5 BALL
    pygame.Color("#F1FFE7")   # 6 PADDLE
]

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

PADDING = 1

PADDLE_WIDTH = 100
BALL_R = 10
BRICK_W = 80
BRICK_H = 30
N_BRICK_W = SCREEN_WIDTH / (BRICK_W + PADDING)
N_BRICK_H = (SCREEN_HEIGHT / 3) / (BRICK_H + PADDING)

# Movement Initializers

SPEED = 2
L_DOWN = False
R_DOWN = False


# Classes

class Paddle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.rect = pygame.Rect(int(self.x), int(self.y), PADDLE_WIDTH, 10)
        pygame.gfxdraw.box(screen, self.rect, COLORS[6])

    def move(self, d):
        if d and self.x > 0:
            self.x -= SPEED
        if not d and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += SPEED


class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.randint(-5, 5) / 10
        self.vy = 10 / SPEED

    def draw(self):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), BALL_R, COLORS[5])

    def update(self):
        global GAME_OVER

        # Bottom of the screen

        if self.y >= SCREEN_HEIGHT - BALL_R:
            GAME_OVER = 1

        # All other walls

        if not BALL_R < int(self.x) < SCREEN_WIDTH - BALL_R:
            self.vx *= -1
        if not BALL_R < int(self.y) < SCREEN_HEIGHT - BALL_R:
            self.vy *= -1

        # Paddle Collision

        if paddle.rect.collidepoint(ball.x, ball.y + BALL_R):
            self.vy *= -1

            if L_DOWN:
                if self.vx >= 0:
                    self.vx -= 0.1
                else:
                    self.vx -= 0.1
            if R_DOWN:
                if self.vx <= 0:
                    self.vx += 0.1
                else:
                    self.vx += 0.1

            if self.vx > 1:
                self.vx = 1
            if self.vx < -1:
                self.vx = -1

        self.y += self.vy / SPEED
        self.x += self.vx / SPEED

        self.draw()


class Brick(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = COLORS[type]
        self.rect = pygame.Rect(self.x, self.y, BRICK_W, BRICK_H)

    def draw(self):
        pygame.gfxdraw.box(screen, self.rect, self.color)

    def update(self):

        # Brick Collision

        if self.rect.collidepoint(ball.x, ball.y - BALL_R) or self.rect.collidepoint(ball.x, ball.y + BALL_R):
            ball.vy *= -1
            brick_array.remove(self)
            pass
        if self.rect.collidepoint(ball.x - BALL_R, ball.y) or self.rect.collidepoint(ball.x + BALL_R, ball.y):
            ball.vx *= -1
            brick_array.remove(self)

        if len(brick_array) == 0:
            print('none left')

        self.draw()


# Game Initialization

pygame.init()
pygame.display.set_caption("Simple Brick Break")
pygame.font.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
paddle = Paddle((SCREEN_WIDTH - PADDLE_WIDTH) / 2, SCREEN_HEIGHT - 50)
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
brick_array = []
pygame.display.update()

for x in range(int(N_BRICK_W) + 1):
    for y in range(int(N_BRICK_H)):
        brick_array.append(Brick(x * (BRICK_W + PADDING), y * (BRICK_H + PADDING), SINGLE))


# Game Loop

def move():
    if L_DOWN:
        paddle.move(True)
    elif R_DOWN:
        paddle.move(False)


while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                L_DOWN = True
            elif event.key == K_RIGHT:
                R_DOWN = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                L_DOWN = False
            elif event.key == K_RIGHT:
                R_DOWN = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(0)

    if GAME_OVER:
        font = pygame.font.SysFont('arial black', 55)
        text = font.render("GAME OVER!", True, pygame.Color("RED"))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
    else:
        move()
        paddle.draw()
        ball.update()
        for brick in brick_array:
            brick.update()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
