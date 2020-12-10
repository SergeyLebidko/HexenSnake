import random
from math import pi, sin, cos
import pygame as pg

WINDOW_TITLE = 'HexenSnake'
COL_COUNT = 31
ROW_COUNT = 15
RADIUS = 30
NORMAL = RADIUS * cos(pi / 6)
HEX_MARGIN = 3
BORDER = 10
FPS = 5
BACKGROUND_COLOR = (235, 235, 235)

CELLS = {}
DIRECTIONS = [
    [(-1, 0), (-1, 0)],
    [(-1, 1), (0, 1)],
    [(0, 1), (1, 1)],
    [(1, 0), (1, 0)],
    [(0, -1), (1, -1)],
    [(-1, -1), (0, -1)]
]


class Snake:
    START_LEN = 5

    def __init__(self):
        self.coords = [(ROW_COUNT // 2, COL_COUNT // 2)]
        self.direction = random.randint(0, 5)
        for _ in range(self.START_LEN - 1):
            self.coords.append(CELLS[self.coords[-1]][self.direction])
        self.direction = (self.direction + 3) % 6

    def step(self):
        self.coords = [CELLS[self.coords[0]][self.direction]] + self.coords
        self.coords = self.coords[:-1]

    def draw(self, surface):
        for segment in self.coords:
            pg.draw.polygon(surface, (255, 0, 0), CELLS[segment]['coords'])


def main():
    # Вычисляем размеры окна
    window_width = 2 * BORDER + 2 * NORMAL * cos(pi / 6) * (COL_COUNT - 1) + (2 * RADIUS)
    window_height = 2 * BORDER + 2 * NORMAL * ROW_COUNT
    if COL_COUNT > 1:
        window_height += NORMAL
    window_width, window_height = int(window_width), int(window_height)

    # Создаем поверхность для рисования фона
    hexen_surface = pg.Surface((window_width, window_height))
    hexen_surface.set_colorkey(BACKGROUND_COLOR)
    hexen_surface.fill(BACKGROUND_COLOR)

    # Вычисляем положение опорной точки
    x0 = BORDER + RADIUS
    y0 = BORDER + NORMAL

    # Вычисляем положение центров гексов
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            x = x0 + 2 * col * NORMAL * cos(pi / 6)
            y = y0 + 2 * row * NORMAL + (col % 2) * NORMAL
            CELLS[(row, col)] = {'center': (x, y)}
            for direction in range(6):
                delta_row, delta_col = DIRECTIONS[direction][col % 2]
                next_row, next_col = row + delta_row, col + delta_col
                next_row = next_row if 0 <= next_row < ROW_COUNT else None
                next_col = next_col if 0 <= next_col < COL_COUNT else None
                CELLS[(row, col)][direction] = (next_row, next_col)

    # Отрисовываем сами гексы
    delta_alpha = pi / 3
    for cell in CELLS.keys():
        x0, y0 = CELLS[cell].pop('center')
        alpha = 0
        coords = []
        for _ in range(6):
            coords.append((x0 + (RADIUS - HEX_MARGIN) * cos(alpha), y0 - (RADIUS - HEX_MARGIN) * sin(alpha)))
            alpha += delta_alpha
        pg.draw.polygon(hexen_surface, (220, 220, 220), coords)
        CELLS[cell]['coords'] = coords

    snake = Snake()

    # Инициализируем окно
    pg.init()
    sc = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption(WINDOW_TITLE)
    clock = pg.time.Clock()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        sc.fill(BACKGROUND_COLOR)
        sc.blit(hexen_surface, (0, 0))
        snake.draw(sc)
        pg.display.update()

        snake.step()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
