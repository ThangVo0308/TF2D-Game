from setting import *
from pytmx.util_pygame import load_pygame  # pip install pytmx
from os.path import join
from data import *
from sprites import *
from level import Level
from folderHandle import *
from display import display
import os


class Main:
    def __init__(self, ):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('TF2D World')
        self.clock_tick = pygame.time.Clock()
        self.import_assets()

        self.display = display(self.font, self.ui_frames)

        self.data = Data(self.display)

        base_path = os.path.dirname(__file__)

        self.tmx_maps = {
            0: load_pygame(join(base_path,'..', 'data', 'levels', 'underground.tmx')),
        }

        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_map)

        self.audio_files['bg_music'].play()
        self.audio_files['bg_music'].set_volume(0.2)


    def import_assets(self):
        base_path = os.path.dirname(__file__)
        self.level_frames = {
            'items': {
                'hp': import_image(join(base_path,'..', 'graphics', 'items', 'apple')),
                'dame': import_image(join(base_path,'..', 'graphics', 'items', 'dame')),
                'key': import_image(join(base_path,'..', 'graphics', 'items', 'key')),
                'protect': import_image(join(base_path,'..', 'graphics', 'items', 'protect')),
                'boom': import_folder(join(base_path,'..', 'graphics', 'items', 'boom')),
                'buff': import_folder(join(base_path,'..', 'graphics', 'items', 'buff')),
                'hp_animate': import_folder(join(base_path,'..', 'graphics', 'items', 'hp')),
            },
            'skeleton': import_folder(join(base_path,'..', 'graphics', 'enemies', 'skeleton', 'run')),
            'thorn': import_folder(join(base_path,'..', 'graphics', 'enemies', 'thorn')),
            'tooth': import_folder(join(base_path,'..', 'graphics', 'enemies', 'tooth', 'run')),
            'bear_trap': import_folder(join(base_path,'..', 'graphics', 'objects', 'bear_trap')),
            'moving_chain': import_folder(join(base_path,'..', 'graphics', 'objects', 'chain_moving')),
            'flag': import_folder(join(base_path,'..', 'graphics', 'objects', 'flag')),
            'floor_spike': import_folder(join(base_path,'..', 'graphics', 'objects', 'floor_spikes')),
            'helicopter': import_folder(join(base_path,'..', 'graphics', 'objects', 'helicopter')),
            'vine': import_folder(join(base_path,'..', 'graphics', 'objects', 'vines')),
            'chain': import_image(join(base_path,'..', 'graphics', 'objects', 'chain')),
            'cord': import_image(join(base_path,'..', 'graphics', 'objects', 'cord')),
            'particle': import_folder(join(base_path,'..', 'graphics', 'effects', 'particle')),
            'player_knight': import_sub_folders(join(base_path,'..', 'graphics', 'player','knight')),
            # 'player_mage': import_sub_folders(join('..', 'graphics', 'player','mage')),
            # 'player_rogue': import_sub_folders(join('..', 'graphics', 'player','Rogue')),
        }


        self.audio_files = {
            'coin': pygame.mixer.Sound(join(base_path,'..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join(base_path,'..', 'audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join(base_path,'..', 'audio', 'damage.wav')),
            'hit': pygame.mixer.Sound(join(base_path,'..', 'audio', 'hit.wav')),
            'jump': pygame.mixer.Sound(join(base_path,'..', 'audio', 'jump.wav')),
            'bg_music': pygame.mixer.Sound(join(base_path,'..', 'audio', 'starlight_city.mp3'))
        }

        self.font = pygame.font.Font(join('..','graphics','ui','runescape_uf.ttf'), 40)

        self.ui_frames = {
            'heart': import_folder(join('..', 'graphics', 'ui', 'heart')),
            'sword': import_folder(join('..', 'graphics', 'ui', 'heart'))
        }


    def switch_map(self, target, level=0):
        if target == 'level': # when player is inside a level map
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames,  self.audio_files,self.data, self.switch_map)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        while True:
            dt = self.clock_tick.tick(60) / 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.check_game_over()
            self.current_stage.run(dt)
            self.display.update(dt)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
