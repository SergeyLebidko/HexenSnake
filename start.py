import random
from math import pi, sin, cos
import pygame as pg

WINDOW_TITLE = 'HexenSnake'
COL_COUNT = 31
ROW_COUNT = 15
RADIUS = 30
NORMAL = RADIUS * cos(pi / 6)
HEX_MARGIN = 3
FOOD_SIZE = RADIUS - HEX_MARGIN - 10
BORDER = 10
FPS = 30
BACKGROUND_COLOR = (235, 235, 235)

COLOR_PRESETS = [
    (255, 0, 0),
    (5, 200, 100),
    (0, 0, 255),
    (128, 0, 255),
    (255, 0, 255),
    (255, 128, 0),
    (30, 30, 30),
    (150, 150, 150),
    (175, 62, 18),
    (0, 128, 255)
]

CELLS = {}
DIRECTIONS = [
    [(-1, 0), (-1, 0)],
    [(-1, 1), (0, 1)],
    [(0, 1), (1, 1)],
    [(1, 0), (1, 0)],
    [(0, -1), (1, -1)],
    [(-1, -1), (0, -1)]
]
KEY_DIRECTIONS = {
    pg.K_KP5: 0,
    pg.K_KP6: 1,
    pg.K_KP3: 2,
    pg.K_KP2: 3,
    pg.K_KP1: 4,
    pg.K_KP4: 5
}


def create_food(snake):
    cell = random.choice(list(set(CELLS.keys()) - set(snake.coords)))
    color = random.choice(list(set(COLOR_PRESETS) - {snake.color}))
    return {
        'cell': cell,
        'center': CELLS[cell]['center'],
        'color': color
    }


def draw_food(surface, food):
    pg.draw.circle(surface, food['color'], food['center'], FOOD_SIZE)


class SnakeCrashException(Exception):
    pass


class Snake:
    START_LEN = 5

    def __init__(self):
        self.coords = [(ROW_COUNT // 2, COL_COUNT // 2)]
        self.direction = random.randint(0, 5)
        for _ in range(self.START_LEN - 1):
            self.coords.append(CELLS[self.coords[-1]][(self.direction + 3) % 6])
        self.color = random.choice(COLOR_PRESETS)
        self.eat_count = 0

    def set_direction(self, next_direction):
        if (self.direction + 3) % 6 != next_direction:
            self.direction = next_direction

    def step(self, food):
        head = self.coords[0]
        next_head = CELLS[head][self.direction]
        if None in next_head:
            contr_direction = (self.direction + 3) % 6
            next_head = head
            while not (None in CELLS[next_head][contr_direction]):
                next_head = CELLS[next_head][contr_direction]

        self.coords = [next_head] + self.coords
        if self.coords[0] != food['cell']:
            self.coords = self.coords[:-1]

        if len(set(self.coords)) < len(self.coords):
            raise SnakeCrashException()

        eat_flag = self.coords[0] == food['cell']
        if eat_flag:
            self.eat_count += 1
        return eat_flag

    def draw(self, surface):
        for segment in self.coords:
            pg.draw.polygon(surface, self.color, CELLS[segment]['coords'])


class Tab:

    def __init__(self, font, window_width, window_height):
        self.font = font
        self.window_width = window_width
        self.window_height = window_height
        self.current_text = None
        self.tab_surface = None
        self.tab_surface_pos = None

    def draw(self, surface, text):
        if text != self.current_text:
            self.current_text = text
            self.tab_surface = self.font.render(self.current_text, True, (0, 0, 0))
            self.tab_surface.set_alpha(20)
            self.tab_surface_pos = (
                self.window_width // 2 - self.tab_surface.get_rect().width // 2,
                self.window_height // 2 - self.tab_surface.get_rect().height // 2
            )

        surface.blit(self.tab_surface, self.tab_surface_pos)


class SpeedController:
    SPEED_LIMIT = 6

    def __init__(self):
        self.current_speed = self.SPEED_LIMIT
        self.counter = 0

    def speed_plus(self):
        if self.current_speed > 0:
            self.current_speed -= 1

    def speed_minus(self):
        if self.current_speed < self.SPEED_LIMIT:
            self.current_speed += 1

    def enable_frame(self):
        self.counter += 1
        if self.counter > self.current_speed:
            self.counter = 0
        return self.counter == self.current_speed

    def get_speed_for_display(self):
        return self.SPEED_LIMIT - self.current_speed + 1


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
        x0, y0 = CELLS[cell]['center']
        alpha = 0
        coords = []
        for _ in range(6):
            coords.append((x0 + (RADIUS - HEX_MARGIN) * cos(alpha), y0 - (RADIUS - HEX_MARGIN) * sin(alpha)))
            alpha += delta_alpha
        pg.draw.polygon(hexen_surface, (220, 220, 220), coords)
        CELLS[cell]['coords'] = coords

    snake = Snake()
    food = create_food(snake)
    speed_controller = SpeedController()

    # Инициализируем окно
    pg.init()
    sc = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption(f'{WINDOW_TITLE} - скорость: {speed_controller.get_speed_for_display()}')
    clock = pg.time.Clock()

    font = pg.font.Font(None, 512)
    tab = Tab(font, window_width, window_height)

    pause = False
    while True:
        if speed_controller.enable_frame():
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_KP_MINUS:
                        speed_controller.speed_minus()
                        pg.display.set_caption(f'{WINDOW_TITLE} - скорость: {speed_controller.get_speed_for_display()}')

                    if event.key == pg.K_KP_PLUS:
                        speed_controller.speed_plus()
                        pg.display.set_caption(f'{WINDOW_TITLE} - скорость: {speed_controller.get_speed_for_display()}')

                    if event.key == pg.K_SPACE:
                        pause = not pause
                        continue

                    next_direction = KEY_DIRECTIONS.get(event.key)
                    if next_direction is not None:
                        snake.set_direction(next_direction)

            if not pause:
                try:
                    eat_flag = snake.step(food)
                except SnakeCrashException:
                    snake = Snake()
                    food = create_food(snake)
                else:
                    if eat_flag:
                        snake.color = food['color']
                        food = create_food(snake)

        sc.fill(BACKGROUND_COLOR)
        sc.blit(hexen_surface, (0, 0))
        if pause:
            tab.draw(sc, 'PAUSE')
        else:
            tab.draw(sc, str(snake.eat_count))
        draw_food(sc, food)
        snake.draw(sc)
        pg.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
