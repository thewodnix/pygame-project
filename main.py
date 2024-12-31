import pygame
import random

# Инициализация Pygame
pygame.init()

class Pacman:
    def __init__(self):
        self.x = COLS // 2
        self.y = ROWS // 2
        self.direction = (0, 0)
        self.score = 0

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.x %= COLS
        self.y %= ROWS

    def draw(self, surface):
        pygame.draw.circle(surface, 'yellow',
                           (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)


# Класс еды
class Food:
    def __init__(self):
        self.position = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

    def respawn(self):
        self.position = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

    def draw(self, surface):
        pygame.draw.rect(surface, 'white', (
        self.position[0] * CELL_SIZE + 5, self.position[1] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    pacman = Pacman()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman.direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            pacman.direction = (1, 0)
        elif keys[pygame.K_UP]:
            pacman.direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            pacman.direction = (0, 1)
        else:
            pacman.direction = (0, 0)

        pacman.move()

        if (pacman.x, pacman.y) == food.position:
            pacman.score += 1
            food.respawn()

        screen.fill('black')
        pacman.draw(screen)
        food.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
