from collections import deque

DIRS = {
    'W': (0,-1),
    'S': (0,1),
    'A': (-1,0),
    'D': (1,0),
}
ACTIONS = ['W','S','A','D','.' ]

def step(snake, direction, action, apple):
    dx, dy = direction
    if action != '.':
        nd = DIRS[action]
        if nd != (-dx, -dy):
            dx, dy = nd
    headx, heady = snake[0]
    new_head = (headx + dx, heady + dy)
    mod_head = (new_head[0] % 10, new_head[1] % 10)
    apple_hit = (mod_head == apple)
    new_snake = [new_head] + snake
    if not apple_hit:
        new_snake = new_snake[:-1]
    for seg in new_snake[1:]:
        if (seg[0] % 10, seg[1] % 10) == mod_head:
            return None, (dx,dy)
    return new_snake, (dx,dy)

def find_path(snake, direction, apple):
    start_sig = (tuple((x%10,y%10) for x,y in snake), direction)
    queue = deque()
    queue.append((snake, direction, []))
    seen = {start_sig}
    while queue:
        snake, direction, path = queue.popleft()
        head_mod = (snake[0][0] % 10, snake[0][1] % 10)
        if head_mod == apple and path:
            return path
        for action in ACTIONS:
            result = step(list(snake), direction, action, apple)
            if result[0] is None:
                continue
            new_snake, new_dir = result
            new_head_mod = (new_snake[0][0] % 10, new_snake[0][1] % 10)
            if new_head_mod == apple:
                return path + [action]
            sig = (tuple((x%10,y%10) for x,y in new_snake), new_dir)
            if sig not in seen:
                seen.add(sig)
                queue.append((new_snake, new_dir, path + [action]))
    return None

if __name__ == '__main__':
    snake = [(6,4),(6,5),(5,5),(4,5)]
    direction = (0,-1)
    apple = (4,7)
    path = find_path(snake, direction, apple)
    print(path)
