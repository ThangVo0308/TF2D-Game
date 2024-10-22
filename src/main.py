from setting import *
from pytmx.util_pygame import load_pygame  # pip install pytmx
from os.path import join
from data import *
from sprites import *
from level import *
from folderHandle import *
from display import display
import os
from button import Button


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH-30, WINDOW_HEIGHT-70))
        pygame.display.set_caption('TF2D World')
        self.clock_tick = pygame.time.Clock()
        self.import_assets()

        self.display = display(self.font, self.ui_frames)
        self.data = Data(self.display)

        base_path = os.path.dirname(__file__)
        self.selectedPlayer = "player_knight"

        self.tmx_maps = {
            0: load_pygame(join(base_path, '..', 'data', 'levels', 'underground.tmx')),
            1: load_pygame(join(base_path, '..', 'data', 'levels', 'outsite.tmx')),
        }

        #self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
        #                           self.audio_files, self.data, self.switch_map)

        self.audio_files['bg_music'].play(-1)
        self.audio_files['bg_music'].set_volume(0.9)

    def import_assets(self):
        base_path = os.path.dirname(__file__)
        self.level_frames = {
            'items': {
                'hp': import_image(join(base_path, '..', 'graphics', 'items', 'apple')),
                'dame': import_image(join(base_path, '..', 'graphics', 'items', 'dame')),
                'key': import_image(join(base_path, '..', 'graphics', 'items', 'key')),
                'protect': import_image(join(base_path, '..', 'graphics', 'items', 'protect')),
                'boom': import_folder(join(base_path, '..', 'graphics', 'items', 'boom')),
                'buff': import_folder(join(base_path, '..', 'graphics', 'items', 'buff')),
                'hp_animate': import_folder(join(base_path, '..', 'graphics', 'items', 'hp')),
            },
            'skeleton': import_folder(join(base_path, '..', 'graphics', 'enemies', 'skeleton', 'run')),
            'thorn': import_folder(join(base_path, '..', 'graphics', 'enemies', 'thorn')),
            'tooth': import_folder(join(base_path, '..', 'graphics', 'enemies', 'tooth', 'run')),
            'bear_trap': import_folder(join(base_path, '..', 'graphics', 'objects', 'bear_trap')),
            'moving_chain': import_folder(join(base_path, '..', 'graphics', 'objects', 'chain_moving')),
            'snake': import_folder(join(base_path, '..', 'graphics', 'objects', 'snake')),
            'flag': import_folder(join(base_path, '..', 'graphics', 'objects', 'flag')),
            'floor_spike': import_folder(join(base_path, '..', 'graphics', 'objects', 'floor_spikes')),
            'helicopter': import_folder(join(base_path, '..', 'graphics', 'objects', 'helicopter')),
            'vine': import_folder(join(base_path, '..', 'graphics', 'objects', 'vines')),
            'chain': import_image(join(base_path, '..', 'graphics', 'objects', 'chain')),
            'cord': import_image(join(base_path, '..', 'graphics', 'objects', 'cord')),
            'particle': import_folder(join(base_path, '..', 'graphics', 'effects', 'particle')),
            'player_knight': import_sub_folders(join(base_path, '..', 'graphics', 'player', 'knight')),
            'player_mage': import_sub_folders(join(base_path,'..', 'graphics', 'player','mage')),
            'player_rogue': import_sub_folders(join(base_path,'..', 'graphics', 'player','Rogue')),
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join(base_path, '..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join(base_path, '..', 'audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join(base_path, '..', 'audio', 'damage.wav')),
            'hit': pygame.mixer.Sound(join(base_path, '..', 'audio', 'hit.wav')),
            'jump': pygame.mixer.Sound(join(base_path, '..', 'audio', 'jump.wav')),
            'bg_music': pygame.mixer.Sound(join(base_path, '..', 'audio', 'starlight_city.mp3')),
            'click_button': pygame.mixer.Sound(join(base_path, '..', 'audio', 'click_button.mp3'))
        }

        self.font = pygame.font.Font(join(base_path, '..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)

        self.ui_frames = {
            'heart': import_folder(join(base_path, '..', 'graphics', 'ui', 'heart')),
            'sword': import_folder(join(base_path, '..', 'graphics', 'ui', 'heart'))
        }

        self.menu_background = pygame.image.load(os.path.join(base_path, '..', 'graphics', 'map', 
                                                              'background', 'bg_underwatermap.png'))

    def switch_map(self, target, level=0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                       self.audio_files, self.data, self.switch_map, self.selectedPlayer)

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

    def menu(self):     
        BG = self.menu_background
        
        SCREEN = self.display_surface
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("TF2D WORLD", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                                    text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=None, pos=(640, 400), 
                                        text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=None, pos=(640, 550), 
                                    text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):                        
                        self.audio_files['click_button'].play()
                        self.select_character_menu()
                        #self.run()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def get_font(self, size): 
        return pygame.font.Font(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 
                                             'graphics', 'font', 'start_menu_font.ttf'), size)        
        
    def options(self):
        SCREEN = self.display_surface
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("white")

            OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                                    text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.menu()

            pygame.display.update()

    def select_character_menu(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        SCREEN = self.display_surface
        while True:
            SELECT_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("white")

            SELECT_TEXT = self.get_font(45).render("SELECT CHARACTER", True, "Black")
            SELECT_RECT = SELECT_TEXT.get_rect(center=(640, 50))
            SCREEN.blit(SELECT_TEXT, SELECT_RECT)

            SELECT_PLAYER_KNIGHT = Button(image=pygame.image.load(os.path.join(project_root, 'graphics', 'player', 'knight', 'Idle', '5.png')), 
                                   pos=(440, 250), text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")            
            SELECT_PLAYER_MAGE = Button(image=pygame.image.load(os.path.join(project_root, 'graphics', 'player', 'mage', 'Idle', '8.png')), 
                                 pos=(640, 250), text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            SELECT_PLAYER_ROGUE = Button(image=pygame.image.load(os.path.join(project_root, 'graphics', 'player', 'Rogue', 'Idle', '0.png')), 
                                  pos=(840, 250), text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            for player in [SELECT_PLAYER_KNIGHT, SELECT_PLAYER_MAGE, SELECT_PLAYER_ROGUE]:
                player.changeColor(SELECT_MOUSE_POS)
                player.update(SCREEN)

            SELECT_BACK = Button(image=None, pos=(640, 570), 
                                    text_input="BACK", font=self.get_font(45), base_color="Black", hovering_color="Green")

            SELECT_BACK.changeColor(SELECT_MOUSE_POS)
            SELECT_BACK.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SELECT_PLAYER_KNIGHT.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                   self.audio_files, self.data, self.switch_map, 'player_knight')
                        self.selectedPlayer = "player_knight"
                        self.run()
                    if SELECT_PLAYER_MAGE.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                   self.audio_files, self.data, self.switch_map, 'player_mage')
                        self.selectedPlayer = "player_mage"
                        self.run()                        
                    if SELECT_PLAYER_ROGUE.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                   self.audio_files, self.data, self.switch_map, 'player_rogue')
                        self.selectedPlayer = "player_rogue"
                        self.run()
                    if SELECT_BACK.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.menu()                        
            pygame.display.update()

if __name__ == "__main__":    
    main = Main()
    main.menu()

