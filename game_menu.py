import pygame

pygame.init()

# Создаём окно Pygame
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Menu')


def button_maker(text):
    # Создаем объект шрифта
    font_button = pygame.font.Font(None, 60)

    # Создайте поверхность для кнопки
    button_surface = pygame.Surface((300, 100))

    # Отображение текста на кнопке
    text_button = font_button.render(text, True, (255, 255, 0))
    text_rect = text_button.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    return button_surface, text_rect, text_button

# Создаем объект pygame.Rect, который представляет границы кнопки
play_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 75, 300, 100)
surf1, rect1, text1 = button_maker('Play')
surf2, rect2, text2 = button_maker('Quit')
running = True
while running:
    screen.fill((1, 1, 20))
    # Получаем события из очереди событий
    for event in pygame.event.get():
        # Проверьте событие выхода
        if event.type == pygame.QUIT:
            running = False
        # Проверяем событие нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button_rect.collidepoint(event.pos):
                print("Button play clicked!")
            elif quit_button_rect.collidepoint(event.pos):
                running = False
    # Показать текст кнопки
    surf1.blit(text1, rect1)
    surf2.blit(text2, rect2)
    # Нарисуйте кнопку на экране
    screen.blit(surf1, (play_button_rect.x, play_button_rect.y))
    screen.blit(surf2, (quit_button_rect.x, quit_button_rect.y))
    # Обновить состояние
    pygame.display.update()
# Тимур В.
