#-*- coding:utf-8 -*-

# from python
import random
from functools import reduce

# from pygame
import pygame
from pygame.locals import *


SPEED = 10
STATE = {
    "moving": lambda: define_keys(0),
    "talking": lambda: define_keys(1),
}
ARROW = "▶"
DEFAULT_WALL = "images/wall.bmp"
DEFAULT_GROUND = "images/background.bmp"


class Slot():
    """Size of a slot, eg a wall"""

    def __init__(self, picture):
        self.picture = pygame.image.load(picture).convert()
        self.size = self.picture.get_size()

    def __repr__(self):
        return self.picture


class Text():

    def __init__(self, text):
        self.default_font = pygame.font.SysFont(pygame.font.get_fonts()[0], 12)
        self.text = text
        self.text_to_draw = self.default_font.render(self.text, True, (0,)*4)
        self.size = self.text_to_draw.get_size()


class Message():

    def __init__(self, question, answers, coords, width, height):
        self.default_font = pygame.font.SysFont(pygame.font.get_fonts()[0], 12)
        self.question = Text(question)
        self.answers = [Text(answer) for answer in answers]
        self.coords = coords
        self.height = height

    def draw(self, window):
        # First the question
        coord_qx = self.coords[0] + self.question.size[0] * 5
        coord_qy = self.coords[1] + self.height * .25
        window.blit(self.question.text_to_draw, (coord_qx, coord_qy))
        # Then the answers
        coord_ax = self.coords[0] + self.question.size[0] * 10
        coord_ay = self.coords[1] + self.height * .5
        for i, answer in enumerate(self.answers):
            window.blit(
                answer.text_to_draw,
                (coord_ax, coord_ay + i * self.question.size[1]),
            )


class MessageBox():
    """Window for displaying the text"""

    def __init__(self, world_size, window):
        self.x = world_size[0]
        self.y = world_size[1] * 0.75
        self.window = window
        self.coords = (self.x, self.y)
        self.width = world_size[0]
        self.height = world_size[1]
        self.default_font = pygame.font.SysFont(pygame.font.get_fonts()[0], 12)
        self.messages = []
        self.surface = pygame.Surface(self.coords)
        self.surface.fill((255,)*4)
        self.choice = 1

    def set_message(self, question, answers):
        self.messages.append(
            Message(question, answers, self.coords, self.width, self.height)
        )

    def keys(self, key):
        """Event keys available in talking mode"""

        if key == K_UP:
            self.choice = (self.choice + 1) % len(self.messages[0].answers)
        elif key == K_DOWN:
            self.choice = (self.choice - 1) % len(self.messages[0].answers)
        elif key == K_RETURN:
            print ("choice: %s" % self.messages[0].answers[choice])


    def draw_border(self):
        # Top and bottom lines
        char_to_draw = self.default_font.render("=", True, (0, ) * 4)
        text_coords = char_to_draw.get_size()
        for i in range(0, int(self.x / text_coords[0]) - 2):
            self.window.blit(
                char_to_draw,
                (text_coords[0] * (i + 1), 3 * (self.y / 4))
            )
            self.window.blit(
                char_to_draw,
                (text_coords[0] * (i + 1), self.y - text_coords[1])
            )
        # Right and Left lines
        char_to_draw = self.default_font.render("║", True, (0, ) * 4)
        text_coords = char_to_draw.get_size()
        for i in range(0, int(self.x / text_coords[1]) - 2):
            self.window.blit(
                char_to_draw,
                (0, 3 * (self.y / 4) + (i + 1) * text_coords[1]))
            self.window.blit(
                char_to_draw,
                (self.x - text_coords[0],
                3 * (self.y / 4) + (i + 1) * text_coords[1])
            )
        # Corners
        char_to_draw = self.default_font.render("╔", True, (0, ) * 4)
        self.window.blit(char_to_draw, (0, 3 * (self.y / 4 )))
        char_to_draw = self.default_font.render("╗", True, (0, ) * 4)
        self.window.blit(
            char_to_draw,
            (self.x - text_coords[0], 3 * (self.y / 4 ))
        )
        char_to_draw = self.default_font.render("╚", True, (0, ) * 4)
        self.window.blit(char_to_draw, (0, self.y - text_coords[1] ))
        char_to_draw = self.default_font.render("╝", True, (0, ) * 4)
        self.window.blit(
            char_to_draw,
            (self.x - text_coords[0], self.y - text_coords[1] )
        )

    def draw(self):
        print("beginning of drawing")
        self.draw_border()
        self.draw_speaking_window()
        [message.draw(self.window) for message in self.messages]

    def draw_speaking_window(self):
        for i, message in enumerate(self.messages[0].answers):
            if self.choice == i:
                speaking_arrow = self.default_font.render(ARROW, True, (0, ) * 4)
                print("%d,%d" % (message.size[0] * 3,  3 * (self.y / 4) +
                                 message.size[1] * (2 + i * 1.4)))
                print(self.window)
                print(dir(self.window))
                self.window.blit(
                    speaking_arrow,
                    (message.size[0] * 3,
                     3 * (self.y / 4) + message.size[1] * (2 + i * 1.4))
                )
            text_to_draw = self.default_font.render(message.text, True, (0, ) * 4)
            self.window.blit(
                text_to_draw,
                (message.size[0] * 5,
                 3 * (self.y / 4) + message.size[1] * (2 + i * 1.4))
            )


class Player():
    """Initialize a new player"""

    def __init__(self, name, picture, position=None):
        self.name = name
        self.image = pygame.image.load(picture).convert_alpha()
        self.position = self.image.get_rect(topleft=position)
        self.previous_pos = self.position
        self.size = self.image.get_size()

    def draw(self, window):
        window.blit(self.image, self.position)

    def move(self, key):
        """Event keys available in moving mode"""
        if key == K_LEFT:
            self.position = self.position.move(-self.size[0], 0)
        elif key == K_RIGHT:
            self.position = self.position.move(self.size[0], 0)
        elif key == K_UP:
            self.position = self.position.move(0, -self.size[1])
        elif key == K_DOWN:
            self.position = self.position.move(0, self.size[1])

    def get_position(self):
        return self.position

    def set_previous_pos(self, previous_pos):
        self.previous_pos = previous_pos

    def speaking_pos(self):
        """ Return a list of slots next to a player"""
        return [
            (self.position[0], self.position[1] - self.size[1]),
            (self.position[0], self.position[1] + self.size[1]),
            (self.position[0] - self.size[0], self.position[1]),
            (self.position[0] + self.size[0], self.position[1]),
        ]


class World():
    """The board"""
    the_map = [
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
    players = {}

    def __init__(self, window, wall=None, ground=None):
        self.wall = Slot(wall or DEFAULT_WALL)
        self.ground = Slot(ground or DEFAULT_GROUND)
        self.size = self.to_pixel((len(self.the_map[0]), len(self.the_map)))
        self.set_window(window)
        self.messageBox = MessageBox(self.size, self.window)

    def to_pixel(self, coords):
        return coords[0] * self.wall.size[0], coords[1] * self.wall.size[1]

    def from_pixel(self, coords):
        x = int(coords[0] / self.wall.size[0])
        y = int(coords[1] / self.wall.size[1])
        return x, y

    def set_window(self, window):
        print("window size : (%d, %d)"% (self.size[0], self.size[1]))
        self.window = pygame.display.set_mode(self.size)

    def get_map(self):
        return self.the_map

    def add_player(self, name=None, position=None):
        """Create a new player in this world"""
        picture = "images/hero.bmp"
        if not name:
            """We give a name and a random position to the computer"""
            name = "ai%d" % len(self.players)
            position = self.get_empty_pos()
            picture = "images/vilain.bmp"
        self.players[name] = Player(name, picture, self.to_pixel(position))

    def get_player(self, name):
        return self.players[name]

    def check_collision(self, player):
        """Return True if the slot is not empty"""
        slot_x = int(player.get_position()[1] / self.wall.size[1])
        slot_y = int(player.get_position()[0] / self.wall.size[0])
        return self.the_map[slot_x][slot_y]

    def draw_wall(self):
        for i, line in enumerate(self.get_map()):
            for j, col in enumerate(line):
                self.window.blit(
                    col and self.wall.picture or self.ground.picture,
                    self.to_pixel((j, i))
                )

    def draw(self):
        self.draw_wall()
        for player in self.players.values():
            player.draw(self.window)
            old_coords = self.from_pixel(player.previous_pos)
            self.the_map[old_coords[1]][old_coords[0]] = 0
            new_coords = self.from_pixel(player.get_position())
            self.the_map[new_coords[1]][new_coords[0]] = 1


    def get_empty_pos(self):
        """Look for an empty slot to display the vilain"""
        x = random.randint(0, len(self.the_map) -1 )
        y = random.randint(0, len(self.the_map[1]) -1)
        if self.the_map[x][y]:
            return self.get_empty_pos()
        return (y, x)

    def get_talking_pos(self, hero):
        return [player.speaking_pos() for player in
                self.players.values() if player != hero]


def main():
    # Initialization
    pygame.init()

    # Empty window
    global_window = pygame.display.set_mode((0, 0))

    world = World(global_window)

    world.messageBox.set_message(
        "ありがとう",
        ["おはよございます", "こんいちは"],
    )
    # Players
    player_state = "moving"
    world.add_player("player_name", (9, 8))
    world.add_player()
    world.add_player()

    # Enable to move player while keeping the key pressed
    pygame.key.set_repeat(400, 30)

    world.draw()
    # Display the window
    pygame.display.flip()
    #player_pos = player_pos.move(self.wall.size[0], self.wall.size[1])

    next = 1
    while next:
        world.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                next = 0
            elif event.type == KEYDOWN:
                player = world.get_player("player_name")
                player.set_previous_pos(player.get_position())
                if event.key == K_SPACE:
                    print("Space")
                elif event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN):
                    tuple_pos = (
                        player.get_position()[0],
                        player.get_position()[1],
                    )
                    if tuple_pos in reduce(list.__add__,
                            world.get_talking_pos(player)):
                        world.messageBox.draw()
                        world.messageBox.keys(event.key)
                    else:
                        player.move(event.key)

                if world.check_collision(player):
                    player.position = player.previous_pos

        #make_wall()
        #global_window.blit(player, player_pos)
        #global_window.blit(vilain, to_pixel(vilain_pos))
        #if from_pixel(player_pos) in speaking_pos(vilain_pos):
            #draw_speaking_window()
        pygame.display.flip()


if __name__ == "__main__":
    """We execute the program"""
    main()
