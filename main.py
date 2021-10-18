"""
    Project name: SimpleBrickBreak
    File name: main.py
    Author: Hunter Webb
    Date created: 10/18/2021
    Date last modified: 10/18/2021
    Python Version: 3.9.5
"""

# Module Imports
import math

import pygame
import sys
from pygame.locals import *

# Constants

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDING = 5

# Movement Initializers

SPEED = 10
L_DOWN = False
R_DOWN = False


# Classes

class Paddle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(math.floor(self.x), math.floor(self.y), PADDLE_WIDTH, 10))

    def move(self, d):
        if d and self.x > 0:
            self.x -= 1 / SPEED
        if not d and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += 1 / SPEED


# Game Initialization

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
paddle = Paddle((SCREEN_WIDTH - PADDLE_WIDTH) / 2, SCREEN_HEIGHT - PADDING * 10)


# Game Loop

def move_left():
    paddle.move(True)


def move_right():
    paddle.move(False)


def check_movement():
    if L_DOWN:
        move_left()
    elif R_DOWN:
        move_right()


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

    check_movement()

    screen.fill(0)
    paddle.draw()
    pygame.display.flip()
