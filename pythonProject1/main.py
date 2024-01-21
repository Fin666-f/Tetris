import pygame

import random

pygame.init()

BORDER_WIDTH = 750
BORDER_HEIGHT = 600

SCREEN_WIDTH = BORDER_WIDTH + 200
SCREEN_HEIGHT = BORDER_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
PURPLE = (139, 0, 255)

BLOCK_SIZE = 30

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

def new_figure():
    global current_figure, next_figure, current_x, current_y

    current_figure = next_figure
    next_figure = random.choice(FIGURES)

    # координаты фигуры, посередине экрана
    current_x = (BORDER_WIDTH // BLOCK_SIZE - len(current_figure[0])) // 2
    current_y = 0

    # пока что все белого цвета, серого когда упадут
    draw_figure(current_x, current_y, current_figure, WHITE)
    draw_interface()

    pygame.display.flip()

def check_collision(x, y, figure):
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j] and (x + j < 0 or x + j >= BORDER_WIDTH // BLOCK_SIZE or y + i >= BORDER_HEIGHT // BLOCK_SIZE or board.get((x + j, y + i))):
                return True
    return False

def add_figure_to_board(x, y, figure):
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j]:
                board[(x + j, y + i)] = 1

def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_figure(x, y, figure, color):
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j]:
                draw_block(x + j, y + i, color=color)

def draw_interface():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    inner_rect = (0, 0, BORDER_WIDTH, BORDER_HEIGHT)
    pygame.draw.rect(screen, PURPLE, inner_rect, 5)

board = {}
current_figure = random.choice(FIGURES)
next_figure = random.choice(FIGURES)
current_x = BORDER_WIDTH // 2 - len(current_figure[0]) * BLOCK_SIZE // 2
current_y = 0
score = 0

new_figure()

running = True
clock = pygame.time.Clock()

new_figure()

while running:
    print()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not check_collision(current_x - 1, current_y, current_figure):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not check_collision(current_x + 1, current_y, current_figure):
                    current_x += 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not check_collision(current_x, current_y + 1, current_figure):
                    current_y += 1
            elif event.key == pygame.K_SPACE:
                pass

    if not check_collision(current_x, current_y + 1, current_figure):
        current_y += 1
    else:
        add_figure_to_board(current_x, current_y, current_figure)
        new_figure()

    screen.fill(BLACK)

    for i in range(BORDER_HEIGHT // BLOCK_SIZE):
        for j in range(BORDER_WIDTH // BLOCK_SIZE):
            if board.get((j, i)):
                draw_block(j, i, GRAY)

    # проверка что за края экрана не улетело ничего
    if current_x < 0:
        current_x = 0
    elif current_x + len(current_figure[0]) > BORDER_WIDTH // BLOCK_SIZE:
        current_x = BORDER_WIDTH // BLOCK_SIZE - len(current_figure[0])
    if current_y + len(current_figure) > BORDER_HEIGHT // BLOCK_SIZE:
        current_y = BORDER_HEIGHT // BLOCK_SIZE - len(current_figure)

    draw_figure(current_x, current_y, current_figure, WHITE)
    draw_figure(BORDER_WIDTH // BLOCK_SIZE + 2, 2, next_figure, WHITE)
    draw_interface()

    pygame.display.flip()

    clock.tick(FALL_SPEED)
    pygame.display.update()

pygame.quit()
