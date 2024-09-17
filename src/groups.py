from setting import *
from data import Data

class AllSprite(pygame.sprite.Sprite):
    def __init__(self, tmx_map, level_frames, audio_files, data):
        self.surface_display = pygame.display.get_surface()
        self.data = data
        self.audio_files = audio_files

        # Level's data
        self.level_width = tmx_map.get_width() * TILE_SIZE
        self.level_height = tmx_map.get_height() * TILE_SIZE


