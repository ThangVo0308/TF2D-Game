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
        self.speed = 10
        self.health = int(health)

        self.hit_timer = Timer(250)
        self.on_ground = False  # Biến để theo dõi trạng thái chạm terrain

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()
        if dt > 0.5:
            dt = 0.5
        # animation
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # Movement

        self.rect.x += self.direction * self.speed * dt

        if not self.is_on_terrain():
            self.direction *= -1

    def is_on_terrain(self):
        for rect in self.collision_rects:
            if(self.direction == 1):
                left_rect = self.rect.move(self.rect.width / 2, self.rect.height)
            else:
                left_rect = self.rect.move(-self.rect.width / 2, self.rect.height)

            if left_rect.colliderect(rect):
                return True

        # Nếu không có va chạm nào, trả về False (không tiếp xúc với terrain)
        return False

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, health):
        super().__init__(groups)
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 7
        self.health = int(health)

        self.hit_timer = Timer(250)
        self.on_ground = False  # Biến để theo dõi trạng thái chạm terrain

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()
        if dt > 0.5:
            dt = 0.5
        # animation
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # Movement
        self.rect.x += self.direction * self.speed * dt

        # Kiểm tra xem có terrain dưới chân hay không
        if self.is_on_terrain() == False:
            self.direction *= -1

    def is_on_terrain(self):
        for rect in self.collision_rects:
            if(self.direction == 1):
                left_rect = self.rect.move(self.rect.width / 2, self.rect.height)
            else:
                left_rect = self.rect.move(-self.rect.width / 2, self.rect.height)

            if left_rect.colliderect(rect):
                return True

        # Nếu không có va chạm nào, trả về False (không tiếp xúc với terrain)
        return False

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

class FloorSpike(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, flip_down=False, flip_left=False, flip_right=False):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.flip_down = flip_down
        self.flip_left = flip_left
        self.flip_right = flip_right
        self.image = self.get_image()
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']

    def get_image(self):
        image = self.frames[int(self.frames_index % len(self.frames))]

        if self.flip_down:
            image = pygame.transform.flip(image, False, True)  # Lat xuong
        elif self.flip_left:
            image = pygame.transform.rotate(image, 90)  # Lat trai
        elif self.flip_right:
            image = pygame.transform.rotate(image, -90)  # Lat phai

        return image

    def update(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.get_image()
