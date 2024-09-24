from setting import *
from data import Data

class AllSprite(pygame.sprite.Group):
    def __init__(self, width, height, bg_tile=None, top_limit=0):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()  # camera offset
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE

        self.borders = {
            'left': 0,
            'right': -(self.width) + WINDOW_WIDTH,
            'bottom': -(self.height) + WINDOW_HEIGHT,
            'top': top_limit
        }

    def camera_constrain(self):  # camera logic
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders[
            'left']  # camera will block when player is reaching the left side of the map
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders[
            'right']  # camera will block when player is reaching the right side of the map
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']



