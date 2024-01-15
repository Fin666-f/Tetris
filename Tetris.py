import pygame

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


def render(screen):
    #Клетчатое поле
    s = 53
    for i in range(20):
        y = 10 + s * i
        for j in range(10):
            x = 695 + s * j
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), (x, y, s, s), 1)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), (20, 20, s * 6, s * 4), 3)
    #Подсчёт очков
    font = pygame.font.Font(None, 90)
    text = font.render('SCORE:', True, (255, 255, 255))
    screen.blit(text, (60, 60))
    count = 0
    text = font.render(f'{count}', True, (255, 255, 255))
    screen.blit(text, (60, 150))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    render(screen)
    pygame.display.flip()

pygame.quit()