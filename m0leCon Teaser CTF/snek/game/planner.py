import ctypes
from collections import deque

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

ACTIONS = ['.', 'W', 'A', 'S', 'D']
DIRS = {
    'W': (0, -1),
    'S': (0, 1),
    'A': (-1, 0),
    'D': (1, 0),
}

class SnakeGame:
    def __init__(self):
        self.reset_global()

    def rand(self):
        return libc.rand()

    def reset_global(self):
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.direction = (1, 0)
        self.snake = [(6,5),(5,5),(4,5)]
        self.length = 3
        self.apple = self.pick_new_apple()

    def clone(self):
        g = SnakeGame.__new__(SnakeGame)
        g.__dict__ = self.__dict__.copy()
        g.snake = list(self.snake)
        g.direction = tuple(self.direction)
        g.apple = tuple(self.apple)
        return g

    def pick_new_apple(self):
        available = [1]*100
        count = 100
        for x,y in self.snake[:self.length]:
            idx = ((y % 10) * 10) + (x % 10)
            if available[idx]:
                available[idx] = 0
                count -= 1
        if count == 0:
            return self.snake[0]  # shouldn't happen
        r = self.rand() % count
        for idx in range(100):
            if available[idx]:
                if r == 0:
                    return (idx % 10, idx // 10)
                r -= 1
        raise RuntimeError("Failed to pick apple")

    def snek_turn(self, action):
        if action == '.':
            return
        if action not in DIRS:
            raise ValueError(action)
        ndx, ndy = DIRS[action]
        cdx, cdy = self.direction
        if (ndx, ndy) == (-cdx, -cdy):
            return
        self.direction = (ndx, ndy)

    def step(self, action):
        if self.game_over:
            return 'game_over'
        self.snek_turn(action)
        dx, dy = self.direction
        headx, heady = self.snake[0]
        new_head = (headx + dx, heady + dy)
        mod_head = (new_head[0] % 10, new_head[1] % 10)
        apple_hit = (mod_head == self.apple)
        if apple_hit:
            self.snake = [new_head] + self.snake[:self.length]
            self.length += 1
            self.score += 1
            self.apple = self.pick_new_apple()
        else:
            self.snake = [new_head] + self.snake[:self.length-1]
        # Self collision check
        for segment in self.snake[1:self.length]:
            if (segment[0] % 10, segment[1] % 10) == mod_head:
                self.lives -= 1
                if self.lives == 0:
                    self.game_over = True
                    return 'game_over'
                # reset snake for new life
                self.direction = (1,0)
                self.length = 3
                self.snake = [(6,5),(5,5),(4,5)]
                self.apple = self.pick_new_apple()
                return 'life_lost'
        return 'ok_apple' if apple_hit else 'ok'

    def state_signature(self):
        return (tuple((x % 10, y % 10) for x,y in self.snake[:self.length]),
                self.direction,
                tuple(sorted((x % 10, y % 10) for x,y in self.snake[:self.length])),
                self.apple)

if __name__ == '__main__':
    game = SnakeGame()
    print('initial apple:', game.apple)
