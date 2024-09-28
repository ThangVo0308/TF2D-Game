from setting import *
import pygame.sprite
import threading, time

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None, z=Z_LAYERS['main']):
        super().__init__(groups)

        # Terrain
        self.image = surface

        # Player
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        if isinstance(frames, pygame.Surface):
            frames = [frames]

        self.frames, self.frames_index = frames, 0
        super().__init__(pos, self.frames[self.frames_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]

    def update(self, dt):
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
        self.rect.topleft += self.direction * float(self.speed) * dt
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

class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data, player, visible=False):
        animated = item_type in ['boom', 'buff', 'hp_animate']
        super().__init__(pos, frames, groups)

        self.rect.center = pos
        self.item_type = item_type
        self.data = data
        self.player = player
        self.visible = visible

        # Item properties
        self.is_picked_up = False
        self.item_expiration_time = 10  # Duration item effect

    def animate(self, dt):
        if self.item_type == 'boom':
            self.frames_index += self.animation_speed * dt

            if self.frames_index < len(self.frames):
                self.image = self.frames[int(self.frames_index)]
            else:  # destroy
                # Kiểm tra nếu hitbox của player va chạm với vùng của item
                if self.player.hitbox_rect.colliderect(self.rect.inflate(TILE_SIZE, TILE_SIZE)):
                    print(self.data.health)
                    self.data.health -= 2

                self.kill()  # Xóa item


    def activate(self):
        if not self.is_picked_up:
            if self.item_type == 'key':
                self.data.keys += 1
                if self.data.keys == 3:
                    print("ok")

            elif self.item_type == 'buff':
                self.apply_buff()

            elif self.item_type == 'dame':
                self.apply_damage_buff()

            elif self.item_type in ['hp_animate', 'hp']:
                self.data.health += 1

            if not self.visible:
                self.hide()

    def apply_buff(self):
        if not self.is_picked_up:
            self.player.jump_height += 5
            self.is_picked_up = True
            threading.Thread(target=self.start_timer).start()  # Create threads for timer

    def apply_damage_buff(self):
        if not self.is_picked_up:
            self.player.attack_damage += 1
            self.is_picked_up = True
            threading.Thread(target=self.start_timer).start() # Create threads for timer

    def start_timer(self):
        time.sleep(self.item_expiration_time)  # Wait for expire(10s)
        self.reset()

    def reset(self):
        if self.is_picked_up:
            if self.item_type == 'buff':
                self.player.jump_height -= 5
            elif self.item_type == 'dame':
                self.player.attack_damage -= 1
            self.is_picked_up = False

    def pick_up(self):
        if not self.is_picked_up:
            self.activate()

    def hide(self):
        for group in self.groups():
            group.remove(self)
        self.visible = False

    def update(self, dt):
        self.animate(dt)
        if not self.visible:
            self.hide()





