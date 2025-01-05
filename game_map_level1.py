import pygame

# Размеры ячеек
cell_size = 30

# Определение карты
map_ = [
    'x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x',
    'x,o,o,o,o,x,o,o,o,o,o,o,o,o,x,o,o,o,o,x',
    'x,o,x,x,o,x,o,x,x,x,x,x,x,o,x,o,x,x,o,x',
    'x,o,x,o,o,o,o,o,o,o,o,o,o,o,o,o,o,x,o,x',
    'x,o,x,o,x,x,o,x,x,o,o,x,x,o,x,x,o,x,o,x',
    'x,o,o,o,o,o,o,x,o,o,o,o,x,o,o,o,o,o,o,x',
    'x,o,x,o,x,x,o,x,x,x,x,x,x,o,x,x,o,x,o,x',
    'x,o,x,o,o,o,o,o,o,o,o,o,o,o,o,o,o,x,o,x',
    'x,o,x,x,o,x,o,x,x,x,x,x,x,o,x,o,x,x,o,x',
    'x,o,o,o,o,x,o,o,o,o,o,o,o,o,x,o,o,o,o,x',
    'x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x'
]

# Инициализация Pygame
pygame.init()

# Установка размера окна
sc = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Tutorial')
clock = pygame.time.Clock()

running = True  

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение экрана черным цветом
    sc.fill((0, 0, 0))

    # Отрисовка карты
    for row_index, row in enumerate(map_):
        for col_index, cell in enumerate(row.split(',')):
            if cell == 'x':
                pygame.draw.rect(sc, (255, 255, 255), (col_index * cell_size, row_index * cell_size, cell_size, cell_size))
            elif cell == 'o':
                pygame.draw.rect(sc, (100, 100, 100), (col_index * cell_size, row_index * cell_size, cell_size, cell_size))

    pygame.display.update()

pygame.quit()
#Тимур.В