import asyncio
import curses
import time
import random
from itertools import cycle
from more_itertools import chunked
import os


STARS = '*+.:'
STARS_AMOUNT = 300
SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 452
RIGHT_KEY_CODE = 454
UP_KEY_CODE = 450
DOWN_KEY_CODE = 456
HORIZONTAL_MOVE = 5
VERICAL_MOVE = 5


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
            rows_direction = -VERICAL_MOVE

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = VERICAL_MOVE

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = HORIZONTAL_MOVE

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -HORIZONTAL_MOVE

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    
    return rows_direction, columns_direction, space_pressed



async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3000):
            await asyncio.sleep(0)



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


def animate_shot(canvas, row, column):
    shot = fire(canvas, start_row=row//2, start_column=column//2, rows_speed=-0.3, columns_speed=0)

    while True:
        try:
            shot.send(None)
            canvas.border()
            curses.curs_set(False)
            canvas.refresh()
            time.sleep(0.05)
        except StopIteration:
            break
    


async def animate_spaceship(canvas, row, column, rocket_1, rocket_2):
    """
    Отрисовывает корабль.
    """
    canvas_row, canvas_column = canvas.getmaxyx()

    rockets = (
        rocket_1,
        rocket_2,
    )
    for rocket in cycle(rockets):
        canvas.nodelay(True)
        row_change, column_change, _ = read_controls(canvas=canvas)

        if (row + row_change <= 0 or
            row + row_change >= canvas_row - 2 * VERICAL_MOVE):
                continue
        else:
            row += row_change

        if (column + column_change <= 0 or
                column + column_change >= canvas_column - HORIZONTAL_MOVE):
                continue
        else:
            column += column_change
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket,
        ) 
        await Sleep(1)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=rocket,
            negative=True,
        ) 
        await Sleep(0.5)
    

def draw(canvas):
    """
    Рисует получая данные от корутины.
    """

    canvas_row, canvas_column = canvas.getmaxyx()

    rockets = []
    for scheme in os.listdir('rocket_scheme'):
        with open(f'rocket_scheme/{scheme}') as rocket_scheme:
            rockets.append(rocket_scheme.read())
    
    

    spaceship = animate_spaceship(
        canvas=canvas,
        row=canvas_row//2,
        column=canvas_column//2,
        rocket_1=rockets[0],
        rocket_2=rockets[-1],
    )
    
    courutines = []
    for _ in range(STARS_AMOUNT):
        courutines.append(
            blink(
                canvas=canvas,
                row=random.randint(1, canvas_row-1),
                column=random.randint(1, canvas_column-1),
                symbol=random.choice(STARS),    
            ),
        )
   
    # создаем анимацию звезд и корабля

    star_queues = list(chunked(courutines, 10))
    while True:
        for queue in star_queues:
            for courutine in queue:
                courutine.send(None)
            canvas.border()
            spaceship.send(None)
            canvas.refresh()
            time.sleep(0.5)
            spaceship.send(None)
            canvas.refresh()



if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
