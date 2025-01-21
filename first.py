import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
# размеры окна:
size = width, height = 300, 300
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
x_mouse, y_mouse = 0, 0
all_sprites = pygame.sprite.Group()
# создадим спрайт
sprite = pygame.sprite.Sprite()
# определим его вид
sprite.image = load_image("img.png")
# и размеры
sprite.rect = sprite.image.get_rect()
# добавим спрайт в группу
all_sprites.add(sprite)

class Mouse(pygame.sprite.Sprite):
    image = load_image("img.png")

    def __init__(self):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.image = Mouse.image
        self.rect = self.image.get_rect()

    def movement(self, pos):
        pygame.mouse.set_visible(False)
        x, y = pos
        sprite.rect.x = x
        sprite.rect.y = y


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            Mouse().movement(event.pos)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
