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
        self.offset.x = self.offset.x if self.offset.x < float(self.borders['left']) else float(self.borders['left'])
        self.offset.x = self.offset.x if self.offset.x > float(self.borders['right']) else float(self.borders['right'])
        self.offset.y = self.offset.y if self.offset.y > float(self.borders['bottom']) else float(self.borders['bottom'])
        self.offset.y = self.offset.y if self.offset.y < float(self.borders['top']) else float(self.borders['top'])

    def draw(self, target_pos, dt):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        self.camera_constrain()

        for sprite in sorted(self, key=lambda
                sprite: int(sprite.z) if str(sprite.z).isdigit() else float('inf')): # check type sprite.z
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)


