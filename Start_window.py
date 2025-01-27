import pygame
from pygame import Rect
import itertools
from func import *
from load_sprites import load_image

# Создаём окно Pygame
pygame.init()

switchermus = itertools.cycle(['Black', 'Gray'])
switchercheats_ad = itertools.cycle(['On', 'Off'])
switchercheats_ad1 = itertools.cycle(['On', 'Off'])

while running:
    # Получаем события из очереди событий
    for event in pygame.event.get():
        # Проверьте событие выхода
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            cheat_code_flag = True

        # Проверяем событие нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu:
                if rect_cheat_code.collidepoint(event.pos):
                    sound_click.play()
                    menu = False
                    cheatc = True
                    clear_window()
                    print('cheat')

                if play_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    menu = False
                    clear_window()

                elif settings_button_rect.collidepoint(event.pos):
                    clear_window()
                    sound_click.play()
                    menu = False
                    draw_stngs(screen)
                    stngs = True

                elif quit_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    running = False

                if event.type == font_fade:
                    show_text = not show_text

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
            if cheat_code_flag:
                surf_cheat_code.blit(text_cheat_code, rect_cheat_code)
                screen.blit(surf_cheat_code, (cheat_code_button_rect.x, cheat_code_button_rect.y))
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

        surf_back_button.blit(text_back_button, rect_back_button)
        screen.blit(surf_back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if music_button_rect.collidepoint(event.pos):
                    surf_music.fill(next(switchermus))

                if back_button_rect.collidepoint(event.pos):
                    stngs = False
                    menu = True
                    print(1)

                elif quit_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    surf_cheat_code_dis
                    running = False
    if cheatc:
        draw_cheats(screen)
        surf_cheat_code_dis.blit(text_cheat_code_dis, rect_cheat_code_dis)
        screen.blit(surf_cheat_code_dis, (cheat_code_dis_button_rect.x, cheat_code_dis_button_rect.y))

        surf_cheat_code_col.blit(text_cheat_code_col, rect_cheat_code_col)
        screen.blit(surf_cheat_code_col, (cheat_code_dis_col_rect.x, cheat_code_dis_col_rect.y))

        surf_back_button.blit(text_back_button, rect_back_button)
        screen.blit(surf_back_button, (back_button_rect.x, back_button_rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cheat_code_dis_button_rect.collidepoint(event.pos):
                    surf_cheat_code_dis, rect_cheat_code_dis, text_cheat_code_dis \
                        = button_maker(next(switchercheats_ad), 150, 50, 60)

                if cheat_code_dis_col_rect.collidepoint(event.pos):
                    surf_cheat_code_col, rect_cheat_code_col, text_cheat_code_col \
                        = button_maker(next(switchercheats_ad1), 150, 50, 60)

                if back_button_rect.collidepoint(event.pos):
                    cheatc = False
                    menu = True

                elif quit_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    running = False

    pygame.display.flip()
