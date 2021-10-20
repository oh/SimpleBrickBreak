"""
    Project name: SimpleBrickBreak
    File name: main.py
    Author: Hunter Webb
    Date created: 10/18/2021
    Date last modified: 10/18/2021
    Python Version: 3.9.5
"""


# Module Imports

import random
import os
import pygame
import sys
from pygame.locals import *


# Constants

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
BALL_R = 10
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
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(int(self.x), int(self.y), PADDLE_WIDTH, 10))

    def move(self, d):
        if d and self.x > 0:
            self.x -= 1 / SPEED
        if not d and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += 1 / SPEED


class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.randint(-5, 5) / 10
        self.vy = 3/SPEED

    def draw(self):
        pygame.draw.circle(screen, (155, 155, 255), (int(self.x), int(self.y)), BALL_R)

    def update(self):
        # self.print_info()

        if self.y >= SCREEN_HEIGHT - BALL_R:
            pygame.quit()
            sys.exit()

        if not BALL_R < int(self.x) < SCREEN_WIDTH - BALL_R:
            self.vx *= -1
        if not BALL_R < int(self.y) < SCREEN_HEIGHT - BALL_R:
            self.vy *= -1

        self.y += self.vy / SPEED
        self.x += self.vx / SPEED

        self.draw()

    def print_info(self):
        print("x: " + str(self.x), "\ny: " + str(self.y), "\nvx: " + str(self.vx), "\nvy: " + str(self.vy) + "\n" * 20)


# Game Initialization

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
paddle = Paddle((SCREEN_WIDTH - PADDLE_WIDTH) / 2, SCREEN_HEIGHT - PADDING * 10)
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


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

    move()

    screen.fill(0)
    paddle.draw()
    ball.update()
    pygame.display.flip()
