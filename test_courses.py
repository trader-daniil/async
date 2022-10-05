import asyncio
import curses
import time


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
    blinking_first = blink(
        canvas=canvas,
        row=5,
        column=20,
    )
    blinking_second = blink(
        canvas=canvas,
        row=5,
        column=22,
    )
    blinking_third = blink(
        canvas=canvas,
        row=5,
        column=24,
    )
    blinking_fourth = blink(
        canvas=canvas,
        row=5,
        column=26,
    )
    blinking_fives = blink(
        canvas=canvas,
        row=5,
        column=28,
    )
    courutines = [
        blinking_first,
        blinking_second,
        blinking_third,
        blinking_fourth,
        blinking_fives,
    ]
    while True:
        for courutine in courutines:
            courutine.send(None)
        canvas.border()
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(1)


curses.update_lines_cols()
curses.wrapper(draw)
