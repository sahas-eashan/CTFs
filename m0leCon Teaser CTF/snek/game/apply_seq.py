import ctypes
from planner import SnakeGame

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

with open("replay.txt") as f:
    actions = list(f.read().strip())

game = SnakeGame()
for idx, action in enumerate(actions, 1):
    res = game.step(action)
    print(idx, action, res, 'head', (game.snake[0][0]%10, game.snake[0][1]%10), 'len', game.length, 'lives', game.lives, 'score', game.score)
print('game_over', game.game_over)
