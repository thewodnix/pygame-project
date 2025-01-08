import pygame
from load_sprites import load_image

# Создаём окно Pygame
pygame.init()
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
animation_set = [load_image(f'assets/photo_menu_data', f"Pac_manModel{i}.png", 'WHITE') for i in range(1, 4)]
pygame.display.set_caption('PAC-MAN')
sound_pac = pygame.mixer.Sound('1452.mp3')
sound_click = pygame.mixer.Sound('1452.mp3')
clock = pygame.time.Clock()

font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 800)
font_text = pygame.font.SysFont(None, 40)
show_text = True
text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
x_pos = -90


def clear_window():
    screen.fill((1, 1, 21))


def button_maker(text, width, height, size, font=None):
    # Создаем объект шрифта
    font_button = pygame.font.Font(font, size)

    # Создайте поверхность для кнопки
    button_surface = pygame.Surface((width, height))

    # Отображение текста на кнопке
    text_button = font_button.render(text, True, (255, 255, 0))
    text_rect = text_button.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    return button_surface, text_rect, text_button


# Создаем объект pygame.Rect, который представляет границы кнопки
play_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 200, 300, 100)
music_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
settings_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 75, 300, 100)
surf_play, rect_play, text_play = button_maker('Play', 300, 100, 60)
surf_quit, rect_quit, text_quit = button_maker('Quit', 300, 100, 60)
surf_settings, rect_settings, text_settings = button_maker('Settings', 300, 100, 60)
surf_music, rect_music, text_music = button_maker('Music', 300, 100, 60, 'assets/fonts/title.ttf')



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

def draw(screen):
    screen.fill((1, 1, 20))
    font = pygame.font.Font('assets/fonts/title.ttf', 200)
    text = font.render("Settings", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - height * 0.33
    screen.blit(text, (text_x, text_y))
    text_w = text.get_width()
    text_h = text.get_height()

coord_balls = [0, 200, 400, 600]
running = True
k = 0
menu_click = False
menu = True
stngs = False
while running:
    # Получаем события из очереди событий
    for event in pygame.event.get():
        # Проверьте событие выхода
        if event.type == pygame.QUIT:
            running = False
        # Проверяем событие нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu:
                if play_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    menu = False
                    clear_window()
                    print(1)
                elif settings_button_rect.collidepoint(event.pos):
                    clear_window()
                    sound_click.play()
                    menu = False
                    draw(screen)
                    stngs = True
                    print(2)
                elif quit_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    running = False
                    print(3)
                if event.type == font_fade:
                    show_text = not show_text
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    print(5)
                    menu_click = True
    if menu:
        if not menu_click:
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
            clock.tick(60)
            # обновление состояния
            time_delta = clock.tick(60) / 1000.0
        else:
            start_window_draw(screen)
            image = load_image('assets/photo_menu_data', 'Pac_manModel3.png', 'WHITE')
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

    if stngs:
        surf_music.blit(text_music, rect_music)
        screen.blit(surf_music, (music_button_rect.x, music_button_rect.y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if music_button_rect.collidepoint(event.pos):
                    print(1)

    pygame.display.flip()

