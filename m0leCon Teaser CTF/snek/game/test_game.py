from planner import SnakeGame

game = SnakeGame()
print('apple', game.apple)
print(game.step('W'))
print('snake', game.snake[:game.length])
print('length', game.length, 'score', game.score)
print('next apple', game.apple)
