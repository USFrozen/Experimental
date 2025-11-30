# All module imports go here for organization
# NOTE: pygame = PyGame-CE not original pygame due to use of floating point rectangles
import pygame
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
import pytmx
import sys
import os

# Pygame-CE settings
WINDOW_WIDTH, WINDOW_HEIGHT = 720, 720
#WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
BACKGROUND_COLOR = pygame.Color('black')

# PyTMX settings
TILE_SIZE = 16
base_dir = os.path.dirname(__file__) # Gets current directory
# Using os.path to point to assets so this hopefully wont break when not on Linux
world = os.path.join(base_dir, 'assets', 'TMX', 'world.tmx')
player_house = os.path.join(base_dir, 'assets', 'TMX', 'player_house.tmx')

# Animation settings
characters = os.path.join(base_dir, 'assets', 'PNG', 'characters')
tile_width = 24
tile_height = 24
ANIMATION_SPEED = 10
player_sprite = "Character_018"

# Fonts
dialogue_font = os.path.join(base_dir, 'assets', 'FONTS', 'NeatpixelsMinimal.ttf')
dialogue_font_size = 10
TEXT_SPEED = 30

# Sprite layer draw order
WORLD_DRAW_ORDER = {
    'bg': 0,
    'decoration':1,
    'main': 2,
    'fg': 3
}