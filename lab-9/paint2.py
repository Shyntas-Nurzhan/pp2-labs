import pygame
import sys
import math

# Инициализация Pygame и создание окна
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Размер окна 800x600
pygame.display.set_caption("Simple Paint Extended")  # Заголовок окна
clock = pygame.time.Clock()  # Объект для ограничения FPS

# Переменные состояния и настройки
drawing = False             # Флаг, показывающий, что происходит рисование (мышь зажата)
start_pos = (0, 0)          # Начальная точка для рисования фигуры
# Инструмент по умолчанию — прямоугольник; остальные: circle, eraser, square, right_triangle, equilateral_triangle, rhombus
tool = 'rectangle'
color = (255, 0, 0)         # Текущий цвет (красный по умолчанию)
bg_color = (255, 255, 255)  # Цвет фона (белый)
radius = 10                 # Радиус для рисования окружностей и ластика

# Ограничения по радиусу ластика
min_radius = 5
max_radius = 100

# Заполняем экран фоновым цветом
screen.fill(bg_color)

def draw_shape(surface, tool, color, start, end):
    """
    Отрисовка фигуры на поверхности 'surface' в зависимости от выбранного инструмента.
    Параметры:
      tool  - тип фигуры ('rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus')
      color - цвет фигуры
      start - начальная точка (при нажатии мыши)
      end   - конечная точка (при отпускании мыши)
    """
    if tool == 'rectangle':
        # Рисуем прямоугольник: нормализуем прямоугольник, чтобы его размеры были положительными
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        pygame.draw.rect(surface, color, rect, 2)
        
    elif tool == 'circle':
        # Рисуем окружность: вычисляем ширину и высоту области, затем находим центр и радиус
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])
        radius_circle = max(width, height) // 2  # Радиус выбирается по большей стороне
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        pygame.draw.circle(surface, color, center, radius_circle, 2)
    
    elif tool == 'square':
        # Рисуем квадрат: из нормализованного прямоугольника выбираем сторону как max(width, height)
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        side = max(rect.width, rect.height)
        square_rect = pygame.Rect(rect.topleft, (side, side))
        pygame.draw.rect(surface, color, square_rect, 2)
    
    elif tool == 'right_triangle':
        # Рисуем прямоугольный (правильный) треугольник,
        # используя нормализованный прямоугольник и беря правый угол в нижнем левом угле.
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        # Выбираем три вершины: верхний левый, нижний левый и нижний правый углы прямоугольника
        p1 = (rect.left, rect.top)
        p2 = (rect.left, rect.bottom)
        p3 = (rect.right, rect.bottom)
        pygame.draw.polygon(surface, color, [p1, p2, p3], 2)
    
    elif tool == 'equilateral_triangle':
        # Рисуем равносторонний треугольник. 
        # Для корректного отображения берем сторону как минимум из ширины и высоты нормализованного прямоугольника.
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        side = min(rect.width, rect.height)
        # Базу треугольника делаем горизонтальной в нижней части прямоугольника
        p1 = (rect.left, rect.bottom)
        p2 = (rect.left + side, rect.bottom)
        # Высота равностороннего треугольника = side * sqrt(3)/2
        height_tri = int(side * math.sqrt(3) / 2)
        p3 = (rect.left + side // 2, rect.bottom - height_tri)
        pygame.draw.polygon(surface, color, [p1, p2, p3], 2)
    
    elif tool == 'rhombus':
        # Рисуем ромб (алмаз): используем середины сторон нормализованного прямоугольника как вершины
        rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
        rect.normalize()
        p1 = (rect.centerx, rect.top)
        p2 = (rect.right, rect.centery)
        p3 = (rect.centerx, rect.bottom)
        p4 = (rect.left, rect.centery)
        pygame.draw.polygon(surface, color, [p1, p2, p3, p4], 2)

# Главный цикл программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Выход из программы при закрытии окна
            pygame.quit()
            sys.exit()

        # Начало рисования: нажата кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  # Сохраняем начальную позицию
        
        # Завершение рисования: отпущена кнопка мыши
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos  # Получаем конечную позицию
                # Если выбран один из инструментов для отрисовки фигур, вызываем соответствующую функцию
                if tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    draw_shape(screen, tool, color, start_pos, end_pos)
            drawing = False

        # Обработка нажатий клавиш для смены инструментов и цвета
        if event.type == pygame.KEYDOWN:
            # Инструменты для рисования фигур
            if event.key == pygame.K_r:
                tool = 'rectangle'         # Прямоугольник
            elif event.key == pygame.K_c:
                tool = 'circle'            # Круг
            elif event.key == pygame.K_q:
                tool = 'square'            # Квадрат
            elif event.key == pygame.K_t:
                tool = 'right_triangle'    # Правый (прямоугольный) треугольник
            elif event.key == pygame.K_v:
                tool = 'equilateral_triangle'  # Равносторонний треугольник
            elif event.key == pygame.K_d:
                tool = 'rhombus'           # Ромб (алмаз)
            elif event.key == pygame.K_e:
                tool = 'eraser'            # Ластик
            
            # Смена цвета
            elif event.key == pygame.K_1:
                color = (255, 0, 0)        # Красный
            elif event.key == pygame.K_2:
                color = (0, 255, 0)        # Зелёный
            elif event.key == pygame.K_3:
                color = (0, 0, 255)        # Синий
            elif event.key == pygame.K_4:
                color = (0, 0, 0)          # Чёрный
            elif event.key == pygame.K_5:
                color = (255, 255, 255)    # Белый

            # Изменение радиуса ластика
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                radius = min(radius + 5, max_radius)
                print(f"Радиус ластика: {radius}")
            elif event.key == pygame.K_MINUS:
                radius = max(radius - 5, min_radius)
                print(f"Радиус ластика: {radius}")

    # Если выбран инструмент "ластик" и кнопка мыши зажата, стираем область (закрашиваем фоновым цветом)
    if drawing and tool == 'eraser':
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, bg_color, mouse_pos, radius)

    pygame.display.flip()  # Обновляем экран
    clock.tick(60)         # Ограничиваем FPS до 60