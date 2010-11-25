import pygame
from pygame.locals import *


# Initialization
pygame.init()

# New window
window = pygame.display.set_mode((640, 480), RESIZABLE)

background = pygame.image.load("background.jpg").convert()
window.blit(window, (0, 0))
pygame.display.flip()

next = 1
while next:
    next = int(input())
