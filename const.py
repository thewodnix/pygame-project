import pygame
from load_sprites import load_image

pygame.init()
coord_balls = [0, 200, 400, 600]
running = True
k = 0
menu_click = False
menu = True
stngs = False
cheatc = False
cheat_code_flag = False

size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
animation_set = [load_image(f'assets/photo_menu_data', f"Pac_manModel{i}.png", 'WHITE') for i in range(1, 4)]
pygame.display.set_caption('PAC-MAN')
sound_pac = pygame.mixer.Sound('pick_up_ammo_sound.mp3')
sound_click = pygame.mixer.Sound('pick_up_ammo_sound.mp3')
clock = pygame.time.Clock()

font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 800)
font_text = pygame.font.SysFont(None, 40)
show_text = True
text_surf = font_text.render('press  any  button  to  start', True, (255, 255, 0))
x_pos = -90

