import pygame
import os
import sys
from load_sprites import load_image_special

pygame.init()
WIDTH, HEIGHT = 1500, 900
GAME_WIDTH = 600  # Игровая зона
INFO_WIDTH = WIDTH - GAME_WIDTH  # Обучение справа
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Обучение")

font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()
player_image = pygame.transform.scale(load_image_special('animation4.png', 'White'),
                                      (50, 50))
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.Surface((width, height))
        self.image.fill((249, 249, 249))
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 8
        self.gravity = 4
        self.jump_power = 10
        self.velocity_y = 0
        self.jumping = False

    def move(self, pos):
        if pos == 'left':
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x += self.speed
        elif pos == 'right':
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x -= self.speed
        elif pos == 'jump':
            self.velocity_y = -self.jump_power
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += self.jump_power

    def gravitation(self):
        self.rect.y += self.velocity_y
        self.velocity_y += 1

        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.velocity_y
            self.velocity_y = 0

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocity_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player(100, HEIGHT - 150)
Platform(200, 700)
Platform(400, 600)
Platform(200, 300)

instructions = [
    "ДОБРО ПОЖАЛОВАТЬ В ОБУЧЕНИЕ!",
    "Управление:",
    "- A - Движение влево",
    "- D - Движение вправо",
    "- SPACE - Прыжок (можно прыгать повторно)",
    "",
    "Попробуйте протестировать слева!",
    "Нажмите ESC для выхода."
]


def draw_text(text_list, x, y):
    for line in text_list:
        text_surface = font.render(line, True, 'black')
        screen.blit(text_surface, (x, y))
        y += 40


def game():
    running = True
    while running:
        screen.fill('white')

        pygame.draw.rect(screen, (162, 210, 255), (0, 0, GAME_WIDTH, HEIGHT))

        pygame.draw.rect(screen, (189, 224, 254), (GAME_WIDTH, 0, INFO_WIDTH, HEIGHT))
        draw_text(instructions, GAME_WIDTH + 100, 50)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move('left')
        if keys[pygame.K_d]:
            player.move('right')
        if keys[pygame.K_SPACE]:
            player.move('jump')
        player.gravitation()
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
        clock.tick(60)

    return True
