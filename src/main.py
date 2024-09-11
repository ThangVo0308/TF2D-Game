from setting import  *
from pytmx.util_pygame import load_pygame # pip install pytmx
from os.path import join


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('TF2D World')
        self.clock_tick = pygame.time.Clock()

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


