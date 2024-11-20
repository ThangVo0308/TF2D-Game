import pygame.sprite

from setting import *
from data import Data
from timer import Timer
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames, collision_sprites, semi_collision_sprites, sound, data, visible=False):
        super().__init__(groups)

        self.z = Z_LAYERS['main']

        self.visible = visible

        # data
        self.data = data

        if self.visible:
            # image(handle when player moves)
            self.frames, self.frame_index = frames, 0
            self.state, self.facing_right = 'Idle', True
            self.image = self.frames[self.state][self.frame_index]
            # rects
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox_rect = self.rect.inflate(5, 0)
            self.old_rect = self.hitbox_rect.copy()
            self.hitbox_rect.topleft = self.rect.topleft

            # movement
            self.direction = vector()
            self.speed = 20
            self.gravity = 30
            self.jump = False
            self.jump_height = 15
            self.attacking = False

        # collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        self.display_surface = pygame.display.get_surface()

        # Timer
        self.timers = {
            'wall jump': Timer(250),
            'jump': Timer(300),
            'platform skip': Timer(300),
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
            if input_vector.length() > 0:
                self.direction.x = input_vector.normalize().x
            else:
                self.direction.x = 0
        if keys[pygame.K_SPACE]:
            self.jump = True
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
            # Fix the player attacking when standing on the floor and can't attack(refresh frame_index)
            self.frame_index = 0
            self.timers['attack block'].activate()
            self.attack_sound.play()

    def move(self, dt):
        # horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical
        if not self.on_surface['floor']:
            self.direction.y += self.gravity / 10 * dt  # result of direction.y calculation
            self.hitbox_rect.y += self.direction.y  # move direction.y
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['jump'].activate()
                self.hitbox_rect.bottom -= 10  # fix the error that when player try to jump in up and down moving object, the player can't jump
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
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # right collision
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:  # vertical collision
                    # top collision
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        # fix the problem when the moving sprite (vertical) is moving down and the player is under it
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 5

                    # bottom collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0  # prevent vertical collision keep increasing self.direction.y

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
            self.hitbox_rect.topleft += self.platform.direction * int(self.platform.speed) * dt        

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

        # # left check
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
                self.state = 'Attack'
            else:
                self.state = 'Idle' if self.direction.x == 0 else 'Run'
        else:
            if self.attacking:
                self.state = 'Attack_Extra'
            else:
                if self.direction.y < 0:
                    self.state = 'Jump'
                elif self.direction.y > 0:
                    self.state = 'Fall'

    def animate(self, dt):
        previous_image_width = self.image.get_width()

        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'Hurt' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'Idle'  # Khi hoạt ảnh Hurt kết thúc, quay lại trạng thái Idle

        if self.state == 'Attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'Idle'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        # Fix when jump > the player auto attack
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

        current_image_width = self.image.get_width()
        width_diff = current_image_width - previous_image_width

        if self.facing_right:
            self.rect.x -= width_diff

    def get_damage(self):
        if not self.timers['delay enemy damage'].active:
            self.data.health -= 1
            self.timers['delay enemy damage'].activate()

    def flicker(self):  # animation when player gets hit
        self.original_image = self.image.copy()

        if self.timers['delay enemy damage'].active and sin(pygame.time.get_ticks() * 35) >= 0:
            self.state = 'Hurt'
            self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        else:
            self.image = self.original_image

    def is_off_screen(self, map_height):
        if self.rect.bottom > map_height:
            return True
        return False
    
    def is_colliderect_winner(self, obj):
        if self.rect.x - 41 == obj.x and self.rect.y + 34 == obj.y :
            return True
        return False

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

