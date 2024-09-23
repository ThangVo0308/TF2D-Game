import pygame.sprite

from setting import *
from data import Data
from timer import Timer
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames, collision_sprites, semi_collision_sprites, sound, data):
        super().__init__(groups)

        self.z = Z_LAYERS['main']

        # data
        self.data = data

        # image
        self.frames, self.frames_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frames_index]
        # rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-80, 40)
        self.old_rect = self.rect.copy()
        self.hitbox_rect.topleft = self.rect.topleft

        # movement setup
        self.direction = vector()
        self.speed = 300
        self.gravity = 30
        self.jump_height = 15
        self.jump = False
        self.attacking = False

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
            'platform skip': Timer(300),  # for moving down when clicking down button
            'attack block': Timer(500),
            'delay enemy damage': Timer(400)
        }

        # sound
        self.jump_sound = sound['jump']
        self.attack_sound = sound['attack']
        self.jump_sound.set_volume(0.2)

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

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
            self.attacking = True

            self.frames_index = 0
            self.timers['attack block'].activate()
            self.attack_sound.play()

    def move(self, dt):
        # horizontal move
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical move
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) \
                and not self.timers['wall slide block'].active:
            self.direction.y += self.gravity / 10 * dt  # calculate
            self.hitbox_rect.y += self.direction.y  # move
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 10  # fix error when player jump up and down in moving object, player can't move
                self.jump_sound.play()

        self.jump = False

        self.collision('vertical')
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left collision
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(
                            sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # right collision
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(
                            sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    # vertical collision(top collision)
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(
                            sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        # fix the problem when the moving sprite(verical) is moving down and the player is under it, it will stuck under the sprite
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 5

                    # bottom collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(
                            sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0  # moving down error fix
    def semi_collision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    # Fix when sprite is moving down
                    elif sprite.rect.colliderect(self.hitbox_rect.move(0, self.direction.y)) and self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0

    def platform_move(self, dt):
        if self.platform:  # if player is standing on the platform > moving the player by the direction of the platform at current frame rate
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt

    def check_contact(self):
        # floor check
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rects = [sprite.rect for sprite in self.semi_collision_sprites]

        # collision check(on floor check)
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or \
                                           floor_rect.collidelist(
                                               semi_collide_rects) >= 0 and self.direction.y >= 0 else False

        # wall check
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4),
                                 (2, self.hitbox_rect.height / 2))
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False

        # left check
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4),
                                (2, self.hitbox_rect.height / 2))
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        # platform check
        # check that player is standing on a moving object or not
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()

        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
    # ----------------------------------------------------------
    # PLAYER
    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'idle'

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frames_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frames_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        # Fix when jump > the player auto attack
        if self.attacking and self.frames_index > len(self.frames[self.state]):
            self.attacking = False

    def get_damage(self):
        if not self.timers['delay enemy damage'].active:
            self.data.health -= 1
            self.timers['delay enemy damage'].activate()

    def flicker(self): # animation when player get hit
        if self.timers['delay tooth damage'].active and sin(pygame.time.get_ticks() * 100) >= 0: # *100: faster responding flicker
            white_mask = pygame.mask.from_surface(self.image)
            white_surface = white_mask.to_surface() # Convert to surface which will display by white pixel
            white_surface.set_colorkey('black') # remove black image around player
            self.image = white_mask


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timer()

        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()

        # player
        self.get_state()
        self.animate(dt)
        self.flicker()

