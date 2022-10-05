import asyncio
import time


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


async def do_ticking(amount_of_ticks, sound):
    for _ in range(amount_of_ticks):
        print(sound)
        await Sleep(1)


async def bang_the_bomb(amount_of_ticks=5, sound='tick'):
    clock = do_ticking(amount_of_ticks, sound)
    await clock
    print("BOOM!")


bombs = [
    bang_the_bomb(amount_of_ticks=9, sound='click'),
    bang_the_bomb(amount_of_ticks=5, sound='chick'),
    bang_the_bomb(amount_of_ticks=3)
]

while True:
    for bomb in bombs:
        try:
            sleep_comand = bomb.send(None)
            time.sleep(sleep_comand.seconds)
        except StopIteration:
            bombs.remove(bomb)
            continue
    if len(bombs) == 0:
        break
    

