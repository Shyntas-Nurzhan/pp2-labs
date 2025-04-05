import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# --- Основные настройки экрана ---
WIDTH, HEIGHT = 600, 400         # Размеры игрового окна
BLOCK_SIZE = 20                  # Размер одного блока (для змейки и еды)
FENCE_THICKNESS = 20             # Толщина ограды (фенса)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# --- Цвета ---
WHITE  = (255, 255, 255)         # Белый
GREEN  = (0, 200, 0)             # Зеленый для змейки
RED    = (255, 0, 0)             # Красный (еда вес 1)
ORANGE = (255, 165, 0)           # Оранжевый (еда вес 2)
PURPLE = (128, 0, 128)           # Фиолетовый (еда вес 3)
BLACK  = (0, 0, 0)              # Черный (текст)
BROWN  = (139, 69, 19)          # Коричневый (ограда)

# --- Шрифты и FPS ---
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)
clock = pygame.time.Clock()

# --- Функция создания пиксельного фона ---
def create_pixel_background(width, height, scale=8):
    """
    Создает фон в пиксельном стиле путём масштабирования поверхности низкого разрешения.
    """
    # Размер поверхности низкого разрешения
    low_res_width = width // scale
    low_res_height = height // scale
    low_res_surface = pygame.Surface((low_res_width, low_res_height))
    
    # Заполняем поверхность узором: чередование оттенков зеленого
    for x in range(low_res_width):
        for y in range(low_res_height):
            # Чередование цвета в зависимости от суммы координат
            if (x + y) % 2 == 0:
                color = (34, 139, 34)  # Темно-зеленый
            else:
                color = (0, 128, 0)    # Зеленый
            low_res_surface.set_at((x, y), color)
    
    # Масштабируем поверхность до оригинального размера с эффектом пикселизации
    return pygame.transform.scale(low_res_surface, (width, height))

# --- Функция отрисовки ограды (фенса) ---
def draw_fence():
    """
    Рисует ограду по периметру экрана с заданной толщиной.
    """
    # Верхняя ограда
    pygame.draw.rect(screen, BROWN, (0, 0, WIDTH, FENCE_THICKNESS))
    # Нижняя ограда
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - FENCE_THICKNESS, WIDTH, FENCE_THICKNESS))
    # Левая ограда
    pygame.draw.rect(screen, BROWN, (0, 0, FENCE_THICKNESS, HEIGHT))
    # Правая ограда
    pygame.draw.rect(screen, BROWN, (WIDTH - FENCE_THICKNESS, 0, FENCE_THICKNESS, HEIGHT))

# --- Класс еды с весом и таймером ---
class Food:
    def __init__(self, snake):
        # Время появления еды
        self.spawn_time = time.time()
        # Время жизни еды (от 5 до 10 секунд)
        self.lifespan = random.randint(5, 10)
        # Вес еды (очки: 1, 2 или 3)
        self.weight = random.choice([1, 2, 3])
        # Цвет еды зависит от её веса
        self.color = {1: RED, 2: ORANGE, 3: PURPLE}[self.weight]
        # Генерируем позицию еды с учетом положения змейки и ограды
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        """
        Генерирует позицию для еды так, чтобы она не появлялась на змейке
        и находилась внутри огражденной области.
        """
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
        """
        Проверяет, истекло ли время жизни еды.
        """
        return time.time() - self.spawn_time > self.lifespan

    def draw(self, surface):
        """
        Отрисовывает еду как квадрат с заданным цветом.
        """
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# --- Функция отображения счёта и уровня ---
def draw_score_level(score, level):
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    # Вывод текста внутри огражденной области
    screen.blit(score_text, (FENCE_THICKNESS + 10, 10))
    screen.blit(level_text, (FENCE_THICKNESS + 10, 30))

# --- Функция отрисовки змейки ---
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

# --- Функция завершения игры ---
def game_over(score):
    screen.fill(BLACK)
    msg = big_font.render(f"Game Over! Score: {score}", True,RED)
    screen.blit(msg, (WIDTH // 6 - 35, HEIGHT // 2 - 35))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# --- Основной игровой цикл ---
def game_loop():
    # Инициализация змейки: список координат блоков
    snake = [(100, 100)]
    # Начальное направление движения: вправо
    dx, dy = BLOCK_SIZE, 0
    speed = 10          # Начальная скорость игры
    score = 0
    level = 1
    food_eaten_count = 0

    # Создаем первую еду
    current_food = Food(snake)

    # Создаем пиксельный фон
    pixel_background = create_pixel_background(WIDTH, HEIGHT)

    running = True
    while running:
        clock.tick(speed)

        # Обработка событий (выход, управление)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Управление стрелками (запрещаем разворот на 180°)
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE

        # Вычисление новой позиции головы змейки
        new_head = (snake[-1][0] + dx, snake[-1][1] + dy)

        # Проверка столкновения с оградой или самим собой:
        # Ограничиваем область так, чтобы змейка не заходила в зону ограды
        if (new_head in snake or
            new_head[0] < FENCE_THICKNESS or new_head[0] >= WIDTH - FENCE_THICKNESS or
            new_head[1] < FENCE_THICKNESS or new_head[1] >= HEIGHT - FENCE_THICKNESS):
            game_over(score)

        # Добавляем новую голову к змейке
        snake.append(new_head)

        # Проверка: съедена ли еда?
        if new_head == current_food.position:
            score += current_food.weight  # Прибавляем очки в зависимости от веса еды
            food_eaten_count += 1
            current_food = Food(snake)     # Генерируем новую еду
        else:
            # Если еду не съели, удаляем хвост (движение змейки)
            snake.pop(0)

        # Если еда «протухла», заменяем её новой
        if current_food.is_expired():
            current_food = Food(snake)

        # Каждые 4 съеденные единицы еды повышаем уровень и увеличиваем скорость
        if food_eaten_count >= 4:
            level += 1
            speed += 2
            food_eaten_count = 0

        # --- Отрисовка ---
        # Рисуем пиксельный фон
        screen.blit(pixel_background, (0, 0))
        # Рисуем ограду (фенс)
        draw_fence()
        # Рисуем змейку
        draw_snake(snake)
        # Рисуем еду
        current_food.draw(screen)
        # Рисуем счет и уровень
        draw_score_level(score, level)
        # Обновляем экран
        pygame.display.update()

# --- Запуск игры ---
game_loop()