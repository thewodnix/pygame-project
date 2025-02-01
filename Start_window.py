import pygame
from random import choice, random
from load_sprites import load_image_special
import os
import sys

# Создаём окно Pygame
pygame.init()
size = width, height = 1500, 900
tile_height, tile_width = 38, 38
screen = pygame.display.set_mode(size)
animation_set = [load_image_special(f'photo_menu_data/Pac_manModel{i}.png', 'WHITE') for i in range(1, 4)]
pygame.display.set_caption('PAC-MAN')
sound_pac = pygame.mixer.Sound('music_data/music_menu_data/Voicy_Pac-Man Pellet Eaten.mp3')
sound_click = pygame.mixer.Sound('music_data/music_menu_data/click_sound.mp3')
fps = 60
clock = pygame.time.Clock()
sound_click = pygame.mixer.Sound('music_data/music_menu_data/click_sound.mp3')
pick_up = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_sound.mp3')
pick_up_ammo = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_ammo_sound.mp3')
shot_sound = pygame.mixer.Sound('music_data/Game_sounds_data/gun_shot.mp3')
indentation_x = 200
indentation_y = 10


def clear_window():
    screen.fill((1, 1, 21))
    for i in all_sprites:
        i.kill()


restart_btn = pygame.Rect(width // 2 - width // 5, height // 2 - 50, 100, 100)


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def final_window(score, win_result, level):
    clear_window()
    image_restart = load_image_special('Final_window_photos/play_again_photo.png', 'black')
    image_restart_btn = pygame.transform.scale(image_restart, (200, 200))
    image_menu = load_image_special('Final_window_photos/menu.png', 'black')
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
                    game_main(level)
                    running = False
                elif menu_btn.collidepoint(event.pos):
                    sound_click.play()
                    level_selection_menu()
                    running = False
        screen.blit(text_res, (text_res_x, text_res_y))
        screen.blit(text, (text_x, text_y))
        screen.blit(image_restart_btn, (width // 2 - 250, height // 2 - 100, 200, 200))
        screen.blit(image_menu_btn, (width // 2 + 85, height // 2 - 100, 200, 200))
        pygame.display.flip()


image_wall = pygame.transform.scale(load_image_special('Game_photo_data/wall.png'), (38, 38))
ground_image = pygame.transform.scale(load_image_special('Game_photo_data/ground.png'), (38, 38))
passage_image = pygame.transform.scale(load_image_special('Game_photo_data/special_waLL.png'), (38, 38))
diamond_image = pygame.transform.scale(load_image_special('Game_photo_data/diamond.png', 'White'), (20, 20))
ammo_image = pygame.transform.scale(load_image_special('Game_photo_data/ammo.png', 'White'), (20, 20))
tile_images = {
    'wall': image_wall,
    'empty': ground_image,
    'passage': passage_image
}
player_image = pygame.transform.scale(load_image_special('animation4.png', 'White'),
                                      (30, 30))
redghost_image = pygame.transform.scale(load_image_special('Game_photo_data/red.png'), (30, 30))
orange_image = pygame.transform.scale(load_image_special('Game_photo_data/orange_ghost.png'), (30, 30))


class Crossroads(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, crossroads_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x, indentation_y + tile_height * pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(bullet_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = 0
        self.speed = 5
        self.image = pygame.transform.scale(
            load_image_special(f'Game_photo_data/bullet_{direction}.png', 'White'),
            (20, 20))
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
            indentation_x + tile_width * pos_x + 2, indentation_y + tile_height * pos_y + 12)


class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, diamond_group)
        self.image = diamond_image
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x + 5, indentation_y + tile_height * pos_y + 5)

    def get_position(self):
        return self.rect.x, self.rect.y


class Passage(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_pac_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x, indentation_y + tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_ghosts_group, tiles_pac_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x, indentation_y + tile_height * pos_y)


class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x, indentation_y + tile_height * pos_y)


class RedGhost(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(ghost_group, all_sprites)
        self.image = redghost_image
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * x_pos, indentation_y + tile_height * y_pos)
        self.speed = 4
        self.dir = choice(['right', 'left'])
        self.cell_size = 30
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
            self.rect.x += self.speed
        elif self.dir == 'up' and self.possible_moves(x, y - self.speed):
            self.rect.y -= self.speed
        elif self.dir == 'left' and self.possible_moves(x - self.speed, y):
            self.rect.x -= self.speed
        elif self.dir == 'down' and self.possible_moves(x, y + self.speed):
            self.rect.y += self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.gravity = 4
        self.score = 0
        self.image = player_image
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * pos_x, indentation_y + tile_height * pos_y)
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

    def target_reached(self):
        if self.alive:
            if pygame.sprite.spritecollideany(self, ghost_group):
                return True

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
                shot_sound.play()
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


class OrangeGhost(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(ghost_group, all_sprites)
        self.image = orange_image
        self.rect = self.image.get_rect().move(
            indentation_x + tile_width * x_pos + 15, indentation_y + tile_height * y_pos + 5)
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
                    pygame.transform.scale(load_image_special('Game_photo_data/orange_ghost.png'), (32, 32)),
                    True,
                    False)
            elif self.dir == 'left':
                self.image = pygame.transform.scale(load_image_special('Game_photo_data/orange_ghost.png'),
                                                    (32, 32))

            self.rect.x, self.rect.y = new_x, new_y


FPS = 50
# основной персонаж
player = None
# призраки
redghost = None

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


def generate_ghost(level):
    new_ghost, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'b':
                Ground('empty', x, y)
                new_ghost = RedGhost(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_ghost, x, y


def generate_ghost_orange(level):
    new_ghost, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'c':
                Ground('empty', x, y)
                new_ghost = OrangeGhost(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_ghost, x, y


def terminate():
    pygame.quit()
    sys.exit()


def game_main(level):
    player, level_x, level_y = generate_level(load_level(f'levels_data/level{level}_data'))
    redghost, level_x, level_y = generate_ghost(load_level(f'levels_data/level{level}_data'))
    orangeghost, level_x, level_y = generate_ghost_orange(load_level(f'levels_data/level{level}_data'))
    image_sprite = [load_image_special("animation1.png", 'white'),
                    load_image_special("animation2.png", 'white'),
                    load_image_special("animation3.png", 'white'),
                    load_image_special("animation4.png", 'white')]
    value = 0
    moving = False
    screen.fill((0, 0, 0))
    result = None
    total_score = 0
    while True:
        total_score = player.score_taker()
        clock.tick(FPS)
        player.diamond_pick_up()
        player.ammo_pick_up()
        result = player.win_result_taker()
        if player.target_reached() or result is True:
            final_window(total_score, result, level)
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
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    moving = False
                    value = 0
        if moving:
            value += 1
        if value >= len(image_sprite):
            value = 0
        image = image_sprite[value]
        image = pygame.transform.scale(image, (30, 30))
        screen.blit(image, (player.get_position()))
        keys = pygame.key.get_pressed()
        # Управление на ASD
        if keys[pygame.K_a]:
            player.move('left', 'pass')
            moving = True
        if keys[pygame.K_d]:
            player.move('right', 'pass')
            moving = True
        if keys[pygame.K_SPACE]:
            player.move('jump', 'pass')
        if keys[pygame.K_s]:
            player.move('down', 'pass')
            # pygame.mouse.set_visible(False)
        redghost.move_towards(target_x, target_y)
        orangeghost.move_towards(target_x, target_y)
        player.gravitation()
        # Обновление
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        tiles_ghosts_group.draw(screen)
        tiles_pac_group.draw(screen)
        pygame.display.flip()


def menu_shower():
    screen.fill((1, 1, 21))
    start_window_draw(screen)
    image = load_image_special('photo_menu_data/Pac_manModel3.png', 'WHITE')
    # рисуем спрайт
    image1 = pygame.transform.scale(image, (110, 110))
    screen.blit(image1, (width // 2 - 150, height // 2 - 63 - height * 0.33))
    # Показать текст кнопки
    surf_play.blit(text_play, rect_play)
    surf_quit.blit(text_quit, rect_quit)
    surf_settings.blit(text_settings, rect_settings)
    # Нарисуйте кнопку на экране
    screen.blit(surf_play, (play_button_rect.x, play_button_rect.y))
    screen.blit(surf_quit, (quit_button_rect.x, quit_button_rect.y))
    screen.blit(surf_settings, (settings_button_rect.x, settings_button_rect.y))
    # Обновить состояние
    pygame.display.update()


def image_downloader():
    screen.fill((1, 1, 21))
    image_level1 = load_image_special('photo_level_selection/level1_image.png')
    image_l1 = pygame.transform.scale(image_level1, (250, 150))
    image_level2 = load_image_special('photo_level_selection/level2_image.png')
    image_l2 = pygame.transform.scale(image_level2, (300, 300))
    image_level3 = load_image_special('photo_level_selection/level3_image.png')
    image_l3 = pygame.transform.scale(image_level3, (300, 300))
    screen.blit(image_l1, (width // 3 - 360, height // 2 - 120))
    screen.blit(image_l2, (width // 2 - 150, height // 2 - 270))
    screen.blit(image_l3, (width - 425, height // 2 - 270))


def button_level_clicked_checker(pos):
    level = 0
    if fst_level_rect.collidepoint(pos):
        sound_click.play()
        level = 1
    elif snd_level_rect.collidepoint(pos):
        sound_click.play()
        level = 2
    elif trd_level_rect.collidepoint(pos):
        sound_click.play()
        level = 3
    return level


def level_selection_menu():
    running = True
    while running:
        image_downloader()
        # Получаем события из очереди событий
        for event in pygame.event.get():
            # Проверьте событие выхода
            if event.type == pygame.QUIT:
                running = False
            # Проверяем событие нажатия кнопки мыши
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    start_menu()
                    running = False
                level = button_level_clicked_checker(event.pos)
                if level > 0:
                    game_main(level)
                    running = False
        shower_level_selection()
        clock.tick(fps)
        pygame.display.flip()


def shower_level_selection():
    # Показать текст кнопки
    surf_back.blit(text_back, rect_back)
    surf_fst_level.blit(fst_level_text, fst_level_back)
    surf_snd_level.blit(snd_level_text, snd_level_back)
    surf_trd_level.blit(trd_level_text, trd_level_back)
    # Нарисуйте кнопку на экране
    screen.blit(surf_back, (back_button_rect.x, back_button_rect.y))
    screen.blit(surf_fst_level, (fst_level_rect.x, fst_level_rect.y))
    screen.blit(surf_snd_level, (snd_level_rect.x, snd_level_rect.y))
    screen.blit(surf_trd_level, (trd_level_rect.x, trd_level_rect.y))


def button_maker(text, width, height, size):
    # Создаем объект шрифта
    font_button = pygame.font.Font(None, size)

    # Создайте поверхность для кнопки
    button_surface = pygame.Surface((width, height))

    # Отображение текста на кнопке
    text_button = font_button.render(text, True, (255, 255, 0), (0, 0, 0))
    text_rect = text_button.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    return button_surface, text_rect, text_button


# Создаем объект pygame.Rect, который представляет границы кнопки
back_button_rect = pygame.Rect(width // 2 - 100, height - 125, 200, 100)
fst_level_rect = pygame.Rect(width // 3 - 315, height // 2 + 50, 150, 50)
snd_level_rect = pygame.Rect(width // 2 - 75, height // 2 + 50, 150, 50)
trd_level_rect = pygame.Rect(width - 350, height // 2 + 50, 150, 50)
surf_back, rect_back, text_back = button_maker('Back', 200, 100, 75)
surf_fst_level, fst_level_back, fst_level_text = button_maker('1 Level', 150, 50, 50)
surf_snd_level, snd_level_back, snd_level_text = button_maker('2 Level', 150, 50, 50)
surf_trd_level, trd_level_back, trd_level_text = button_maker('3 Level', 150, 50, 50)
play_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 100)
quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 200, 300, 100)
settings_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 75, 300, 100)
surf_play, rect_play, text_play = button_maker('Play', 300, 100, 60)
surf_quit, rect_quit, text_quit = button_maker('Quit', 300, 100, 60)
surf_settings, rect_settings, text_settings = button_maker('Settings', 300, 100, 60)


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


def start_menu():
    running = True
    while running:
        # Получаем события из очереди событий
        for event in pygame.event.get():
            # Проверьте событие выхода
            if event.type == pygame.QUIT:
                running = False
                # screen.fill((1, 1, 20))
            # Проверяем событие нажатия кнопки мыши
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    level_selection_menu()
                    running = False
                elif settings_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    clear_window()
                    running = False
                elif quit_button_rect.collidepoint(event.pos):
                    sound_click.play()
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    clear_window()
        menu_shower()
        # Обновить состояние
        pygame.display.flip()


def start_window():
    font_fade = pygame.USEREVENT + 1
    pygame.time.set_timer(font_fade, 800)
    font_text = pygame.font.SysFont(None, 40)
    show_text = True
    text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
    x_pos = -90
    coord_balls = [0, 200, 400, 600]
    running = True
    k = 0
    menu = False
    counter_monitors = 0
    while running:
        # Получаем события из очереди событий
        for event in pygame.event.get():
            # Проверьте событие выхода
            if event.type == pygame.QUIT:
                running = False
                # Проверяем событие нажатия кнопки мыши
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                clear_window()
                menu = True
        if menu:
            start_menu()
            running = False
        else:
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
            # обновление состояния
            time_delta = clock.tick(60) / 1000.0
            if counter_monitors > 20:
                show_text = not show_text
                counter_monitors = 0
            counter_monitors += 1
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    start_window()

# Тимур В.
