import asyncio
import curses
import nntplib
import time


async def blink(canvas, row, column, symbol='*'):
    """
    Возвращает данные для отрисовки.
    """
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


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
        time.sleep(0.5)


curses.update_lines_cols()
curses.wrapper(draw)
