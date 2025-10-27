import ctypes
from planner import SnakeGame
from path_utils import find_path_to_apple, find_crash_sequence

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

game = SnakeGame()
replay_actions = []
life = 0
while not game.game_over:
    life += 1
    print(f"Life {life}: starting apple {game.apple}")
    # eat two apples
    for apple_index in (1,2):
        path = find_path_to_apple(game.snake[:game.length], game.direction, game.apple)
        if path is None:
            raise RuntimeError("No path to apple")
        print(f"  path{apple_index}", ''.join(path))
        for action in path:
            result = game.step(action)
            replay_actions.append(action)
            if result != ('ok_apple' if action == path[-1] else 'ok') and result != 'ok_apple':
                print('unexpected result', result)
        print(f"   ate apple, new apple {game.apple}, length {game.length}")
    crash_seq = find_crash_sequence(game.snake[:game.length], game.direction, game.apple)
    if crash_seq is None:
        raise RuntimeError("Failed to find crash sequence")
    print(f"  crash seq {''.join(crash_seq)}")
    for action in crash_seq:
        res = game.step(action)
        replay_actions.append(action)
        if res == 'life_lost':
            print(f"  lost life, lives left {game.lives}, apple {game.apple}")
            break
        elif res == 'game_over':
            print('  game over!')
            break
        elif res == 'ok_apple':
            raise RuntimeError('Crash sequence ate apple unexpectedly')

print('Total actions', len(replay_actions))
print('Replay string:', ''.join(replay_actions))
with open('replay.txt','w') as f:
    f.write(''.join(replay_actions))
