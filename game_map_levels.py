import pygame

level = int(input())
# Определение карты
with open(f'levels_data/level{level}_data', 'r', encoding='utf-8') as f:
    read_data = f.readlines()
map_ = read_data
# Инициализация Pygame
pygame.init()

if level == 1:
    # Размеры ячеек
    cell_size = 60
    # Создание отступа
    strip = 150

elif level == 2:
    cell_size = 34
    strip = 360

elif level == 3:
    cell_size = 25
    strip = 400

# Создание радиуса шариков
r = abs(6 - level)

# Установка размера окна
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('Tutorial')
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение экрана черным цветом
    screen.fill((1, 1, 20))

    # Отрисовка карты
    for row_index, row in enumerate(map_):
        for col_index, cell in enumerate(row.split(',')):
            if cell == 'x':
                pygame.draw.rect(screen, (0, 0, 255),
                                 (strip + col_index * cell_size, row_index * cell_size, cell_size, cell_size))
            elif cell == 'o':
                pygame.draw.rect(screen, (0, 0, 0),
                                 (strip + col_index * cell_size, row_index * cell_size, cell_size, cell_size))
                pygame.draw.circle(screen, (255, 255, 0), (
                    strip + col_index * cell_size + cell_size // 2, row_index * cell_size + cell_size // 2), r)
            elif cell == 'g':
                pygame.draw.rect(screen, (30, 10, 10),
                                 (strip + col_index * cell_size, row_index * cell_size, cell_size, cell_size))
            elif cell == 's':
                pygame.draw.rect(screen, (1, 1, 21),
                                 (strip + col_index * cell_size, row_index * cell_size, cell_size, cell_size))

    pygame.display.update()

pygame.quit()
# Тимур.В
