import pygame
import sys
import random
import time
from datetime import datetime
import psycopg2
from config import load_config

# Инициализация Pygame
pygame.init()

# --- Основные настройки экрана ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FENCE_THICKNESS = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# --- Цвета ---
WHITE  = (255, 255, 255)
GREEN  = (0, 200, 0)
RED    = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BLACK  = (0, 0, 0)
BROWN  = (139, 69, 19)

# --- Шрифты и FPS ---
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)
clock = pygame.time.Clock()

# --- Пользователь ---
current_user = None

# --- Создание таблиц ---
def create_tables():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            current_level INTEGER DEFAULT 1
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            date TIMESTAMP NOT NULL,
            score INTEGER NOT NULL,
            level INTEGER NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# --- Сохранение прогресса ---
def save_score(user_id, date, score, level):
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_scores (user_id, date, score, level)
            VALUES (%s, %s, %s, %s);
        """, (user_id, date, score, level))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error saving score:", e)

# --- Получение или создание пользователя ---
def get_or_create_user(username):
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    cur.execute("SELECT id, current_level FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id, level = user
        print(f"Добро пожаловать, {username}. Ваш текущий уровень: {level}")
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        level = 1
        print(f"Создан новый пользователь: {username} (Уровень 1)")
    cur.close()
    conn.close()
    return user_id, level

# --- Функция создания пиксельного фона ---
def create_pixel_background(width, height, scale=8):
    low_res_width = width // scale
    low_res_height = height // scale
    low_res_surface = pygame.Surface((low_res_width, low_res_height))
    for x in range(low_res_width):
        for y in range(low_res_height):
            if (x + y) % 2 == 0:
                color = (34, 139, 34)
            else:
                color = (0, 128, 0)
            low_res_surface.set_at((x, y), color)
    return pygame.transform.scale(low_res_surface, (width, height))

# --- Функция отрисовки ограды (фенса) ---
def draw_fence():
    pygame.draw.rect(screen, BROWN, (0, 0, WIDTH, FENCE_THICKNESS))
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - FENCE_THICKNESS, WIDTH, FENCE_THICKNESS))
    pygame.draw.rect(screen, BROWN, (0, 0, FENCE_THICKNESS, HEIGHT))
    pygame.draw.rect(screen, BROWN, (WIDTH - FENCE_THICKNESS, 0, FENCE_THICKNESS, HEIGHT))

# --- Класс еды ---
class Food:
    def __init__(self, snake):
        self.spawn_time = time.time()
        self.lifespan = random.randint(5, 10)
        self.weight = random.choice([1, 2, 3])
        self.color = {1: RED, 2: ORANGE, 3: PURPLE}[self.weight]
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        min_x = FENCE_THICKNESS
        max_x = WIDTH - FENCE_THICKNESS - BLOCK_SIZE
        min_y = FENCE_THICKNESS
        max_y = HEIGHT - FENCE_THICKNESS - BLOCK_SIZE
        while True:
            x = random.randrange(min_x, max_x + 1, BLOCK_SIZE)
            y = random.randrange(min_y, max_y + 1, BLOCK_SIZE)
            if (x, y) not in snake:
                return (x, y)

    def is_expired(self):
        return time.time() - self.spawn_time > self.lifespan

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# --- Интерфейс ---
def draw_score_level(score, level):
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (FENCE_THICKNESS + 10, 10))
    screen.blit(level_text, (FENCE_THICKNESS + 10, 30))

def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

# --- Конец игры ---
def game_over(score):
    screen.fill(BLACK)
    msg = big_font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(msg, (WIDTH // 6 - 35, HEIGHT // 2 - 35))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# --- Игровой цикл ---
def game_loop():
    global current_user
    username = input("Введите ваше имя: ")
    user_id, level = get_or_create_user(username)
    current_user = user_id

    snake = [(100, 100)]
    dx, dy = BLOCK_SIZE, 0
    speed = 10 + level * 2
    score = 0
    food_eaten_count = 0
    date = datetime.now()
    current_food = Food(snake)
    pixel_background = create_pixel_background(WIDTH, HEIGHT)

    paused = False
    running = True
    while running:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_score(user_id, date, score, level)
                        print("Игра приостановлена и сохранена.")
                if not paused:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK_SIZE, 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK_SIZE

        if paused:
            continue

        new_head = (snake[-1][0] + dx, snake[-1][1] + dy)

        if (new_head in snake or
            new_head[0] < FENCE_THICKNESS or new_head[0] >= WIDTH - FENCE_THICKNESS or
            new_head[1] < FENCE_THICKNESS or new_head[1] >= HEIGHT - FENCE_THICKNESS):
            save_score(user_id, date, score, level)
            game_over(score)

        snake.append(new_head)

        if new_head == current_food.position:
            score += current_food.weight
            food_eaten_count += 1
            current_food = Food(snake)
        else:
            snake.pop(0)

        if current_food.is_expired():
            current_food = Food(snake)

        if food_eaten_count >= 4:
            level += 1
            speed += 2
            food_eaten_count = 0

        screen.blit(pixel_background, (0, 0))
        draw_fence()
        draw_snake(snake)
        current_food.draw(screen)
        draw_score_level(score, level)
        pygame.display.update()

# --- Запуск ---
create_tables()
game_loop()
