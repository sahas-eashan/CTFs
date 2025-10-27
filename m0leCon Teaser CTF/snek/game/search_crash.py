import ctypes
from itertools import product
from planner import SnakeGame

libc = ctypes.CDLL("libc.so.6")
ACTIONS = ['.', 'W', 'A', 'S', 'D']
BASE_SEQ = ['W','A','S','W','W','A']  # eat two apples

for length in range(1, 9):
    print('search length', length)
    for seq in product(ACTIONS, repeat=length):
        libc.srand(1)
        game = SnakeGame()
        valid = True
        for action in BASE_SEQ:
            res = game.step(action)
            if res not in ('ok', 'ok_apple'):
                valid = False
                break
        if not valid:
            continue
        for action in seq:
            res = game.step(action)
            if res == 'life_lost':
                print('found', ''.join(seq))
                exit(0)
            if res == 'ok_apple' or res == 'game_over':
                valid = False
                break
        if not valid:
            continue
print('not found')
