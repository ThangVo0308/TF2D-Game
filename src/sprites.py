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

class movingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_direction, speed, flip=False):
        super().__init__(start_pos, frames, groups)
        if move_direction == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos

        self.rect.center = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos

        # movement
        self.speed = speed
        self.direction = vector(1, 0) if move_direction == 'x' else vector(0, 1)
        self.move_direction = move_direction
        self.moving = True
        self.flip = flip
        self.reverse = {'x': False, 'y': False}

    def check_border(self):
        if self.move_direction == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]

            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]

            self.reverse['x'] = True if self.direction.x < 0 else False
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]

            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]

            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()

        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else: # destroy
            self.kill()