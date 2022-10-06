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
STARS_AMOUNT = 200


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


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


import asyncio
import curses


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

def draw(canvas):
    """
    Рисует получая данные от корутины.
    """    
    row, column = canvas.getmaxyx()
    courutine = fire(canvas, start_row=row//2, start_column=column//2, rows_speed=-0.3, columns_speed=0)
    while True:
        try:
            courutine.send(None)
            canvas.border()
            curses.curs_set(False)
            canvas.refresh()
            time.sleep(0.1)
        except StopIteration:
            break
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
    for courutine in courutines:
        courutine.send(None)
    canvas.border()
    curses.curs_set(False)
    canvas.refresh()
    star_queues = list(chunked(courutines, 10))
    while True:
        for queue in star_queues:
            for courutine in queue:
                courutine.send(None)
            canvas.border()
            curses.curs_set(False)
            canvas.refresh()
            time.sleep(0.1)


curses.update_lines_cols()
curses.wrapper(draw)