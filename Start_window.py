import pygame
from load_sprites import load_image

# Создаём окно Pygame
pygame.init()
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
animation_set = [load_image(f'photo_data/photo_menu_data', f"Pac_manModel{i}.png", 'WHITE') for i in range(1, 4)]
pygame.display.set_caption('PAC-MAN')
sound_pac = pygame.mixer.Sound('music_data/music_menu_data/Voicy_Pac-Man Pellet Eaten.mp3')
sound_click = pygame.mixer.Sound('music_data/music_menu_data/click_sound.mp3')
fps = 60
clock = pygame.time.Clock()

font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 800)
font_text = pygame.font.SysFont(None, 40)
show_text = True
text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
x_pos = -90

x_mouse, y_mouse = 0, 0
mouse_sprites = pygame.sprite.Group()
# создадим спрайт
sprite = pygame.sprite.Sprite()
# определим его вид
sprite.image = load_image('data', "img.png")
# и размеры
sprite.rect = sprite.image.get_rect()
# добавим спрайт в группу
mouse_sprites.add(sprite)


class Mouse(pygame.sprite.Sprite):
    image = load_image('data', "img.png")

    def __init__(self):
        # Вызываем конструктор родительского класса Sprite.
        super().__init__()
        self.image = Mouse.image
        self.rect = self.image.get_rect()

    def movement(self, pos):
        pygame.mouse.set_visible(False)
        x, y = pos
        sprite.rect.x = x
        sprite.rect.y = y


def menu_shower():
    start_window_draw(screen)
    image = load_image('photo_data/photo_menu_data', 'Pac_manModel3.png', 'WHITE')
    # рисуем спрайт
    image1 = pygame.transform.scale(image, (110, 110))
    screen.blit(image1, (width // 2 - 150, height // 2 - 63 - height * 0.33))
    # Показать текст кнопки
    surf_play.blit(text_play, rect_play)
    surf_quit.blit(text_quit, rect_quit)
    surf_settings.blit(text_settings, rect_settings)
    # Нарисуйте кнопку на экране
    screen.blit(surf_play, (play_button_rect.x, play_button_rect.y))
    screen.blit(surf_quit, (quit_button_rect.x, quit_button_rect.y))
    screen.blit(surf_settings, (settings_button_rect.x, settings_button_rect.y))
    # Обновить состояние
    pygame.display.update()


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


def clear_window():
    screen.fill((1, 1, 21))


def start_window_draw(screen):
    screen.fill((1, 1, 20))
    font = pygame.font.Font(None, 20)
    text = font.render("By VORFIL Team", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2 - 270
    text_y = height // 2 - text.get_height() // 2 + 60 - height * 0.33
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 200)
    text = font.render("PA   -MAN", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - height * 0.33
    screen.blit(text, (text_x, text_y))
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 255, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


# Создаем объект pygame.Rect, который представляет границы кнопки
back_button_rect = pygame.Rect(width // 2 - 100, height - 125, 200, 100)
fst_level_rect = pygame.Rect(width // 3 - 315, height // 2 + 50, 150, 50)
snd_level_rect = pygame.Rect(width // 2 - 75, height // 2 + 50, 150, 50)
trd_level_rect = pygame.Rect(width - 350, height // 2 + 50, 150, 50)
surf_back, rect_back, text_back = button_maker('Back', 200, 100, 75)
surf_fst_level, fst_level_back, fst_level_text = button_maker('1 Level', 150, 50, 50)
surf_snd_level, snd_level_back, snd_level_text = button_maker('2 Level', 150, 50, 50)
surf_trd_level, trd_level_back, trd_level_text = button_maker('3 Level', 150, 50, 50)

play_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 200, 300, 100)
settings_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 75, 300, 100)
surf_play, rect_play, text_play = button_maker('Play', 300, 100, 60)
surf_quit, rect_quit, text_quit = button_maker('Quit', 300, 100, 60)
surf_settings, rect_settings, text_settings = button_maker('Settings', 300, 100, 60)

level = 0
level_selected = False
coord_balls = [0, 200, 400, 600]
running = True
k = 0
menu_click = False
menu = True
level_selection_flag = False
counter_monitors = 0
while running:
    # Получаем события из очереди событий
    for event in pygame.event.get():
        # Проверьте событие выхода
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            Mouse().movement(event.pos)
            # screen.fill((1, 1, 20))
        # Проверяем событие нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not level_selection_flag:
                if menu:
                    if play_button_rect.collidepoint(event.pos):
                        sound_click.play()
                        menu = False
                        level_selection_flag = True
                        clear_window()
                    elif settings_button_rect.collidepoint(event.pos):
                        sound_click.play()
                        clear_window()
                    elif quit_button_rect.collidepoint(event.pos):
                        sound_click.play()
                        running = False
                    if event.type == font_fade:
                        show_text = not show_text
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        clear_window()
                        menu_click = True
            else:
                if not menu:
                    if not level_selected:
                        if back_button_rect.collidepoint(event.pos):
                            sound_click.play()
                            menu = True
                            level_selection_flag = False
                        level = button_level_clicked_checker(event.pos)
                        if level > 0:
                            level_selected = True
    if menu:
        if menu_click is False:
            start_window_draw(screen)
            if x_pos < width // 2 - 150:
                x_pos += 10
                image = animation_set[k // 20]
                image1 = pygame.transform.scale(image, (110, 110))
                screen.blit(image1, (x_pos, height // 2 - 63 - height * 0.33))
                for coord in coord_balls:
                    if coord - 50 == x_pos:
                        sound_pac.play()
            else:
                image1 = pygame.transform.scale(animation_set[2], (110, 110))
                screen.blit(image1, (x_pos, height // 2 - 63 - height * 0.33))
                if show_text:
                    screen.blit(text_surf, (width // 2 - 190, height // 1.2))
            k += 4
            if k == 60:
                k = 0
            # обновление состояния
            time_delta = clock.tick(60) / 1000.0
        else:
            menu_shower()
            # Обновить состояние
            pygame.display.update()
    if not menu:
        if level_selected:
            screen.fill((1, 1, 20))
            map_creation(level)
        else:
            image_downloader()
            shower_level_selection()
    if counter_monitors > 20:
        show_text = not show_text
        counter_monitors = 0
    mouse_sprites.draw(screen)
    mouse_sprites.update()
    counter_monitors += 1
    clock.tick(fps)
    pygame.display.flip()
    # Тимур В.
