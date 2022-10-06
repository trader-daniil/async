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
STARS_AMOUNT = 20


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


def draw(canvas):
    """
    Рисует получая данные от корутины.
    """    
    row, column = canvas.getmaxyx()

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
