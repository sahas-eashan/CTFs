import ctypes
from planner import SnakeGame
from path_utils import find_path_to_apple

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

game = SnakeGame()
actions = []
prefixes = []
num_apples = 12
for i in range(num_apples):
    path = find_path_to_apple(game.snake[:game.length], game.direction, game.apple)
    if path is None:
        raise RuntimeError("No path")
    for action in path:
        game.step(action)
        actions.append(action)
    prefixes.append(''.join(actions))

for idx, seq in enumerate(prefixes,1):
    with open(f"apple_prefix{idx}.txt","w") as f:
        f.write(seq)
print('generated prefixes up to', num_apples, 'apples')
