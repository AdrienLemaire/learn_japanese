###########
##########
#########-*- coding:utf-8 -*-

import pygame
from pygame.locals import *


# Initialization
pygame.init()

# New window
window = pygame.display.set_mode((640, 480), RESIZABLE)

background = pygame.image.load("background.bmp").convert()
window.blit(background, (0, 0))
pygame.display.flip()

next = 1
while next:
    for event in pygame.event.get():
        if event.type == QUIT:
            next = 0
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                print("Space")
            if event.key == K_RETURN:
                print("Enter")
