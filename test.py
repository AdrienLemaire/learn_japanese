#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *


SPEED = 10
STATE = {
    "moving": lambda: define_keys(0),
    "talking": lambda: define_keys(1),
}
WORLD_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
CHOICES = ["おはよございます", "こんいちは"]
CHOICE = 0
ARROW = "▶"


def move_in_game(key):
    global player_pos
    if event.key == K_LEFT:
        player_pos = player_pos.move(-pixel_size[0], 0)
    elif event.key == K_RIGHT:
        player_pos = player_pos.move(pixel_size[0], 0)
    elif event.key == K_UP:
        player_pos = player_pos.move(0, -pixel_size[1])
    elif event.key == K_DOWN:
        player_pos = player_pos.move(0, pixel_size[1])


def move_in_window(key):
    global CHOICE, CHOICES

    if event.key == K_UP:
        CHOICE = (CHOICE + 1) % len(CHOICES)
    elif event.key == K_DOWN:
        CHOICE = (CHOICE - 1) % len(CHOICES)


def to_pixel(coords):
    return coords[0] * pixel_size[0], coords[1] * pixel_size[1]


def from_pixel(coords):
    return int(coords[0] / pixel_size[0]), int(coords[1] / pixel_size[1])


def make_wall():
    for i, line in enumerate(WORLD_MAP):
        for j, col in enumerate(line):
            window.blit(col and wall or grass, to_pixel((j, i)))


def get_empty_pos():
    import random
    x = random.randint(0, len(WORLD_MAP) -1 )
    y = random.randint(0, len(WORLD_MAP[0]) -1)
    if WORLD_MAP[x][y]:
        return get_empty_pos()
    return (y, x)


def draw_speaking_window():
    speaking_window_size =  (world_size[0], world_size[1]/4)
    speaking_window = pygame.Surface(speaking_window_size)
    speaking_window.fill((255,)*4)
    window.blit(speaking_window, (0, 3*(world_size[1]/4)))

    text_to_draw = default_font.render("=", True, (0,)*4)
    text_coords = text_to_draw.get_size()
    for i in range(0, int(speaking_window_size[0] / text_coords[0]) - 2):
        window.blit(
            text_to_draw,
            (text_coords[0] * (i + 1), 3*(world_size[1]/4))
        )
        window.blit(
            text_to_draw,
            (text_coords[0] * (i + 1), world_size[1] - text_coords[1])
        )
    text_to_draw = default_font.render("║", True, (0,)*4)
    text_coords = text_to_draw.get_size()
    for i in range(0, int(speaking_window_size[1] / text_coords[1]) - 2):
        window.blit(
            text_to_draw,
            (0, 3*(world_size[1]/4) + (i + 1)* text_coords[1]))
        window.blit(
            text_to_draw,
            (world_size[0] - text_coords[0],
            3*(world_size[1]/4) + (i + 1)* text_coords[1])
        )
    text_to_draw = default_font.render("╔", True, (0,)*4)
    window.blit(text_to_draw, (0, 3*(world_size[1]/4 )))
    text_to_draw = default_font.render("╗", True, (0,)*4)
    window.blit(
        text_to_draw,
        (world_size[0] - text_coords[0], 3*(world_size[1]/4 ))
    )
    text_to_draw = default_font.render("╚", True, (0,)*4)
    window.blit(text_to_draw, (0, world_size[1] - text_coords[1] ))
    text_to_draw = default_font.render("╝", True, (0,)*4)
    window.blit(
        text_to_draw,
        (world_size[0] - text_coords[0], world_size[1] - text_coords[1] )
    )

    for i, c in enumerate(CHOICES):
        if CHOICE == i:
            arrow_parlant = default_font.render(ARROW, True, (0,)*4)
            window.blit(
                arrow_parlant,
                (text_coords[0]*3,
                 3*(world_size[1]/4) + text_coords[1]*(2 + i * 1.4))
            )
        text_to_draw = default_font.render(c, True, (0,)*4)
        window.blit(
            text_to_draw,
            (text_coords[0]*5,
             3*(world_size[1]/4) + text_coords[1]*(2 + i * 1.4))
        )


def check_collision():
    if WORLD_MAP[int(player_pos[1] / pixel_size[1])][int(player_pos[0] /
                                                         pixel_size[0])]:
        return True


def speaking_pos(position):
    return [(position[0], position[1]-1)]


# Initialization
pygame.init()
default_font = pygame.font.SysFont(pygame.font.get_fonts()[0], 12)

# New window
window = pygame.display.set_mode((0, 0) , RESIZABLE)

wall = pygame.image.load("wall.bmp").convert()
pixel_size = wall.get_size()
world_size = to_pixel((len(WORLD_MAP[0]), len(WORLD_MAP)))

# New window
window = pygame.display.set_mode(world_size , RESIZABLE)

# Background
grass = pygame.image.load("background.bmp").convert()

make_wall()
# Players
player = pygame.image.load("hero.bmp").convert_alpha()
player_state = "moving"
vilain = pygame.image.load("vilain.bmp").convert_alpha()

# Get its position
player_pos = player.get_rect()
window.blit(player, player_pos)
vilain_pos = get_empty_pos()
WORLD_MAP[vilain_pos[1]][vilain_pos[0]] = 1
window.blit(vilain, to_pixel(vilain_pos))

# Enable to move player while keeping the key pressed
pygame.key.set_repeat(400, 30)

# Display the window
pygame.display.flip()
player_pos = player_pos.move(pixel_size[0], pixel_size[1])



next = 1
while next:
    for event in pygame.event.get():
        if event.type == QUIT:
            next = 0
        elif event.type == KEYDOWN:
            old_position = player_pos
            if event.key == K_SPACE:
                print("Space")
            elif event.key == K_RETURN:
                print ("CHOICE: %s" % CHOICES[CHOICE])
            elif event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                if from_pixel(player_pos) in speaking_pos(vilain_pos):
                    move_in_window(event.key)
                else:
                    move_in_game(event.key)

            if check_collision():
                player_pos = old_position

    make_wall()
    window.blit(player, player_pos)
    window.blit(vilain, to_pixel(vilain_pos))
    if from_pixel(player_pos) in speaking_pos(vilain_pos):
        draw_speaking_window()
    pygame.display.flip()
