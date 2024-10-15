from sprites import AnimatedSprite
from random import randint
from setting import *
from timer import Timer

class display: 
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()  # draw on display surface
        self.sprites = pygame.sprite.Group()
        self.font = font

        # health / heart display
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # sword / sword display
        self.sword_frames = frames['sword']
        self.sword_surf_width = self.sword_frames[0].get_width()
        self.sword_padding = 5

        # coins
        self.coin_amount = 0
        self.coin_timer = Timer(1000)

    def create_heart(self, amount):
        for sprite in self.sprites:
            if isinstance(sprite, Heart):
                sprite.kill()
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10  # topleft.y + 10
            Heart((x, y), self.heart_frames, self.sprites)

    def create_sword(self, amount):
        for sprite in self.sprites:
            if isinstance(sprite, Sword):
                sprite.kill()
        for sword in range(amount):
            x = 10 + sword * (self.sword_surf_width + self.sword_padding)
            y = 30  # topleft.y + 30
            Sword((x, y), self.sword_frames, self.sprites)

    def update(self, dt):
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)


class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else: # finish animation
            self.active = False
            self.frames_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 2000) == 1: # Timer(Heart can only be animated in random time)
                self.active = True

class Sword(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else: # finish animation
            self.active = False
            self.frames_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 2000) == 1: # Timer(Heart can only be animated in random time)
                self.active = True