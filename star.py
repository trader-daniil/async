import time
import curses
import asyncio


def draw(canvas):
    while True:
        curses.curs_set(False)
        row, column = (5, 20)
        canvas.addstr(row, column, 'Hello', curses.A_DIM)
        canvas.refresh()
        time.sleep(2)
        canvas.addstr(row, column, 'Hello')
        canvas.refresh()
        time.sleep(0.3)
        canvas.addstr(row, column, 'Hello', curses.A_BOLD)
        canvas.refresh()
        time.sleep(0.5)
        canvas.addstr(row, column, 'Hello')
        canvas.refresh()
        time.sleep(0.3)




if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
