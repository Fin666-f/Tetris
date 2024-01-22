import sys
import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Main_window:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Main window')
        self.fps = 50

    def load_image(self, name):
        image = pygame.image.load(name)
        return image

    def language(self):
        pass

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run_game(self):
        self.game_over = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.game_over += 1
            if self.game_over == 5:
                self.start_screen()
                run = False
            self.screen.fill(pygame.Color('blue'))
            pygame.display.flip()
            self.clock.tick(self.fps)

    def prosses_control(self, pos, button):
        if button == 1:
            if (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 360 and pos[1] <= 480):
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 500 and pos[1] <= 620):
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 640 and pos[1] <= 760):
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 780 and pos[1] <= 900):
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                  pos[1] >= 920 and pos[1] <= 1040):
                return False

    def control(self):
        fon = pygame.transform.scale(self.load_image('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(fon, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 800) // 2, 100, 800, 200), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 360, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 500, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 640, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 780, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 920, 600, 120), 10)
        run = True
        self.continue_run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.continue_run = self.prosses_control(event.pos, event.button)
            if not self.continue_run:
                self.start_screen()
                run = False
            pygame.display.flip()
            self.clock.tick(self.fps)

    def prosses_start_screen(self, pos, button):
        if button == 1:
            if (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 360 and pos[1] <= 480):
                self.run_game()
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 500 and pos[1] <= 620):
                self.control()
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 640 and pos[1] <= 760):
                self.language()
            elif (pos[0] >= ((SCREEN_WIDTH - 600) // 2) and pos[0] <= ((SCREEN_WIDTH - 600) // 2 + 600) and
                    pos[1] >= 780 and pos[1] <= 900):
                self.terminate()

    def start_screen(self):
        fon = pygame.transform.scale(self.load_image('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(fon, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 800) // 2, 100, 800, 200), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 360, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 500, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 640, 600, 120), 10)
        pygame.draw.rect(self.screen, (255, 255, 255), ((SCREEN_WIDTH - 600) // 2, 780, 600, 120), 10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.prosses_start_screen(event.pos, event.button)
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    main = Main_window()
    main.start_screen()