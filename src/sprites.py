from setting import *

import pygame.sprite

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups, z, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)

        # Terrain
        self.image = surface

        # Player
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z, animation_speed=ANIMATION_SPEED):
        self.frames, self.frames_index = frames, 0
        super().__init__(pos, groups, z, self.frames[self.frames_index])
        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]

    def run(self, dt):
        self.animate(dt)
