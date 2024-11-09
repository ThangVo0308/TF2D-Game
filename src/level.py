import random

import pygame

from setting import *

from sprites import Sprite, movingSprite, AnimatedSprite, ParticleEffectSprite, Item
from player import Player
from groups import AllSprite
from enemies import Tooth, Bear, Skeleton, FloorSpike

class Level:
    def __init__(self, tmx_map, level_frames, audio_files, data, switch_map, selected_player, alert):
        self.finish_rect = None
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.audio_files = audio_files
        self.switch_map = switch_map
        self.selected_player = selected_player
        self.key_quantity = 0

        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']

        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        self.flag_rect = 70

        # init player
        self.player_init = False

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
        self.skeleton_sprites = pygame.sprite.Group()
        self.snake_sprites = pygame.sprite.Group()
        self.boom_sprites = pygame.sprite.Group()
        self.floor_spikes = pygame.sprite.Group()

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

        self.alert = alert


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
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.all_sprites))

        # Player
        for obj in tmx_map.get_layer_by_name('Players'):
            if not self.player_init:
                self.player = Player(pos=(obj.x, obj.y - 100),
                                     groups=self.all_sprites,
                                     collision_sprites=self.collision_sprites,
                                     semi_collision_sprites=self.semi_collision_sprites,
                                     frames=level_frames[self.selected_player],
                                     sound=self.audio_files,
                                     data=self.data,
                                     visible=True)
                self.player_init = True

        # Moving Objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'moving_chain':
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'], ANIMATION_SPEED, reverse=False)
            elif obj.name == 'flag':
                self.finish_rect = pygame.Rect((obj.x + self.flag_rect, obj.y), (obj.width, obj.height))
                AnimatedSprite((obj.x, obj.y), level_frames['flag'], self.all_sprites, Z_LAYERS['bg tiles'], ANIMATION_SPEED, reverse=True)
            elif obj.name == 'snake':
                AnimatedSprite((obj.x, obj.y), level_frames['snake'], self.all_sprites, Z_LAYERS['main'], ANIMATION_SPEED, reverse=False)
            elif obj.name == 'vine':
                AnimatedSprite((obj.x, obj.y), level_frames['vine'], self.all_sprites, Z_LAYERS['main'], ANIMATION_SPEED, reverse=False)
            elif obj.name == 'big_cloud':
                AnimatedSprite((obj.x, obj.y), level_frames['big_cloud'], self.all_sprites, Z_LAYERS['main'], 0.3, reverse=False)
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

                if obj.name == 'saw':
                    if move_direction == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, z=Z_LAYERS['bg details'])
                    else:
                        x = start_pos[0] - level_frames['saw_chain'].get_height() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, z=Z_LAYERS['bg details'])

        # Enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'],
                      (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites, obj.properties['health'])
            elif obj.name == 'bear':
                Bear((obj.x, obj.y), level_frames['bear_trap'], (self.all_sprites, self.damage_sprites, self.snake_sprites))
            elif obj.name == 'skeleton':
                Skeleton((obj.x, obj.y), level_frames['skeleton'],
                      (self.all_sprites, self.damage_sprites, self.skeleton_sprites), self.collision_sprites, obj.properties['health'])
            elif obj.name == 'floor_spike':
                flip_down = obj.properties.get('flip', False)
                flip_left = obj.properties.get('flip_left', False)
                flip_right = obj.properties.get('flip_right', False)

                FloorSpike((obj.x, obj.y), level_frames['floor_spike'],
                   (self.all_sprites, self.damage_sprites, self.floor_spikes),
                          flip_down=flip_down, flip_left=flip_left, flip_right=flip_right)

        # Items
        for obj in tmx_map.get_layer_by_name('Items'):
            is_visible = True
            if obj.name == 'boom' or obj.name == 'dame':
                is_visible = False

            if obj.name == 'key':
                self.key_rect = 10
                Item(obj.name, (obj.x + + self.key_rect + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name],
                     (self.all_sprites, self.item_sprites), self.data, self.player, is_visible)
            else:
                Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name],
                 (self.all_sprites, self.item_sprites), self.data, self.player, is_visible)

        # water
        try:
            for obj in tmx_map.get_layer_by_name('Water'):
                rows = int(obj.height / TILE_SIZE)
                columns = int(obj.width / TILE_SIZE)
                for row in range(rows):
                    for col in range(columns):
                        x = obj.x + col * TILE_SIZE
                        y = obj.y + row * TILE_SIZE
                        if row == 0:
                            AnimatedSprite((x, y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
                        else:
                            Sprite((x, y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])

        except ValueError:
            pass


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
        sprites = self.tooth_sprites.sprites() + self.skeleton_sprites.sprites()
        for target in sprites:
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or\
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right

            if target.rect.colliderect(self.player.hitbox_rect) and self.player.attacking and facing_target:
                target.health -= self.data.damage
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
            collided_items = pygame.sprite.spritecollide(self.player, self.item_sprites, False)
            for item in collided_items:
                if self.player.hitbox_rect.colliderect(item.rect):
                    item.pick_up()
                    item.activate()
                    ParticleEffectSprite(item.rect.center, self.particle_frames, self.all_sprites)
                    self.coin_sound.play()
                    item.kill()

    def count_keys(self):
        self.key_quantity = 0
        for item in self.item_sprites:
            if item.item_type == 'key':
                self.key_quantity += 1

    #next to map
    def next_level(self):
        # print(self.key_quantity)
        if self.finish_rect is not None and isinstance(self.finish_rect, pygame.Rect):
            if isinstance(self.player.hitbox_rect, pygame.Rect):
                if self.player.hitbox_rect.colliderect(self.finish_rect):
                    if self.data.keys == self.key_quantity:
                        self.data.current_level += 1
                        self.switch_map('level', level=self.data.current_level)
                        self.data.keys = 0
                        self.key_quantity = 0
                        return
                    else:
                        self.alert.display_alert("You have to collect more keys!", 2000)
                        return

    def map_check(self):
        if self.player.hitbox_rect.left < 0:
            self.player.hitbox_rect.left = 0
        elif self.player.hitbox_rect.top < 0:
            self.player.hitbox_rect.top = 0
        elif self.player.hitbox_rect.right > self.level_width:
            self.player.hitbox_rect.right = self.level_width


    def run(self, dt):
        self.display_surface.fill('black')

        self.all_sprites.update(dt)
        self.hit_collision()

        self.count_keys()

        self.item_collision()
        self.attack_collision()
        self.next_level()
        self.map_check()

        self.all_sprites.draw(self.player.hitbox_rect.center, dt)


