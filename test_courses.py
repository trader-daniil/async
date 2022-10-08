import asyncio
import curses
import time
import random
from more_itertools import chunked


STARS = (
    '*',
    '+',
    '.',
    ':',
)
STARS_AMOUNT = 300
SPACE_KEY_CODE = 32
#LEFT_KEY_CODE = 260
LEFT_KEY_CODE = 452
#RIGHT_KEY_CODE = 261
RIGHT_KEY_CODE = 454
#UP_KEY_CODE = 259
UP_KEY_CODE = 450
#DOWN_KEY_CODE = 258
DOWN_KEY_CODE = 456


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""
    
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -10

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 10

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 10

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -10

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    
    return rows_direction, columns_direction, space_pressed


async def blink(canvas, row, column, symbol='*'):
    """
    Возвращает данные для отрисовки.
    """
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await Sleep(2)

        canvas.addstr(row, column, symbol)
        await Sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await Sleep(0.5)

        canvas.addstr(row, column, symbol)
        await Sleep(0.3)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed



def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""
    
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break
                
            if symbol == ' ':
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def animate_spaceship(canvas, row, column, rocket_1, rocket_2):
    """
    Отрисовывает корабль.
    """
    while True:
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket_1,
        ) 
        await Sleep(0.5)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket_1,
            negative=True,
        ) 
        await Sleep(0.5)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket_2,
        )
        await Sleep(0.5)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket_2,
            negative=True,
        )
        await Sleep(0.5)


def draw(canvas):
    """
    Рисует получая данные от корутины.
    """

    row, column = canvas.getmaxyx()
    
    with open('rocket_frame_1.txt') as f:
        rocket_1 = f.read()
    with open('rocket_frame_2.txt') as f:
        rocket_2 = f.read()

    spaceship = animate_spaceship(
        canvas=canvas,
        row=row//2,
        column=column//2,
        rocket_1=rocket_1,
        rocket_2=rocket_2,
    )

    courutines = []
    for _ in range(STARS_AMOUNT):
        courutines.append(
            blink(
                canvas=canvas,
                row=random.randint(1, row-1),
                column=random.randint(1, column-1),
                symbol=random.choice(STARS),    
            ),
        )
    #shot = fire(canvas, start_row=row//2, start_column=column//2, rows_speed=-0.3, columns_speed=0)
    #анимация выстрела
    """
    while True:
        try:
            shot.send(None)
            canvas.border()
            curses.curs_set(False)
            canvas.refresh()
            time.sleep(0.05)
        except StopIteration:
            break
    #анимация звездного неба
    """
    star_queues = list(chunked(courutines, 10))
    while True:
        for queue in star_queues:
            for courutine in queue:
                courutine.send(None)
            spaceship.send(None)
            canvas.refresh()
            time.sleep(0.2)
            spaceship.send(None)
            canvas.refresh()
            # получение ввода пользователя
            canvas.nodelay(True)
            row_change, column_change, _ = read_controls(canvas=canvas)
            row += row_change
            column += column_change
            # отображение новых координат корабля
            spaceship = animate_spaceship(
                canvas=canvas,
                row=row//2,
                column=column//2,
                rocket_1=rocket_1,
                rocket_2=rocket_2,
            )
            spaceship.send(None)
            canvas.refresh()
            time.sleep(0.2)
            spaceship.send(None)
            canvas.refresh()

    

curses.update_lines_cols()
curses.wrapper(draw)
