import asyncio
import curses
from os import read
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
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    
    return rows_direction, columns_direction, space_pressed


def draw(canvas):
    """
    canvas.nodelay(True)
    time.sleep(2)
    #char = canvas.getch()
    char = read_controls(canvas=canvas)
    print(f'You pressed {char}')
    """





curses.update_lines_cols()
curses.wrapper(draw)

