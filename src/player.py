import pygame.sprite

from setting import *
from data import Data
from timer import Timer
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames, collision_sprites, semi_collision_sprites,sound, data):
        super().__init__(groups)

        self.z = Z_LAYERS['main']

        #data
        self.data = data

        # image
        self.frames, self.frames_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frames_index]
        # rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-80,40)
        self.old_rect = self.rect.copy()
        self.hitbox_rect.topleft = self.rect.topleft

        # movement setup
        self.direction = vector()
        self.speed = 300
        self.gravity = 30
        self.jump_height = 15
        self.jump = False
        self.attack = False

        # collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False,
                           'right': False}  # True when collising with floor, left wall, right wall
        self.platform = None

        # Timer
        self.timers = {
            'wall jump': Timer(250),
            'wall slide block': Timer(200),
            'platform skip': Timer(300), # for moving down when clicking down button
            'attack block': Timer(500),
        }

        # sound
        self.jump_sound = sound['jump']
        self.attack_sound = sound['attack']
        self.jump_sound.set_volume(0.2)

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
                self.facing_right = True
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
                self.facing_right = False
            self.direction.x = input_vector.normalize().x if input_vector else 0

        if keys[pygame.K_SPACE]:
            self.jump = True
            self.timers['wall jump'].activate()
        if keys[pygame.K_DOWN]:
            self.timers['platform skip'].activate()

        if keys[pygame.K_x]:
            self.attack()

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def attack(self):
        if not self.timers['attack block'].active:
            self.attack = True

            self.frames_index = 0
            self.timers['attack block'].activate()
            self.attack_sound.play()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timer()

