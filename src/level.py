import random

import pygame

from setting import *

from sprites import Sprite, movingSprite, AnimatedSprite, ParticleEffectSprite, Item
from player import Player
from groups import AllSprite
from enemies import Tooth, Bear

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
            width=tmx_map.width,
            height=tmx_map.height,
            bg_tile=bg_tile,
            top_limit=tmx_level_properties['top_limit'],
        )
        self.collision_sprites = pygame.sprite.Group()              #các sprite có khả năng va chạm với các đối tượng khác
        self.semi_collision_sprites = pygame.sprite.Group()         #có va chạm một phần hoặc một số loại va chạm khác biệt, như nền tảng mà nhân vật chỉ va chạm từ phía trên nhưng có thể đi qua từ phía dưới.
        self.damage_sprites = pygame.sprite.Group()                 #Khi va chạm với các sprite này, người chơi có thể bị trừ máu hoặc bị loại khỏi màn chơi
        self.item_sprites = pygame.sprite.Group()                   #vật phẩm mà người chơi có thể thu thập, chẳng hạn như tiền, vũ khí, hoặc vật phẩm tăng sức mạnh.
        self.invisible_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.snake_sprites = pygame.sprite.Group()
        self.boom_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

        # frames
        self.particle_frames = level_frames['particle']
        self.boom_frames = level_frames['items']['boom']
        self.sword = level_frames['items']['dame']

        # audio
        self.damage_sound = audio_files['damage']
        self.coin_sound = audio_files['coin']
        self.hit_sound = audio_files['hit']

        self.damage_sound.set_volume(0.3)

    def setup(self, tmx_map, level_frames):
        # tiles
        # for layer in ['Background', 'Terrain', 'FG', 'Platforms']:
        for layer in ['Background', 'Terrain', 'FG']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                group_sprites = [self.all_sprites]
                if layer == 'Terrain': group_sprites.append(self.collision_sprites)
                # if layer == 'Platforms': group_sprites.append(self.semi_collision_sprites)
                z_layer = {
                    'FG': Z_LAYERS['bg tiles'],
                    'Background': Z_LAYERS['bg tiles'],
                }
                tile_width = surf.get_width()
                tile_height = surf.get_height()

                # print(f'Layer: {layer}, Tile position: ({x}, {y}), Tile size: ({tile_width}x{tile_height})')
                z = z_layer.get(layer, Z_LAYERS['main'])
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, group_sprites, z)

        # Object
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'flag':
                self.finish_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
            if obj.name == 'player':
                self.player = Player(pos=(obj.x, obj.y - 100),
                                     groups=self.all_sprites,
                                     collision_sprites=self.collision_sprites,
                                     semi_collision_sprites=self.semi_collision_sprites,
                                     frames=level_frames['player_knight'],
                                     sound=self.audio_files,
                                     data=self.data)
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))


        # Moving Objects
        for obj in tmx_map.get_layer_by_name('Moving Object'):
            if obj.name == 'moving_chain':
                # print(level_frames[obj.name])
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'], ANIMATION_SPEED)
            else:
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] \
                            else (self.all_sprites, self.damage_sprites)
                if obj.width > obj.height: # horizontal move
                    move_direction = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # vertical move
                    move_direction = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                movingSprite(frames, groups, start_pos, end_pos, move_direction, speed, obj.properties['flip'])

        # Enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'],
                      (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites, obj.properties['health'])
            # elif obj.name == 'snake':
            #     Snake((obj.x, obj.y), level_frames['snake'], (self.all_sprites, self.damage_sprites, self.snake_sprites), obj.properties['health'])
            elif obj.name == 'bear':
                Bear((obj.x, obj.y), level_frames['bear_trap'], (self.all_sprites, self.damage_sprites, self.snake_sprites))

        # Items
        for obj in tmx_map.get_layer_by_name('Items'):
            is_visible = True
            if obj.name == 'boom' or obj.name == 'dame':
                is_visible = False

            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name],
                 (self.all_sprites, self.item_sprites), self.data, self.player, is_visible)

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.damage_sound.play()
                # print('player damage')
                self.player.get_damage()
                if hasattr(sprite, 'snake'):  # change later
                    sprite.kill()
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

    def attack_collision(self):
        for target in self.tooth_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or\
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right

            if target.rect.colliderect(self.player.hitbox_rect) and self.player.attacking and facing_target:
                target.health -= self.player.attack_damage
                self.hit_sound.play()
                self.player.attacking = True

                if target.health <= 0:
                    item_type = random.choice(['boom', 'dame', 'none'])

                    if item_type == 'boom':
                        Item(item_type=item_type,
                             pos=target.rect.center,
                             frames=self.boom_frames,
                             groups=(self.all_sprites, self.boom_sprites),
                             data=self.data,
                             player=self.player,
                             visible=True)
                    elif item_type == 'dame':
                        Item(item_type=item_type,
                             pos=target.rect.center,
                             frames=self.sword,
                             groups=(self.all_sprites, self.item_sprites),
                             data=self.data,
                             player=self.player,
                             visible=True)

                    target.kill()



    def item_collision(self):
        if self.item_sprites:
            collided_items = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            for item in collided_items:
                if self.player.hitbox_rect.colliderect(item.rect):
                    item.pick_up()
                    item.activate()
                    ParticleEffectSprite(item.rect.center, self.particle_frames, self.all_sprites)
                    self.coin_sound.play()


    def run(self, dt):
        self.display_surface.fill('black')

        self.all_sprites.update(dt)
        self.hit_collision()

        self.item_collision()
        self.attack_collision()

        self.all_sprites.draw(self.player.hitbox_rect.center, dt)
