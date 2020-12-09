import random
from math import pi, sin, cos
import pygame as pg

WINDOW_TITLE = 'HexenSnake'
COL_COUNT = 31
ROW_COUNT = 15
RADIUS = 30
HEX_MARGIN = 3
BORDER = 10
FPS = 60
BACKGROUND_COLOR = (235, 235, 235)


def main():
    cells = {}

    # Вычисляем размеры окна
    w = 2 * BORDER + 2 * RADIUS * (cos(pi / 6) ** 2) * (COL_COUNT - 1) + (2 * RADIUS)
    h = 2 * BORDER + 2 * RADIUS * cos(pi / 6) * ROW_COUNT
    if COL_COUNT > 1:
        h += RADIUS * cos(pi / 6)
    w = int(w)
    h = int(h)

    # Создаем поверхность для рисования фона
    hexen_surface = pg.Surface((w, h))
    hexen_surface.set_colorkey(BACKGROUND_COLOR)
    hexen_surface.fill(BACKGROUND_COLOR)

    # Вычисляем положение опорной точки
    x0 = BORDER + RADIUS
    y0 = BORDER + RADIUS * cos(pi / 6)

    # Вычисляем положение центров гексов
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            x = x0 + col * (2 * RADIUS * (cos(pi / 6) ** 2))
            y = y0 + row * (2 * RADIUS * cos(pi / 6)) + ((col % 2) * RADIUS * cos(pi / 6))
            cells[(row, col)] = (x, y)

    # Отрисовываем сами гексы
    delta_alpha = pi / 3
    for cell in cells.keys():
        x0, y0 = cells[cell]
        alpha = 0
        coords = []
        for _ in range(6):
            coords.append((x0 + (RADIUS - HEX_MARGIN) * cos(alpha), y0 - (RADIUS - HEX_MARGIN) * sin(alpha)))
            alpha += delta_alpha
        pg.draw.polygon(hexen_surface, (220, 220, 220), coords)
        cells[cell] = coords

    pg.draw.polygon(hexen_surface, (255, 0, 0), cells[(ROW_COUNT // 2, COL_COUNT // 2)])

    # Инициализируем окно
    pg.init()
    sc = pg.display.set_mode((w, h))
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
        pg.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
