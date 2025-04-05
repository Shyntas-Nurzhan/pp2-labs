import pygame
import sys

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Создаём окно 800x600
pygame.display.set_caption("Simple Paint")    # Заголовок окна
clock = pygame.time.Clock()                   # Для ограничения FPS

# Переменные состояния
drawing = False               # Флаг: происходит ли рисование сейчас
start_pos = (0, 0)            # Начальная точка рисования
tool = 'rectangle'           # Текущий инструмент: 'rectangle', 'circle', 'eraser'
color = (255, 0, 0)           # Цвет по умолчанию — красный
bg_color = (255, 255, 255)    # Цвет фона — белый
radius = 10                   # Радиус для окружностей и ластика

min_radius = 5
max_radius = 100

# Заполняем экран фоновым цветом
screen.fill(bg_color)

def draw_shape(surface, tool, color, start, end):
    if tool == 'rectangle':
        # Нормализуем прямоугольник (чтобы можно было рисовать в любом направлении)
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        pygame.draw.rect(surface, color, rect, 2)

    elif tool == 'circle':
        # Находим размеры по осям
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])
        radius = max(width, height) // 2  # Радиус круга — половина большей стороны
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        pygame.draw.circle(surface, color, center, radius, 2)


# Главный цикл программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Выход из программы при закрытии окна
            pygame.quit()
            sys.exit()

        # Когда нажата кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  # Сохраняем начальную точку

        # Когда отпущена кнопка мыши
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos  # Конечная точка
                if tool in ['rectangle', 'circle']:
                    draw_shape(screen, tool, color, start_pos, end_pos)  # Рисуем фигуру
            drawing = False

        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = 'rectangle'  # Инструмент — прямоугольник
            elif event.key == pygame.K_c:
                tool = 'circle'     # Инструмент — круг
            elif event.key == pygame.K_e:
                tool = 'eraser'     # Инструмент — ластик
            # Выбор цвета
            elif event.key == pygame.K_1:
                color = (255, 0, 0)     # Красный
            elif event.key == pygame.K_2:
                color = (0, 255, 0)     # Зелёный
            elif event.key == pygame.K_3:
                color = (0, 0, 255)     # Синий
            elif event.key == pygame.K_4:
                color = (0, 0, 0)       # Чёрный
            elif event.key == pygame.K_5:
                color = (255, 255, 255) # Белый

          # Увеличение радиуса ластика
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                radius = min(radius + 5, max_radius)
                print(f"Радиус ластика: {radius}")

            # Уменьшение радиуса ластика
            elif event.key == pygame.K_MINUS:
                radius = max(radius - 5, min_radius)
                print(f"Радиус ластика: {radius}")

    # Если рисуем ластиком — закрашиваем кругом фоновым цветом
    if drawing and tool == 'eraser':
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, bg_color, mouse_pos, radius)

    pygame.display.flip()     # Обновляем экран
    clock.tick(60)            # Ограничиваем FPS до 60