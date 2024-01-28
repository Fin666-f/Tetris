import sys
import pygame
import os
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BLOCK_SIZE = 52

BORDER_WIDTH = BLOCK_SIZE * 14
BORDER_HEIGHT = BLOCK_SIZE * 20

X_WIN = (SCREEN_WIDTH - BORDER_WIDTH) // 2 // BLOCK_SIZE

COLORS = ['White', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink']
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

FALL_SPEED = 3  # скорость падения фигур. оптимальная 3-5

FIGURES = [
    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]]
]

blocks = {}
ys = {}
board = {}
score = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Figure:
    def new_figure(self):
        self.current_figure = random.choice(FIGURES)
        self.next_figure = random.choice(FIGURES)

        # координаты фигуры, посередине экрана
        self.current_x = (SCREEN_WIDTH // BLOCK_SIZE - len(self.current_figure[0])) // 2
        self.current_y = 1

        self.next_x = SCREEN_WIDTH // BLOCK_SIZE + 2
        self.next_y = 2

        self.current_color = random.choice(COLORS)
        self.next_color = random.choice(COLORS)

        # пока что все белого цвета, серого когда упадут
        self.draw_figure(self.current_x, self.current_y, self.current_figure, self.current_color)
        self.draw_figure(self.next_x, self.next_y, self.next_figure, self.next_color)

        return self.current_figure, self.next_figure, self.current_x, self.current_y, self.next_y, self.current_color

    def load_image(self, color, dark=False):
        name = color + '_Block.png'
        if dark:
            s = 'Dark_Color_block'
            name = 'Dark_' + name
        else:
            s = 'Color_block'
        fullname = os.path.join(s, name)
        return fullname

    def draw_block(self, x, y, color, dark=False):
        if not dark:
            color_block = self.load_image(color)
        else:
            color_block = self.load_image(color, True)
        fon = pygame.transform.scale(pygame.image.load(color_block), (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(fon, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    def draw_figure(self, x, y, figure, color):
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if figure[i][j]:
                    self.draw_block(x + j, y + i, color)

    def add_figure_to_board(self, x, y, figure):
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if figure[i][j]:
                    board[(x + j, y + i)] = 1


class Interface:
    def __init__(self, language):
        self.language = language

    def draw_interface(self):
        if self.language == 'russian':
            name = 'scores_rus.png'
        else:
            name = 'scores_eng.png'
        score = pygame.image.load(name)
        screen.blit(score, (40, 100))
        pattern = pygame.image.load('pattern.png')
        screen.blit(pattern, (542, 0))
        inner_rect = (X_WIN * BLOCK_SIZE, 0, BORDER_WIDTH, BORDER_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), inner_rect, 1)

    def check_collision(self, x, y, figure):
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if figure[i][j] and (x + j < X_WIN or x + j >= X_WIN + BORDER_WIDTH // BLOCK_SIZE or
                                      y + i >= BORDER_HEIGHT // BLOCK_SIZE or board.get((x + j, y + i))):
                    if y in blocks.keys():
                        blocks[y].append(x)
                    else:
                        blocks[y] = [x]
                    return True
        return False

    def remove_full_lines(self, blocks):
        global score
        for key in board.keys():
            if board[key]:
                x, y = key
                if y in ys.keys():
                    ys[y].append(x)
                else:
                    ys[y] = [x]
        for y in ys.keys():
            print(y, set(ys[y]))
            if len(set(ys[y])) == 14:
                score += 1

                for x in sorted(set(ys[y])):
                    if (x, y) in board.keys():
                        keys = filter(lambda elem: elem[0] == x, board.keys())
                        keys = sorted(keys, key=lambda elem: elem[-1])
                        prev = 0
                        for key in keys:
                            del_x, del_y = key
                            if (del_x, del_y) in board.keys():
                                if board[(del_x, del_y)]:
                                    board[(del_x, del_y)], prev = prev, board[(del_x, del_y)]


class Main_window:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')
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

    def data(self, change_language=False):
        if change_language:
            if self.language == 'english':
                self.language = 'russian'
            else:
                self.language = 'english'
        f1 = open('Tetris_data.txt', 'w', encoding='utf8')
        f1.write('\n'.join([self.language, self.record]))

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run_game(self):
        self.game_over = False
        run = True
        interface = Interface(self.language)
        figure = Figure()
        clock = pygame.time.Clock()
        image = pygame.image.load('church_Blazhenov.png')
        pygame.mixer.music.load('Tetris Theme (Korobeiniki) [Orchestral Cover] (256  kbps).mp3')
        pygame.mixer.music.play(-1)

        current_figure, next_figure, current_x, current_y, next_y, current_color = figure.new_figure()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if ((event.key == pygame.K_LEFT and self.count_left == '2') or (event.key == pygame.K_a and
                                self.count_left == '1') or (event.key == pygame.K_z and self.count_left == '0')):
                        print(self.count_left)
                        if not interface.check_collision(current_x - 1, current_y, current_figure):
                            current_x -= 1
                    elif ((event.key == pygame.K_RIGHT and self.count_right == '2') or (event.key == pygame.K_d and
                                self.count_right == '1') or (event.key == pygame.K_c and self.count_right == '0')):
                        if not interface.check_collision(current_x + 1, current_y, current_figure):
                            current_x += 1
                    elif ((event.key == pygame.K_DOWN and self.count_down == '2') or (event.key == pygame.K_s and
                                self.count_down == '1') or (event.key == pygame.K_x and self.count_down == '0')):
                        if not interface.check_collision(current_x, current_y + 1, current_figure):
                            current_y += 1

            if not interface.check_collision(current_x, current_y + 1, current_figure):
                current_y += 1
            else:
                figure.add_figure_to_board(current_x, current_y, current_figure)
                # lines_removed = remove_full_lines()
                # score += lines_removed ** 2

                current_figure, next_figure, current_x, current_y, next_y, current_color = figure.new_figure()
                interface.remove_full_lines(board)

            screen.fill(BLACK)
            screen.blit(image, (0, 0))

            font = pygame.font.Font(None, 70)
            text = font.render(str(score), True, (255, 255, 255))
            screen.blit(text, (140, 190))

            for i in range(SCREEN_HEIGHT // BLOCK_SIZE):
                for j in range(SCREEN_WIDTH // BLOCK_SIZE):
                    if board.get((j, i)):
                        figure.draw_block(j, i, current_color)

            if current_y == 1 and next_y == 2:
                self.game_over = True
                pygame.mixer.music.pause()
                self.start_screen()
                run = False

            # проверка что за края экрана не улетело ничего
            if current_x < 0:
                current_x = 0
            elif current_x + len(current_figure[0]) > SCREEN_WIDTH // BLOCK_SIZE:
                current_x = SCREEN_WIDTH // BLOCK_SIZE - len(current_figure[0])
            if current_y + len(current_figure) > SCREEN_HEIGHT // BLOCK_SIZE:
                current_y = SCREEN_HEIGHT // BLOCK_SIZE - len(current_figure)


            figure.draw_figure(current_x, current_y, current_figure, current_color)
            figure.draw_figure(SCREEN_WIDTH // BLOCK_SIZE + 2, 2, next_figure, current_color)
            interface.draw_interface()

            pygame.display.flip()

            clock.tick(FALL_SPEED)
            pygame.display.update()

    def prosses_control(self, pos, button):
        if button == 1:
            if (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
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
            else:
                return True

    def render_control_screen(self):
        fon = pygame.transform.scale(pygame.image.load('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fon, (0, 0))
        font_tetris = self.load_image('control.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 1440) // 2, 100))
        font_tetris = self.button('left')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 360))
        font_tetris = self.load_image('left.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 360))
        font_tetris = self.button('right')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 500))
        font_tetris = self.load_image('right.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 500))
        font_tetris = self.button('down')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2 + 884, 640))
        font_tetris = self.load_image('down.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 640))
        font_tetris = self.load_image('back.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 780))

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
                elif event.type == pygame.QUIT:
                    self.terminate()
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
                self.data(True)
            elif (pos[0] >= ((SCREEN_WIDTH - 864) // 2) and pos[0] <= ((SCREEN_WIDTH - 864) // 2 + 864) and
                    pos[1] >= 780 and pos[1] <= 900):
                self.terminate()

    def render_main_screen(self):
        fon = pygame.transform.scale(pygame.image.load('kreml.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fon, (0, 0))
        font_tetris = pygame.image.load('Textis.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 1440) // 2, 100))
        font_tetris = self.load_image('play.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 360))
        font_tetris = self.load_image('control_1.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 500))
        font_tetris = self.load_image('language.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 640))
        font_tetris = self.load_image('exit.png')
        screen.blit(font_tetris, ((SCREEN_WIDTH - 864) // 2, 780))

    def start_screen(self):
        self.render_main_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.prosses_start_screen(event.pos, event.button)
                elif event.type == pygame.QUIT:
                    self.terminate()
            self.render_main_screen()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    main = Main_window()
    main.start_screen()