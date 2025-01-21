import pygame
from load_sprites import load_image

pygame.init()

# Создаём окно Pygame
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Level')
sound_click = pygame.mixer.Sound('music_data/music_menu_data/click_sound.mp3')
menu = False


def map_creation(level):
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
        cell_size = 25
        strip = 400

    elif level == 3:
        cell_size = 34
        strip = 360

    # Создание радиуса шариков
    r = abs(6 - level)
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


def image_downloader():
    screen.fill((1, 1, 20))
    image_level1 = load_image('photo_data/photo_level_selection', 'level1_image.png')
    image_l1 = pygame.transform.scale(image_level1, (250, 150))
    image_level2 = load_image('photo_data/photo_level_selection', 'level2_image.png')
    image_l2 = pygame.transform.scale(image_level2, (300, 300))
    image_level3 = load_image('photo_data/photo_level_selection', 'level3_image.png')
    image_l3 = pygame.transform.scale(image_level3, (300, 300))
    screen.blit(image_l1, (width // 3 - 360, height // 2 - 130))
    screen.blit(image_l2, (width // 2 - 150, height // 2 - 270))
    screen.blit(image_l3, (width - 425, height // 2 - 270))


def button_level_clicked_checker(pos):
    level = 0
    if fst_level_rect.collidepoint(pos):
        sound_click.play()
        level = 1
    elif snd_level_rect.collidepoint(pos):
        sound_click.play()
        level = 2
    elif trd_level_rect.collidepoint(pos):
        sound_click.play()
        level = 3
    return level


def shower_level_selection():
    # Показать текст кнопки
    surf_back.blit(text_back, rect_back)
    surf_fst_level.blit(fst_level_text, fst_level_back)
    surf_snd_level.blit(snd_level_text, snd_level_back)
    surf_trd_level.blit(trd_level_text, trd_level_back)
    # Нарисуйте кнопку на экране
    screen.blit(surf_back, (back_button_rect.x, back_button_rect.y))
    screen.blit(surf_fst_level, (fst_level_rect.x, fst_level_rect.y))
    screen.blit(surf_snd_level, (snd_level_rect.x, snd_level_rect.y))
    screen.blit(surf_trd_level, (trd_level_rect.x, trd_level_rect.y))
    # Обновить состояние
    pygame.display.update()


def button_maker(text, width, height, size):
    # Создаем объект шрифта
    font_button = pygame.font.Font(None, size)

    # Создайте поверхность для кнопки
    button_surface = pygame.Surface((width, height))

    # Отображение текста на кнопке
    text_button = font_button.render(text, True, (255, 255, 0), (0, 0, 0))
    text_rect = text_button.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    return button_surface, text_rect, text_button


# Создаем объект pygame.Rect, который представляет границы кнопки
back_button_rect = pygame.Rect(width // 2 - 100, height - 125, 200, 100)
fst_level_rect = pygame.Rect(width // 3 - 315, height // 2 + 50, 150, 50)
snd_level_rect = pygame.Rect(width // 2 - 75, height // 2 + 50, 150, 50)
trd_level_rect = pygame.Rect(width - 350, height // 2 + 50, 150, 50)
surf_back, rect_back, text_back = button_maker('Back', 200, 100, 75)
surf_fst_level, fst_level_back, fst_level_text = button_maker('1 Level', 150, 50, 50)
surf_snd_level, snd_level_back, snd_level_text = button_maker('2 Level', 150, 50, 50)
surf_trd_level, trd_level_back, trd_level_text = button_maker('3 Level', 150, 50, 50)

level = 0
level_selected = False
running = True
while running:
    # Получаем события из очереди событий
    for event in pygame.event.get():
        # Проверяем событие нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not menu:
                if not level_selected:
                    if back_button_rect.collidepoint(event.pos):
                        sound_click.play()
                        menu = True
                    level = button_level_clicked_checker(event.pos)
                    if level > 0:
                        level_selected = True
    if not menu:
        if level_selected:
            screen.fill((1, 1, 20))
            map_creation(level)
        else:
            image_downloader()
            shower_level_selection()
    else:
        screen.fill((1, 1, 20))
    pygame.display.flip()
# Тимур В.
