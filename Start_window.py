import pygame
from load_sprites import load_image


def draw(screen):
    screen.fill((1, 1, 20))
    font = pygame.font.Font(None, 20)
    text = font.render("By Together_Team", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2 - 270
    text_y = height // 2 - text.get_height() // 2 + 60
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 200)
    text = font.render("PA   -MAN", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (255, 255, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


pygame.init()
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
running = True

clock = pygame.time.Clock()

font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 800)

font_text = pygame.font.SysFont(None, 40)
text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
show_text = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == font_fade:
            show_text = not show_text
    draw(screen)
    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()
    # создадим спрайт
    sprite = pygame.sprite.Sprite()
    for i in range(0, 7, +1):
        # определим его вид
        sprite.image = load_image('photo_menu_data', "ball.png")
        # вырезаем фон
        sprite.image.set_colorkey('WHITE')
        # и размеры
        sprite.rect = sprite.image.get_rect()
        # добавим спрайт в группу
        all_sprites.add(sprite)
        # размещаем спрайт на холсте
        sprite.rect.x = 100 * i
        sprite.rect.y = height // 2
        all_sprites.draw(screen)

    if show_text:
        screen.blit(text_surf, (width // 2 - 200, height // 1.2))
    pygame.display.flip()
    clock.tick(60)
    pygame.display.flip()
