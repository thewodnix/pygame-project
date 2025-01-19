import pygame
import random
import os
import sys

pygame.init()
width, height = 1280, 720
pygame.mixer.init()
pygame.display.set_caption('Pygame_template')
screen = pygame.display.set_mode((width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# assets
player_img = load_image('photo_data/photo_menu_data/Pac_manModel3.png')
player_left_img = player_img
player_right_img = player_img


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (width / 2, height)
        self.isJump = False
        self.jumpCount = 10

    def update(self):
        keys = pygame.key.get_pressed()
        self.image = player_img

        if (keys[pygame.K_LEFT]) and (self.rect.x >= 0):
            self.rect.x -= 5
            self.image = player_left_img
            self.image.set_colorkey("White")

        if (keys[pygame.K_RIGHT]) and (self.rect.x <= 1145):
            self.rect.x += 5
            self.image = player_right_img
            self.image.set_colorkey(0)

        if keys[pygame.K_SPACE]:
            self.isJump = True

        if self.isJump is True:

            if self.jumpCount >= -10:

                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) // 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) // 2

                self.jumpCount -= 1

            else:
                self.isJump = False
                self.jumpCount = 10


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill((156, 113, 58))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
