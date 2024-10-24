import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768
TILE_SIZE = 64
ANIMATION_SPEED = 1

Z_LAYERS = {
    'bg': 0,       # Lớp nền
    'clouds': 1,   # Lớp mây
    'bg tiles': 2, # Lớp các ô nền
    'path': 3,     # Lớp đường đi
    'bg details': 4, # Lớp chi tiết nền
    'main': 5,     # Lớp chính
    'water': 6,    # Lớp nước
    'fg': 7,       # Lớp tiền cảnh
}
