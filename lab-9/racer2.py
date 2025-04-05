import pygame
from pygame.locals import *
import sys
import random

# Инициализация Pygame
pygame.init()

# --- Настройки экрана и ресурсов ---
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RACER")  # Название окна
background = pygame.image.load("AnimatedStreet.png")  # Фоновое изображение

# --- Цвета и шрифты ---
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Verdana", 60)         # Крупный шрифт (для Game Over)
font_small = pygame.font.SysFont("Verdana", 20)   # Маленький шрифт (для очков)
game_over_text = font.render("Game Over", True, BLACK)

# --- Переменные ---
done = False
coin_score = 0           # Счёт обычных монет
beka_coin_score = 0      # Счёт "бека-монет"
FPS = pygame.time.Clock()
speed = 10               # Начальная скорость врагов

# --- Классы ---

# Враг (машина, которую нужно избегать)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        # Двигается вниз с заданной скоростью
        self.rect.move_ip(0, int(speed))
        # Если вышел за экран — возвращается сверху в случайной позиции
        if self.rect.top > screen_height:
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)

# Игрок (машина пользователя)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Управление влево и вправо с границами экрана
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(5, 0)

# Обычная монета
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game-coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        # Двигается вниз
        self.rect.move_ip(0, 7)
        # Если ушла за экран — перерождается сверху
        if self.rect.top > screen_height:
            self.reset_position()

    def reset_position(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, screen_width - 40), 0)

# Большая монета (даёт больше очков)
class BekaCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bigCoin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        # Движение вниз
        self.rect.move_ip(0, 7)
        if self.rect.top > screen_height:
            self.reset_position()

    def reset_position(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, screen_width - 40), 0)

# --- Создание игровых объектов ---

player = Player()

# Группа врагов
enemies = pygame.sprite.Group()
enemies.add(Enemy())

# Группа обычных монет
coins = pygame.sprite.Group()
for _ in range(3):  # Три обычные монеты
    coins.add(Coin())

# Группа бека-монет (одна большая монета)
bekacoins = pygame.sprite.Group()
bekacoins.add(BekaCoin())

# Все объекты вместе (для отрисовки)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(*enemies)
all_sprites.add(*coins)
all_sprites.add(*bekacoins)

# --- Главный игровой цикл ---
while not done:
    # Обработка событий (например, выход из игры)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отображение текущего счёта
    score_display = font_small.render(f"Coins: {coin_score}", True, BLACK)
    screen.blit(score_display, (10, 10))

    # Движение объектов
    player.move()
    for enemy in enemies:
        enemy.move()
    for coin in coins:
        coin.move()
    for bekacoin in bekacoins:
        bekacoin.move()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        screen.fill(RED)
        screen.blit(game_over_text, (30, 250))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Проверка сбора обычных монет
    collected_coins = pygame.sprite.spritecollide(player, coins, False)
    for coin in collected_coins:
        coin_score += 1
        speed += 0.1  # Увеличение сложности
        coin.reset_position()

    # Проверка сбора бека-монет
    beka_collected_coins = pygame.sprite.spritecollide(player, bekacoins, False)
    for bekacoin in beka_collected_coins:
        coin_score += 5
        beka_coin_score += 5
        speed += 0.5
        bekacoin.reset_position()

    # Отрисовка всех объектов на экране
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # Обновление экрана
    pygame.display.update()
    FPS.tick(60)  # Ограничение FPS