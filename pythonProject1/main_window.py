import sys
import pygame
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Main_window:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Main window')
        self.fps = 50
        with open('Tetris_data.txt', 'r', encoding='utf8') as f:
            data = ''.join(f.readlines()).split('\n')
        self.language = data[0]
        self.record = data[1]
        f.close
        with open('Tetris_control.txt', 'r', encoding='utf8') as f:
            data = ''.join(f.readlines()).split('\n')
        self.count_left = data[0]
        self.count_right = data[1]
        self.count_down = data[2]
        f.close

    def load_image(self, name):
        if self.language == 'english':
            s = 'eng_font'
        else:
            s = 'rus_font'
        fullname = os.path.join(s, name)
        image = pygame.image.load(fullname)
        return image

    def button(self, name):
        if name == 'down':
            name = self.count_down
            s = 'down_buttons'
        elif name == 'left':
            name = self.count_left
            s = 'left_buttons'
        else:
            name = self.count_right
            s = 'right_buttons'
        fullname = os.path.join(s, name + '.png')
        image = pygame.image.load(fullname)
        return image

    def data(self, change_language=False, change_record=False):
        if change_language:
            if self.language == 'english':
                self.language = 'russian'
            else:
                self.language = 'english'
        if change_record:
            pass
        f1 = open('Tetris_data.txt', 'w', encoding='utf8')
        f1.write('\n'.join([self.language, self.record]))

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
            if (pos[0] >= ((SCREEN_WIDTH - 1440) // 2) and pos[0] <= ((SCREEN_WIDTH - 1440) // 2 + 1440) and
                    pos[1] >= 360 and pos[1] <= 480):
                self.count_left = str((int(self.count_left) + 1) % 3)
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 500 and pos[1] <= 620):
                self.count_right = str((int(self.count_right) + 1) % 3)
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 640 and pos[1] <= 760):
                self.count_down = str((int(self.count_down) + 1) % 3)
                return True
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 780 and pos[1] <= 900):
                return False

    def render_control_screen(self):
        fon = pygame.transform.scale(pygame.image.load('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(fon, (0, 0))
        font_tetris = self.load_image('control.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 1440) // 2, 100))
        font_tetris = self.button('left')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 360))
        font_tetris = self.load_image('left.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 360))
        font_tetris = self.button('right')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 500))
        font_tetris = self.load_image('right.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 500))
        font_tetris = self.button('down')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 640))
        font_tetris = self.load_image('down.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 640))
        font_tetris = self.load_image('back.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 780))

    def save_control(self):
        f1 = open('Tetris_control.txt', 'w', encoding='utf8')
        f1.write('\n'.join([self.count_left, self.count_right, self.count_down]))

    def control(self):
        self.render_control_screen()
        run = True
        self.continue_run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.continue_run = self.prosses_control(event.pos, event.button)
                    self.save_control()
                    self.render_control_screen()
            if not self.continue_run:
                self.start_screen()
                run = False
            pygame.display.flip()
            self.clock.tick(self.fps)

    def prosses_start_screen(self, pos, button):
        if button == 1:
            if (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 360 and pos[1] <= 480):
                self.run_game()
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 500 and pos[1] <= 620):
                self.control()
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 640 and pos[1] <= 760):
                self.data(True, False)
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 780 and pos[1] <= 900):
                self.terminate()

    def render_main_screen(self):
        fon = pygame.transform.scale(pygame.image.load('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(fon, (0, 0))
        font_tetris = pygame.image.load('Textis.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 1440) // 2, 100))
        font_tetris = self.load_image('play.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 360))
        font_tetris = self.load_image('control_1.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 500))
        font_tetris = self.load_image('language.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 640))
        font_tetris = self.load_image('exit.png')
        self.screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 780))

    def start_screen(self):
        self.render_main_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.prosses_start_screen(event.pos, event.button)
            self.render_main_screen()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    main = Main_window()
    main.start_screen()