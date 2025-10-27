import ctypes
from itertools import product
from planner import SnakeGame, ACTIONS

libc = ctypes.CDLL("libc.so.6")
ACTIONS = ['.', 'W', 'A', 'S', 'D']

for length in range(1, 9):
    print('searching length', length)
    for seq in product(ACTIONS, repeat=length):
        libc.srand(1)
        game = SnakeGame()
        r = game.step('W')
        if r != 'ok_apple':
            continue
        valid = True
        for action in seq:
            result = game.step(action)
            if result == 'life_lost':
                print('found', ''.join(seq))
                exit(0)
            if result == 'ok_apple' or result == 'game_over':
                valid = False
                break
        if not valid:
            continue
print('not found')
