import pygame
from load_sprites import load_image

pygame.init()
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
animation_set = [load_image(f'photo_menu_data', f"Pac_manModel{i}.png", 'WHITE') for i in range(1, 4)]
pygame.display.set_caption('PAC-MAN')
sound1 = pygame.mixer.Sound('Voicy_Pac-Man Pellet Eaten.mp3')
clock = pygame.time.Clock()
x_pos = -90
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, height // 2))
        # добавляем в группу
        self.add(group)
        # у машин будет разная скорость

    def update(self):
        if self.rect.x == x_pos:
            self.kill()
            sound1.play()


def draw(screen, x):
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
    if len(all_sprites) != 4:
        for i in range(0, 7, +2):
            # создадим спрайт
            sprite = pygame.sprite.Sprite()
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
            all_sprites.update()
    all_sprites.draw(screen)
    for coord in all_sprites:
        if coord.rect.x - 50 == x:
            sound1.play()

coord_balls = []
running = True
font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 800)

font_text = pygame.font.SysFont(None, 40)
text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
show_text = True
k = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == font_fade:
            show_text = not show_text
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            running = False
    draw(screen, x_pos)
    if x_pos < width // 2 - 160:
        x_pos += 10
        image = animation_set[k // 20]
        image1 = pygame.transform.scale(image, (110, 110))
        screen.blit(image1, (x_pos, height // 2 - 63))
    else:
        image1 = pygame.transform.scale(animation_set[2], (110, 110))
        screen.blit(image1, (x_pos, height // 2 - 63))
        if show_text:
            screen.blit(text_surf, (width // 2 - 190, height // 1.2))
    k += 4
    if k == 60:
        k = 0
    clock.tick(60)
    # обновление состояния
    time_delta = clock.tick(60) / 1000.0
    pygame.display.flip()
