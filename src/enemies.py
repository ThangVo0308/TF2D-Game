import pygame.sprite

from setting import *
from random import choice
from timer import Timer

class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, health):
        super().__init__(groups)
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200
        self.health = health

        self.hit_timer = Timer(250)

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()
        # animation
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # movement
        self.rect.x += self.direction * self.speed * dt

        # reverse direction
        floor_rect_right = pygame.Rect(self.rect.bottomright, (5, 5))
        floor_rect_left = pygame.Rect(self.rect.bottomright, (-5, 5))

        wall_rect = pygame.Rect(self.rect.topleft, (self.rect.width, 5))

        if floor_rect_right.collidelist(self.collision_rects) and self.direction > 0 or\
                floor_rect_left.collidelist(self.collision_rects) and self.direction < 0 or\
                wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1

class Snake(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, health):
        super().__init__(groups)
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']

        self.health = health

    def update(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]

class Bear(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']


    def update(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]

