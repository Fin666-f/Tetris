import pygame

import random

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BLOCK_SIZE = 48

BORDER_WIDTH = BLOCK_SIZE * 14
BORDER_HEIGHT = BLOCK_SIZE * 20

X_WIN = (SCREEN_WIDTH - BORDER_WIDTH) // 2 // BLOCK_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
PURPLE = (139, 0, 255)

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


class Figure:
    def new_figure(self):
        self.current_figure = random.choice(FIGURES)
        self.next_figure = random.choice(FIGURES)

        # координаты фигуры, посередине экрана
        self.current_x = (SCREEN_WIDTH // BLOCK_SIZE - len(self.current_figure[0])) // 2
        self.current_y = 1

        self.next_x = SCREEN_WIDTH // BLOCK_SIZE + 2
        self.next_y = 2

        # пока что все белого цвета, серого когда упадут
        self.draw_figure(self.current_x, self.current_y, self.current_figure, WHITE)
        self.draw_figure(self.next_x, self.next_y, self.next_figure, WHITE)

        return self.current_figure, self.next_figure, self.current_x, self.current_y

    def draw_block(self, x, y, color):
        pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_figure(self, x, y, figure, color):
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if figure[i][j]:
                    self.draw_block(x + j, y + i, color=color)

    def add_figure_to_board(self, x, y, figure):
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if figure[i][j]:
                    board[(x + j, y + i)] = 1



class Interface:
    def draw_interface(self):
        #font = pygame.font.Font(None, 70)
        #text = font.render(f"Score: {score}", True, WHITE)
        #screen.blit(text, (30, 30))
        inner_rect = (X_WIN * BLOCK_SIZE, 0, BORDER_WIDTH, BORDER_HEIGHT)
        pygame.draw.rect(screen, PURPLE, inner_rect, 20)

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




interface = Interface()
figure = Figure()
board = {}
score = 0
running = True
clock = pygame.time.Clock()
image = pygame.image.load('kreml.png')


def remove_full_lines(blocks):
    global score
    ys = {}
    for key in board.keys():
        if board[key]:
            x, y = key
            if y in ys.keys():
                ys[y].append(x)
            else:
                ys[y] = [x]
    for y in ys.keys():
        #print(y, set(ys[y]))
        if len(set(ys[y])) == 14:
            score += 1
            print(1, board)

            for x in sorted(set(ys[y])):
                if (x, y) in board.keys():
                    keys = filter(lambda elem: elem[0] == x, board.keys())
                    keys = sorted(keys, key=lambda elem: elem[-1])
                    prev = 0
                    for key in keys:
                        del_x, del_y = key
                        if (del_x, del_y) in board.keys():
                            if board[(del_x, del_y)]:
                                print('do', board[(del_x, del_y)])
                                board[(del_x, del_y)], prev = prev, board[(del_x, del_y)]
                                print('po', board[(del_x, del_y)])

            print(2, board)



            print('hooray')
            print()

    ys = {}


current_figure, next_figure, current_x, current_y = figure.new_figure()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not interface.check_collision(current_x - 1, current_y, current_figure):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not interface.check_collision(current_x + 1, current_y, current_figure):
                    current_x += 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not interface.check_collision(current_x, current_y + 1, current_figure):
                    current_y += 1
            elif event.key == pygame.K_SPACE:
                pass


    if not interface.check_collision(current_x, current_y + 1, current_figure):
        current_y += 1
    else:
        figure.add_figure_to_board(current_x, current_y, current_figure)
        #lines_removed = remove_full_lines()
        #score += lines_removed ** 2

        current_figure, next_figure, current_x, current_y = figure.new_figure()
        remove_full_lines(board)

    screen.fill(BLACK)
    screen.blit(image, (0, 0))

    font = pygame.font.Font(None, 100)
    text = font.render(f"Score: {score}", True, PURPLE)
    screen.blit(text, (200, 120))


    for i in range(SCREEN_HEIGHT // BLOCK_SIZE):
        for j in range(SCREEN_WIDTH // BLOCK_SIZE):
            if board.get((j, i)):
                figure.draw_block(j, i, GRAY)
                if i == 1:
                    print('ppp')
                    exit()
                    pygame.quit()


    # проверка что за края экрана не улетело ничего
    if current_x < 0:
        current_x = 0
    elif current_x + len(current_figure[0]) > SCREEN_WIDTH // BLOCK_SIZE:
        current_x = SCREEN_WIDTH // BLOCK_SIZE - len(current_figure[0])
    if current_y + len(current_figure) > SCREEN_HEIGHT // BLOCK_SIZE:
        current_y = SCREEN_HEIGHT // BLOCK_SIZE - len(current_figure)

    figure.draw_figure(current_x, current_y, current_figure, WHITE)
    figure.draw_figure(SCREEN_WIDTH // BLOCK_SIZE + 2, 2, next_figure, WHITE)
    interface.draw_interface()

    pygame.display.flip()

    clock.tick(FALL_SPEED)

    pygame.display.update()

pygame.quit()
