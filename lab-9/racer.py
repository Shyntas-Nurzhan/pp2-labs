import pygame
from pygame.locals import *
import sys
import random

pygame.init()

# --- Настройки экрана и ресурсов ---
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RACER")
background = pygame.image.load("AnimatedStreet.png")

# --- Цвета и шрифты ---
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# --- Переменные ---
done = False
coin_score = 0
FPS = pygame.time.Clock()

# --- Классы ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > screen_height:
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game-coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        self.rect.move_ip(0, 7)
        if self.rect.top > screen_height:
            self.reset_position()

    def reset_position(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, screen_width - 40), 0)


# --- Создание объектов ---
player = Player()

enemies = pygame.sprite.Group()
enemies.add(Enemy())

coins = pygame.sprite.Group()
for _ in range(3):  # Три монеты
    coins.add(Coin())

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(coins)

# --- Главный игровой цикл ---
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    # Отображение очков
    score_display = font_small.render(f"Coins: {coin_score}", True, BLACK)
    screen.blit(score_display, (10, 10))

    # Движение объектов
    player.move()
    for enemy in enemies:
        enemy.move()
    for coin in coins:
        coin.move()

    # Проверка на столкновение с врагами
    if pygame.sprite.spritecollideany(player, enemies):
        screen.fill(WHITE)
        screen.blit(game_over_text, (50, 250))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Проверка сбора монет
    collected_coins = pygame.sprite.spritecollide(player, coins, False)
    for coin in collected_coins:
        coin_score += 1
        coin.reset_position()

    # Отрисовка всех спрайтов
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.update()
    FPS.tick(60)