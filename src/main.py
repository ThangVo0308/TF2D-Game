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
from alert import Alert


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
            2: load_pygame(join(base_path, '..', 'data', 'levels', 'underwater.tmx')),
            3: load_pygame(join(base_path, '..', 'data', 'levels', 'skyland.tmx'))
        }

        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames,
                                  self.audio_files, self.data, self.switch_map, self.selectedPlayer)

        self.audio_files['bg_music'].play(-1)
        self.audio_files['bg_music'].set_volume(0.5)

        self.show_alert = False
        self.alert_text = ""
        self.alert_start_time = 0
        self.alert_duration = 2000  # Thời gian hiển thị mặc định là 2 giây
        self.alert = Alert()

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
            'saw': import_folder(join(base_path,'..', 'graphics', 'enemies', 'saw', 'animation')),
            'saw_chain': import_image(join(base_path,'..', 'graphics', 'enemies', 'saw', 'saw_chain')),
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
            'water': import_folder(join(base_path,'..', 'graphics', 'objects', 'water')),
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
                                       self.audio_files, self.data, self.switch_map, self.selectedPlayer, self.alert)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()
            #self.menu()

    def run(self):
        while True:
            dt = self.clock_tick.tick(60) / 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #self.update_alert()
            self.check_game_over()
            self.current_stage.run(dt)
            self.display.update(dt)
            self.alert.update_alert()

            pygame.display.update()

    def menu(self):     
        BG = self.menu_background
        
        SCREEN = self.display_surface
        while True:
            self.alert.update_alert()
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
        volume_music = self.audio_files['bg_music'].get_volume()
        volume_effects = self.audio_files['click_button'].get_volume()

        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.fill("white")    
            #self.update_alert()
            self.alert.update_alert()

            # Back button
            OPTIONS_BACK = Button(image=None, pos=(640, 600), 
                                text_input="BACK", font=self.get_font(55), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)

            # Volume control title
            VOLUME_TEXT = self.get_font(45).render("Adjust Volume", True, "Black")
            VOLUME_RECT = VOLUME_TEXT.get_rect(center=(640, 150))
            SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

            # Render "Music Volume:" text separately
            MUSIC_VOL_LABEL = self.get_font(30).render("Music Volume: ", True, "Black")
            MUSIC_VOL_LABEL_RECT = MUSIC_VOL_LABEL.get_rect(center=(580, 280))  # Fix the position
            SCREEN.blit(MUSIC_VOL_LABEL, MUSIC_VOL_LABEL_RECT)

            # Render the percentage value separately
            MUSIC_VOL_VALUE = self.get_font(30).render(f"{int(volume_music * 100)}%", True, "Black")
            MUSIC_VOL_VALUE_RECT = MUSIC_VOL_VALUE.get_rect(center=(880, 280))  # Position this next to the label
            SCREEN.blit(MUSIC_VOL_VALUE, MUSIC_VOL_VALUE_RECT)

            # Sound Effects Volume
            EFFECTS_VOL_TEXT = self.get_font(30).render(f"Effects Volume:", True, "Black")
            EFFECTS_VOL_RECT = EFFECTS_VOL_TEXT.get_rect(center=(540, 340))
            SCREEN.blit(EFFECTS_VOL_TEXT, EFFECTS_VOL_RECT)

            EFFECTS_VOL_VALUE = self.get_font(30).render(f"{int(volume_effects * 100)}%", True, "Black")
            EFFECTS_VOL_VALUE_RECT = EFFECTS_VOL_VALUE.get_rect(center=(880, 340))  # Position this next to the label
            SCREEN.blit(EFFECTS_VOL_VALUE, EFFECTS_VOL_VALUE_RECT)

            # Volume control - Increase/Decrease buttons
            MUSIC_UP_BUTTON = Button(image=None, pos=(960, 280), text_input="+", font=self.get_font(40), 
                                    base_color="Black", hovering_color="Green")
            MUSIC_DOWN_BUTTON = Button(image=None, pos=(790, 280), text_input="-", font=self.get_font(40), 
                                    base_color="Black", hovering_color="Green")
            EFFECTS_UP_BUTTON = Button(image=None, pos=(960, 340), text_input="+", font=self.get_font(40), 
                                    base_color="Black", hovering_color="Green")
            EFFECTS_DOWN_BUTTON = Button(image=None, pos=(790, 340), text_input="-", font=self.get_font(40), 
                                        base_color="Black", hovering_color="Green")

            MUSIC_UP_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            MUSIC_DOWN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            EFFECTS_UP_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            EFFECTS_DOWN_BUTTON.changeColor(OPTIONS_MOUSE_POS)

            MUSIC_UP_BUTTON.update(SCREEN)
            MUSIC_DOWN_BUTTON.update(SCREEN)
            EFFECTS_UP_BUTTON.update(SCREEN)
            EFFECTS_DOWN_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle Music Volume controls
                    if MUSIC_UP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        volume_music = min(1.0, volume_music + 0.1)
                        self.audio_files['bg_music'].set_volume(volume_music)
                        self.audio_files['click_button'].play()
                        self.alert.display_alert("Hello beautiful world. I love you 3000. You are the cutest girl i have ever seen in my life.", 2000)

                    if MUSIC_DOWN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        volume_music = max(0.0, volume_music - 0.1)
                        self.audio_files['bg_music'].set_volume(volume_music)
                        self.audio_files['click_button'].play()

                    # Handle Effects Volume controls
                    if EFFECTS_UP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        volume_effects = min(1.0, volume_effects + 0.1)
                        self.audio_files['click_button'].set_volume(volume_effects)
                        self.audio_files['click_button'].play()

                    if EFFECTS_DOWN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        volume_effects = max(0.0, volume_effects - 0.1)
                        self.audio_files['click_button'].set_volume(volume_effects)
                        self.audio_files['click_button'].play()

                    # Handle Back button click
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
                                   self.audio_files, self.data, self.switch_map, 'player_knight', self.alert)
                        self.selectedPlayer = "player_knight"
                        self.run()
                    if SELECT_PLAYER_MAGE.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                   self.audio_files, self.data, self.switch_map, 'player_mage', self.alert)
                        self.selectedPlayer = "player_mage"
                        self.run()                        
                    if SELECT_PLAYER_ROGUE.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, 
                                   self.audio_files, self.data, self.switch_map, 'player_rogue', self.alert)
                        self.selectedPlayer = "player_rogue"
                        self.run()
                    if SELECT_BACK.checkForInput(SELECT_MOUSE_POS):
                        self.audio_files['click_button'].play()
                        self.menu()                        
            pygame.display.update()

if __name__ == "__main__":    
    main = Main()
    main.menu()

