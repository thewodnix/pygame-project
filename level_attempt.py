from random import choice, randint, random

import pygame
import sys
import os

pygame.init()
# размеры окна:
tile_width = tile_height = 50
size = width, height = tile_width * 20, tile_height * 11
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
sound_click = pygame.mixer.Sound('music_data/music_menu_data/click_sound.mp3')
clock = pygame.time.Clock()
pick_up = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_sound.mp3')
pick_up_ammo = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_ammo_sound.mp3')
shot_sound = pygame.mixer.Sound('music_data/Game_sounds_data/gun_shot.mp3')


def clear_window():
    screen.fill((1, 1, 21))
    for i in all_sprites:
        i.kill()


restart_btn = pygame.Rect(width // 2 - width // 5, height // 2 - 50, 100, 100)


def final_window(score, win_result):
    clear_window()
    image_restart = load_image('photo_data/Final_window_photos/play_again_photo.png', 'black')
    image_restart_btn = pygame.transform.scale(image_restart, (200, 200))
    image_menu = load_image('photo_data/Final_window_photos/menu.png', 'black')
    image_menu_btn = pygame.transform.scale(image_menu, (200, 200))

    restart_btn = pygame.Rect(width // 2 - 250, height // 2 - 100, 200, 200)
    surf_restart = pygame.Surface((width, height))
    menu_btn = pygame.Rect(width // 2 + 85, height // 2 - 100, 200, 200)
    surf_menu = pygame.Surface((width, height))
    font_res = pygame.font.Font(None, 65)
    if not win_result:
        text_res = font_res.render(f"You lost!", True, (255, 255, 0))
    else:
        text_res = font_res.render(f"Congratulations! You won", True, (255, 255, 0))
    text_res_x = width // 2 - text_res.get_width() // 2
    text_res_y = height // 2 - text_res.get_height() // 2 - height * 0.33
    font = pygame.font.Font(None, 45)
    text = font.render(f"You collected {score} points", True, (255, 255, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 + text.get_height() // 2 + height * 0.33
    running = True
    while running:
        for event in pygame.event.get():
            screen.fill((1, 1, 21))
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_btn.collidepoint(event.pos):
                    sound_click.play()
                    game_main()
                elif menu_btn.collidepoint(event.pos):
                    sound_click.play()
                    print('menu')
        screen.blit(text_res, (text_res_x, text_res_y))
        screen.blit(text, (text_x, text_y))
        screen.blit(image_restart_btn, (width // 2 - 250, height // 2 - 100, 200, 200))
        screen.blit(image_menu_btn, (width // 2 + 85, height // 2 - 100, 200, 200))
        pygame.display.flip()


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
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


image_wall = pygame.transform.scale(load_image('photo_data/Game_photo_data/wall.png'), (50, 50))
ground_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/ground.png'), (50, 50))
passage_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/special_waLL.png'), (50, 50))
diamond_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/diamond.png', 'White'), (20, 20))
ammo_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/ammo.png', 'White'), (30, 30))
tile_images = {
    'wall': image_wall,
    'empty': ground_image,
    'passage': passage_image
}
player_image = load_image('photo_data/photo_menu_data/Pac_manModel3.png', 'White')
redghost_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/red.png'), (35, 35))
orange_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/orange_ghost.png'), (35, 35))


class Crossroads(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, crossroads_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(bullet_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = 0
        self.speed = 5
        self.image = pygame.transform.scale(load_image(f'photo_data/Game_photo_data/bullet_{direction}.png', 'White'),
                                            (30, 30))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.direction = direction
        self.gun_shot_maker()

    def gun_shot_maker(self):
        while True:
            if self.direction == 'right':
                self.rect.x += self.speed
                if pygame.sprite.spritecollideany(self, tiles_pac_group):
                    self.rect.x -= self.speed
                    break
                collided_ghost = pygame.sprite.spritecollideany(self, ghost_group)
                if collided_ghost:
                    collided_ghost.is_alive()  # Удаляем призрака
                    self.score += 250
                    self.kill()  # Удаляем пулю
                    break
                if self.rect.x > width:  # Выход за пределы экрана
                    self.kill()  # Удаляем пулю
                    break

            elif self.direction == 'left':
                self.rect.x -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_pac_group):
                    self.rect.x += self.speed
                    break
                collided_ghost = pygame.sprite.spritecollideany(self, ghost_group)
                if collided_ghost:
                    collided_ghost.is_alive()  # Удаляем призрака
                    self.score += 250
                    self.kill()  # Удаляем пулю
                    break
                if self.rect.x < 0:  # Выход за пределы экрана
                    self.kill()  # Удаляем пулю
                    break

            elif self.direction == 'down':
                self.rect.y += self.speed
                if pygame.sprite.spritecollideany(self, tiles_pac_group):
                    self.rect.y -= self.speed
                    break
                collided_ghost = pygame.sprite.spritecollideany(self, ghost_group)
                if collided_ghost:
                    collided_ghost.is_alive()
                    self.score += 250
                    self.kill()
                    break
                if self.rect.y > height:
                    self.kill()
                    break

            elif self.direction == 'up':
                self.rect.y -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_pac_group):
                    self.rect.y += self.speed
                    break
                collided_ghost = pygame.sprite.spritecollideany(self, ghost_group)
                if collided_ghost:
                    collided_ghost.is_alive()  # Удаляем призрака
                    self.score += 250
                    self.kill()  # Удаляем пулю
                    break
                if self.rect.y < 0:  # Выход за пределы экрана
                    self.kill()  # Удаляем пулю
                    break
        return self.score

        # for b_s in bullet_group:
        #     b_s.kill()


class Ammo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, ammo_group)
        self.image = ammo_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 2, tile_height * pos_y + 12)


class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, diamond_group)
        self.image = diamond_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 25)

    def get_position(self):
        return self.rect.x, self.rect.y


class Passage(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_pac_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_ghosts_group, tiles_pac_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class RedGhost(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(ghost_group, all_sprites)
        self.image = redghost_image
        self.rect = self.image.get_rect().move(
            tile_width * x_pos + 15, tile_height * y_pos + 5)
        self.speed = 4
        self.dir = choice(['right', 'left'])
        self.cell_size = 50
        self.target_x = 0
        self.target_y = 0
        self.move_possibility = True
        self.count_attempts = 0
        self.alive = True

    def get_position(self):
        return self.rect.x, self.rect.y

    def is_alive(self):
        self.alive = False
        self.kill()

    def possible_moves(self, *coord) -> bool:
        x, y = self.rect.x, self.rect.y
        self.rect.x, self.rect.y = coord
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.x, self.rect.y = x, y
            return False
        self.rect.x, self.rect.y = x, y
        return True

    def move_towards(self, target_x, target_y):
        self.target_reached()
        target_ways = []
        x, y = self.rect.x, self.rect.y
        if self.dir == 'right' and pygame.sprite.spritecollideany(self, crossroads_group):
            if self.possible_moves(x, y - self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y - self.speed) ** 2) ** 0.5), 'up'))
            if self.possible_moves(x, y + self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y + self.speed) ** 2) ** 0.5), 'down'))
            if self.possible_moves(x + self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x + self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'right'))
        if self.dir == 'left' and pygame.sprite.spritecollideany(self, crossroads_group):
            if self.possible_moves(x, y - self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y - self.speed) ** 2) ** 0.5), 'up'))
            if self.possible_moves(x, y + self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y + self.speed) ** 2) ** 0.5), 'down'))
            if self.possible_moves(x - self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x - self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'left'))
        if self.dir == 'down' and pygame.sprite.spritecollideany(self, crossroads_group):
            if self.possible_moves(x, y + self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y + self.speed) ** 2) ** 0.5), 'down'))
            if self.possible_moves(x + self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x + self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'right'))
            if self.possible_moves(x - self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x - self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'left'))
        if self.dir == 'up' and pygame.sprite.spritecollideany(self, crossroads_group):
            if self.possible_moves(x, y - self.speed):
                target_ways.append(
                    ((((self.rect.x - target_x) ** 2 + (self.rect.y - target_y - self.speed) ** 2) ** 0.5), 'up'))
            if self.possible_moves(x + self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x + self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'right'))
            if self.possible_moves(x - self.speed, y):
                target_ways.append(
                    ((((self.rect.x - target_x - self.speed) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5), 'left'))
        if pygame.sprite.spritecollideany(self, crossroads_group) and self.move_possibility:
            self.count_attempts += 1
            if self.count_attempts == 10:
                self.count_attempts = 0
                self.dir = min(target_ways)[1]
        if self.dir == 'right' and self.possible_moves(x + self.speed, y):
            self.image = pygame.transform.flip(
                pygame.transform.scale(load_image('photo_data/Game_photo_data/red.png'), (40, 40)), True, False)
            self.rect.x += self.speed
        elif self.dir == 'up' and self.possible_moves(x, y - self.speed):
            self.rect.y -= self.speed
        elif self.dir == 'left' and self.possible_moves(x - self.speed, y):
            self.image = pygame.transform.scale(load_image('photo_data/Game_photo_data/red.png'), (40, 40))
            self.rect.x -= self.speed
        elif self.dir == 'down' and self.possible_moves(x, y + self.speed):
            self.rect.y += self.speed

    def target_reached(self):
        if self.alive:
            if pygame.sprite.spritecollideany(self, player_group):
                return True


class OrangeGhost(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(ghost_group, all_sprites)
        self.image = orange_image
        self.rect = self.image.get_rect().move(
            tile_width * x_pos + 15, tile_height * y_pos + 5)
        self.speed = 4
        self.dir = choice(['right', 'left'])
        self.cell_size = 50
        self.target_x = 0
        self.target_y = 0
        self.move_possibility = True
        self.count_attempts = 0
        self.alive = True

    def get_position(self):
        return self.rect.x, self.rect.y

    def is_alive(self):
        self.alive = False
        self.kill()

    def possible_moves(self, *coord) -> bool:
        x, y = self.rect.x, self.rect.y
        self.rect.x, self.rect.y = coord
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.x, self.rect.y = x, y
            return False
        self.rect.x, self.rect.y = x, y
        return True

    def move_towards(self, target_x, target_y):
        self.target_reached()
        target_ways = []
        x, y = self.rect.x, self.rect.y

        directions = {
            'up': (x, y - self.speed),
            'down': (x, y + self.speed),
            'left': (x - self.speed, y),
            'right': (x + self.speed, y)
        }

        if pygame.sprite.spritecollideany(self, crossroads_group):
            for direction, (new_x, new_y) in directions.items():
                if self.possible_moves(new_x, new_y):
                    distance = ((new_x - target_x) ** 2 + (new_y - target_y) ** 2) ** 0.5
                    target_ways.append((distance, direction))

            if target_ways:
                if random() < 0.2:
                    self.dir = choice([way[1] for way in target_ways])
                else:
                    self.dir = min(target_ways)[1]

        new_x, new_y = directions[self.dir]
        if self.possible_moves(new_x, new_y):
            if self.dir == 'right':
                self.image = pygame.transform.flip(
                    pygame.transform.scale(load_image('photo_data/Game_photo_data/orange_ghost.png'), (40, 40)), True,
                    False)
            elif self.dir == 'left':
                self.image = pygame.transform.scale(load_image('photo_data/Game_photo_data/orange_ghost.png'), (40, 40))

            self.rect.x, self.rect.y = new_x, new_y

    def target_reached(self):
        if self.alive:
            if pygame.sprite.spritecollideany(self, player_group):
                return True


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.gravity = 4
        self.score = 0
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 10 + self.gravity)
        self.jumpCount = 0
        self.speed = 8
        self.ammo_count = 0
        self.x = self.rect.x
        self.win_result = False
        self.y = self.rect.y

    def get_position(self):
        return self.rect.x, self.rect.y

    def gravitation(self):
        self.rect.y += self.gravity
        if pygame.sprite.spritecollideany(self, tiles_pac_group):
            self.rect.y -= self.gravity

    def win_checker(self):
        if len(diamond_group) == 0:
            self.win_result = True

    def move(self, pos, direction):
        if pos == 'left':
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tiles_pac_group):
                self.rect.x += self.speed
        elif pos == 'shot':
            if self.ammo_count:
                bullet = Bullet(self.rect.x, self.rect.y, direction)
                self.score += bullet.gun_shot_maker()
                self.ammo_count -= 1
            else:
                pass
        elif pos == 'jump':
            for i in range(20):  # Delay the falling down as loops are very fast
                if i <= 10:
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(self, tiles_pac_group):
                        self.rect.y += 1
        elif pos == 'down':
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, tiles_pac_group):
                self.rect.y -= self.speed
        elif pos == 'right':
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, tiles_pac_group):
                self.rect.x -= self.speed

    def diamond_pick_up(self):
        if pygame.sprite.spritecollideany(self, diamond_group):
            for i in diamond_group:
                if pygame.sprite.spritecollideany(i, player_group):
                    self.score += 5
                    pick_up.play()
                    i.kill()
                    self.win_checker()
                    break

    def ammo_pick_up(self):
        if pygame.sprite.spritecollideany(self, ammo_group):
            for i in ammo_group:
                if pygame.sprite.spritecollideany(i, player_group):
                    pick_up_ammo.play()
                    self.score += 10
                    self.ammo_count += 1
                    i.kill()
                    break

    def score_taker(self):
        return self.score

    def win_result_taker(self):
        return self.win_result
        # for i in diamond_group: красиво удаляет кристаллы
        #     print(i.kill())
        #     break


FPS = 50
# основной персонаж
player = None
# призраки
redghost = None
oragneghost = None

crossroads_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
tiles_pac_group = pygame.sprite.Group()
tiles_ghosts_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'o':
                Ground('empty', x, y)
                Diamond(x, y)
            elif level[y][x] == 'r':
                Crossroads('empty', x, y)
                Diamond(x, y)
            elif level[y][x] == 'g':
                Ground('empty', x, y)
            elif level[y][x] == 'x':
                Tile('wall', x, y)
            elif level[y][x] == 'a':
                Ground('empty', x, y)
                Ammo(x, y)
            elif level[y][x] == 'p':
                Passage('passage', x, y)
            elif level[y][x] == 's':
                Ground('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_ghost_red(level):
    new_ghost, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'k':
                Ground('empty', x, y)
                new_ghost = RedGhost(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_ghost, x, y


def generate_ghost_orange(level):
    new_ghost, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'k':
                Ground('empty', x, y)
                new_ghost = OrangeGhost(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_ghost, x, y


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
    redghost, level_x, level_y = generate_ghost_red(load_level('levels_data/level1_data'))
    oragneghost, level_x, level_y = generate_ghost_orange(load_level('levels_data/level1_data'))
    screen.fill((0, 0, 0))
    result = None
    total_score = 0
    while True:
        total_score = player.score_taker()
        clock.tick(FPS)
        player.diamond_pick_up()
        player.ammo_pick_up()
        result = player.win_result_taker()
        if redghost.target_reached() or result is True:
            final_window(total_score, result)
            terminate()
        if oragneghost.target_reached() or result is True:
            final_window(total_score, result)
            terminate()
        target_x, target_y = player.get_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move('shot', 'up')
                elif event.key == pygame.K_DOWN:
                    player.move('shot', 'down')
                elif event.key == pygame.K_RIGHT:
                    player.move('shot', 'right')
                elif event.key == pygame.K_LEFT:
                    player.move('shot', 'left')
        keys = pygame.key.get_pressed()
        # Управление на WASD
        if keys[pygame.K_a]:
            player.move('left', 'pass')
            last_direction = 'left'
        if keys[pygame.K_d]:
            player.move('right', 'pass')
            last_direction = 'right'
        if keys[pygame.K_SPACE]:
            player.move('jump', 'pass')
            last_direction = 'jump'
        if keys[pygame.K_s]:
            player.move('down', 'pass')
            last_direction = 'down'
            # pygame.mouse.set_visible(False)
        redghost.move_towards(target_x, target_y)
        oragneghost.move_towards(target_x, target_y)
        player.gravitation()
        # Обновление
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        tiles_ghosts_group.draw(screen)
        tiles_pac_group.draw(screen)
        pygame.display.flip()


# start_screen()
game_main()
