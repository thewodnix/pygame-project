import pygame
from const import *

pygame.init()
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


def draw_stngs(screen):
    screen.fill((1, 1, 20))
    font = pygame.font.Font('assets/fonts/title.ttf', 100)
    text = font.render("How to play", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - height * 0.4
    screen.blit(text, (text_x, text_y))
    text_w = text.get_width()
    text_h = text.get_height()


def draw_cheats(screen):
    screen.fill((1, 1, 20))
    font = pygame.font.Font('assets/fonts/title.ttf', 100)
    text = font.render("Cheats", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - height * 0.33
    screen.blit(text, (text_x, text_y))
    text_w = text.get_width()
    text_h = text.get_height()

    font1 = pygame.font.Font('assets/fonts/title.ttf', 50)
    text1 = font1.render("Dis Ghost", True, (255, 255, 0))
    text_x1 = width // 2 - text1.get_width() // 2 - 500
    text_y1 = height // 2 - text1.get_height() // 2 - height * 0.33 + 150
    screen.blit(text1, (text_x1, text_y1))
    text_w = text1.get_width()
    text_h = text1.get_height()

    font2 = pygame.font.Font('assets/fonts/title.ttf', 50)
    text2 = font2.render("immortal", True, (255, 255, 0))
    text_x2 = width // 2 - text1.get_width() // 2 - 500
    text_y2 = height // 2 - text1.get_height() // 2 - height * 0.33 + 250
    screen.blit(text2, (text_x2, text_y2))
    text_w = text1.get_width()
    text_h = text1.get_height()

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
surf_play, rect_play, text_play = button_maker('Play', 300, 100, 60)

quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 200, 300, 100)
surf_quit, rect_quit, text_quit = button_maker('Quit', 300, 100, 60)

settings_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 75, 300, 100)
surf_settings, rect_settings, text_settings = button_maker('How to play', 300, 100, 60)

music_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
surf_music, rect_music, text_music = button_maker('Music', 300, 100, 60)

cheat_code_button_rect = pygame.Rect(0, 0, 300, 100)
surf_cheat_code, rect_cheat_code, text_cheat_code = button_maker('Cheat', 150, 50, 60)

cheat_code_dis_button_rect = pygame.Rect(450, 265, 300, 100)
surf_cheat_code_dis, rect_cheat_code_dis, text_cheat_code_dis = button_maker('On', 150, 50, 60)

cheat_code_dis_col_rect = pygame.Rect(450, 365, 300, 100)
surf_cheat_code_col, rect_cheat_code_col, text_cheat_code_col = button_maker('On', 150, 50, 60)

back_button_rect = pygame.Rect(width // 2 - 150, 600, 300, 100)
surf_back_button, rect_back_button, text_back_button = button_maker('Back', 300, 100, 60)