from setting import *
from pytmx.util_pygame import load_pygame  # pip install pytmx
from os.path import join
from data import *
from sprites import *


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('TF2D World')
        self.clock_tick = pygame.time.Clock()


    def import_assets(self):
        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'hit': pygame.mixer.Sound(join('..', 'audio', 'hit.wav')),
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')),
            'bg_music': pygame.mixer.Sound(join('..', 'audio', 'starlight_city.mp3'))
        }
    def run(self):
        while True:
            dt = self.clock_tick.tick(60) / 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
