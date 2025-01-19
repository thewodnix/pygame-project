import pygame
import sys
import os

pygame.init()
# размеры окна:
tile_width = tile_height = 50
size = width, height = 1500, 800
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


image_wall = pygame.transform.scale(load_image('photo_data/Game_photo_data/wall.png'), (50, 50))
ground_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/ground.png'), (50, 50))
passage_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/special_waLL.png'), (50, 50))
tile_images = {
    'wall': image_wall,
    'empty': ground_image,
    'passage': passage_image
}
player_image = load_image('photo_data/photo_menu_data/Pac_manModel3.png')


class Passage(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y
        self.isJump = False
        self.jumpCount = 10

    def move(self, pos):
        if pos == 'left':
            self.rect.x -= 5
        elif pos == 'jump':
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
        # elif pos == 'down':
        #     x, y = x, y + 1
        elif pos == 'right':
            self.rect.x += 5
        if pygame.sprite.spritecollideany(self, tiles_group):
            return


FPS = 50
# основной персонаж
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'o':
                Ground('empty', x, y)
            elif level[y][x] == 'g':
                Ground('empty', x, y)
            elif level[y][x] == 'x':
                Tile('wall', x, y)
            elif level[y][x] == 'p':
                Passage('passage', x, y)
            elif level[y][x] == 's':
                Ground('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def game_main():
    player, level_x, level_y = generate_level(load_level('levels_data/level1_data'))
    screen.fill((0, 0, 0))
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.move('jump')
        keys = pygame.key.get_pressed()
        # Управление на WASD
        if keys[pygame.K_a]:
            player.move('left')
        if keys[pygame.K_d]:
            player.move('right')
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        #     player.move('down')
            pygame.mouse.set_visible(False)
        # Обноение
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        tiles_group.draw(screen)
        pygame.display.flip()


# start_screen()
game_main()
