import pygame
import sys
import os

pygame.init()
# размеры окна:
tile_width = tile_height = 50
size = width, height = tile_width * 20, tile_height * 11
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pick_up = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_sound.mp3')
pick_up_ammo = pygame.mixer.Sound('music_data/Game_sounds_data/pick_up_ammo_sound.mp3')
shot_sound = pygame.mixer.Sound('music_data/Game_sounds_data/gun_shot.mp3')


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
redghost_image = pygame.transform.scale(load_image('photo_data/Game_photo_data/red.png'), (32, 32))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(bullet_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = 2
        self.image = pygame.transform.scale(load_image(f'photo_data/Game_photo_data/bullet_{direction}.png', 'White'),
                                            (30, 30))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.direction = direction
        print(ghost_group)
        self.gun_shot_maker()

    def gun_shot_maker(self):
        if self.direction == 'right':
            for n in range(80):
                if n <= 40:
                    self.rect.x += self.speed
                    if pygame.sprite.spritecollideany(self, tiles_pac_group):
                        self.rect.x -= self.speed
                        break
        elif self.direction == 'left':
            for n in range(80):
                if n <= 40:
                    self.rect.x -= self.speed
                    if pygame.sprite.spritecollideany(self, tiles_pac_group):
                        self.rect.x += self.speed
                        break
        elif self.direction == 'down':
            for n in range(80):
                if n <= 40:
                    self.rect.y += self.speed
                    if pygame.sprite.spritecollideany(self, tiles_pac_group):
                        self.rect.y -= self.speed
                        break
        elif self.direction == 'up':
            for n in range(80):
                if n <= 40:
                    self.rect.y -= self.speed
                    if pygame.sprite.spritecollideany(self, tiles_pac_group):
                        self.rect.y += self.speed
                        break
                    elif pygame.sprite.spritecollideany(self, ghost_group):
                        for g in ghost_group:
                            if pygame.sprite.spritecollideany(g, bullet_group):
                                g.kill()
                                break
                        break

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


# class Pathfinder:
#     def __init__(self, in_arr):
#         cost = np.array(in_arr, dtype=np.bool_).tolist()
#         self.pf = tcod.path.AStar(cost=cost, diagonal=0)
#
#     def get_path(self, from_x, from_y, to_x, to_y):
#         res = self.pf.get_path(from_x, from_y, to_x, to_y)
#         return [(s[1], s[0]) for s in res]


class RedGhost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ghost_group, all_sprites)
        self.image = redghost_image
        self.rect = self.image.get_rect().move(
            tile_width * 8 + 15, tile_height * 5 + 5)
        self.pos = pos_x, pos_y
        self.speed = 4
        self.cell_size = 50
        self.target_x = 0
        self.target_y = 0
        self.alive = True

    def get_position(self):
        return self.rect.x, self.rect.y

    def is_alive(self):
        print()

    def move_towards(self, target_x, target_y, player_direction):
        target_ways = []
        self.rect.x += self.speed
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.x -= self.speed
        else:
            target_ways.append(((self.rect.x - target_x) ** 2 + (self.rect.y - target_y) ** 2) ** 0.5)
            self.rect.x -= self.speed
        self.rect.x -= self.speed
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.x += self.speed
        else:
            target_ways.append(((target_x - self.rect.x) ** 2 + (target_y - self.rect.y) ** 2) ** 0.5)
            self.rect.x += self.speed
        self.rect.y -= self.speed
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.y += self.speed
        else:
            target_ways.append(((target_x - self.rect.x) ** 2 + (target_y - self.rect.y) ** 2) ** 0.5)
            self.rect.y += self.speed
        self.rect.y += self.speed
        if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
            self.rect.y -= self.speed
        else:
            target_ways.append(((target_x - self.rect.x) ** 2 + (target_y - self.rect.y) ** 2) ** 0.5)
            self.rect.y -= self.speed
        min_value = min(target_ways)
        if player_direction == 'right':
            if min_value == (((target_x - self.rect.x - self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x -= self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y + self.speed) ** 2) ** 0.5):
                self.rect.y -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y += self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y - self.speed) ** 2) ** 0.5):
                self.rect.y += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y -= self.speed
        elif player_direction == 'left':
            if min_value == (((target_x - self.rect.x + self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x += self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y + self.speed) ** 2) ** 0.5):
                self.rect.y -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y += self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y - self.speed) ** 2) ** 0.5):
                self.rect.y += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y -= self.speed
        elif player_direction == 'jump':
            if min_value == (((target_x - self.rect.x + self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x += self.speed
            elif min_value == (((target_x - self.rect.x - self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x -= self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y + self.speed) ** 2) ** 0.5):
                self.rect.y -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y += self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y - self.speed) ** 2) ** 0.5):
                self.rect.y += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y -= self.speed
        elif player_direction == 'down':
            if min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y - self.speed) ** 2) ** 0.5):
                self.rect.y += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y -= self.speed
            elif min_value == (((target_x - self.rect.x) ** 2 + (
                    target_y - self.rect.y + self.speed) ** 2) ** 0.5):
                self.rect.y -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.y += self.speed
            elif min_value == (((target_x - self.rect.x + self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x += self.speed
            elif min_value == (((target_x - self.rect.x - self.speed) ** 2 + (
                    target_y - self.rect.y) ** 2) ** 0.5):
                self.rect.x += self.speed
                if pygame.sprite.spritecollideany(self, tiles_ghosts_group):
                    self.rect.x -= self.speed
        if pygame.sprite.spritecollideany(self, player_group):
            print('game over')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.gravity = 4
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 10 + self.gravity)
        self.jumpCount = 0
        self.speed = 8
        self.ammo_count = 0
        self.x = self.rect.x
        self.y = self.rect.y

    def get_position(self):
        return self.rect.x, self.rect.y

    def gravitation(self):
        self.rect.y += self.gravity
        if pygame.sprite.spritecollideany(self, tiles_pac_group):
            self.rect.y -= self.gravity

    def move(self, pos, direction):
        if pos == 'left':
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tiles_pac_group):
                self.rect.x += self.speed
        elif pos == 'shot':
            if self.ammo_count:
                Bullet(self.rect.x, self.rect.y, direction)
                self.ammo_count -= 1
            else:
                print('zero ammo')
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
                    pick_up.play()
                    i.kill()
                    break

    def ammo_pick_up(self):
        if pygame.sprite.spritecollideany(self, ammo_group):
            for i in ammo_group:
                if pygame.sprite.spritecollideany(i, player_group):
                    pick_up_ammo.play()
                    self.ammo_count += 1
                    i.kill()
                    break
        # for i in diamond_group: красиво удаляет кристаллы
        #     print(i.kill())
        #     break


# class OrangeGhost(pygame.sprite.Sprite):  # Класс оранжевого призрака
#     def __inait__(self, pos_x, pos_y):
#         """инициализатор класса"""
#         self.direction = 'up'
#         self.x, self.y = pos_x, pos_y
#         self.delay = 200
#         self.image = pygame.image.load('photo_data/Game_photo_data/orange_ghost.png')
#         self.image1 = pygame.transform.scale(self.image, (24, 24))
#         self.count = 0
#         # pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)
#
#     # вспомогательные методы, возвращающие информацию о положении призрака / выставляющие эти значения
#     def get_position(self):
#         return self.x, self.y
#
#     def set_position(self, position):
#         self.x, self.y = position
#
#     def get_direction(self):
#         return self.direction
#
#     def set_direction(self, direction):
#         self.direction = direction
#
#     #
#     # def update_image(self):
#     #     """метод обновления текстуры призрака"""
#     #     self.image = pygame.image.load(f'characters/orange/{self.direction}{self.count % 2}.png')
#     #     self.image1 = pygame.transform.scale(self.image, (24, 24))
#     #     self.count += 1
#
#     def render(self, screen):
#         """метод рендера призрака на экран"""
#         delta = (self.image1.get_width() - tile_width) // 2
#         screen.blit(self.image1, (self.x * tile_width - delta, self.y * tile_width - delta))
#
#     def move_orange(self):
#         pac_pos = Player().get_position()
#         """метод перемещения оранжевого призрака"""
#         x = abs(pac_pos.get_position()[0] - self.get_position()[0])
#         y = abs(pac_pos.get_position()[1] - self.get_position()[1])
#         distance = round((x ** 2 + y ** 2) ** 0.5)
#         if distance >= 8:
#             next_position = self.labyrinth.find_path_step(self.orange.get_position(),
#                                                           pac_pos.get_position(),
#                                                           self.orange.get_direction())
#         else:
#             next_position = self.labyrinth.find_path_step(self.orange.get_position(),
#                                                           (1, 13), self.orange.get_direction())
#         self.orange.set_direction(find_direction(self.orange.get_position(), next_position))
#         self.orange.set_position(next_position)
#         self.orange.update_image()


FPS = 50
# основной персонаж
player = None
# призраки
redghost = None

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
            elif level[y][x] == 'g':
                Ground('empty', x, y)
                blinki = RedGhost(x, y)
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
            if level[y][x] == 's':
                Ground('empty', x - 1, y)
                new_ghost = RedGhost(x, y)
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
    redghost, level_x, level_y = generate_ghost(load_level('levels_data/level1_data'))
    screen.fill((0, 0, 0))
    last_direction = ''
    while True:
        clock.tick(FPS)
        player.diamond_pick_up()
        player.ammo_pick_up()
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
        redghost.move_towards(target_x, target_y, last_direction)
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
