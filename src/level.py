from setting import *

from sprites import Sprite, movingSprite, AnimatedSprite, ParticleEffectSprite
from player import Player
from groups import AllSprite

class Level:
    def __init__(self, tmx_map, level_frames, audio_files, data, switch_map):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.audio_files = audio_files
        self.switch_map = switch_map

        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']

        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None
        # groups
        self.all_sprites = AllSprite(
            width = tmx_map.width,
            height = tmx_map.height,
            bg_tile = bg_tile,
            top_limit = tmx_level_properties['top_limit'],
        )
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.invisible_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

        # frames
        self.particle_frames = level_frames['particle']

        # audio
        self.coin_sound = audio_files['coin']
        self.damage_sound = audio_files['damage']
        self.hit_sound = audio_files['hit']
        self.pearl_sound = audio_files['pearl']

        self.coin_sound.set_volume(0.4)

    def setup(self, tmx_map, level_frames):
        pass;

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.damage_sound.play()
                # print('player damage')
                self.player.get_damage()
                if hasattr(sprite, 'snake'): # change later
                    sprite.kill()
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True) # destroy items when player collects
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)
                self.coin_sound.play()


    def run(self, dt):
        self.display_surface.fill('black')

        self.all_sprites.update(dt)
        self.hit_collision()

        self.item_collision()

        self.all_sprites.draw(self.player.hitbox_rect.center, dt)