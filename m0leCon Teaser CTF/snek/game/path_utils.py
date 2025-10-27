from collections import deque

DIRS = {
    'W': (0,-1),
    'S': (0,1),
    'A': (-1,0),
    'D': (1,0),
}
ACTIONS = ['.', 'W', 'A', 'S', 'D']

def step_state(snake, direction, action, apple):
    dx, dy = direction
    if action != '.':
        ndx, ndy = DIRS[action]
        if (ndx, ndy) != (-dx, -dy):
            dx, dy = ndx, ndy
    headx, heady = snake[0]
    new_head = (headx + dx, heady + dy)
    mod_head = (new_head[0] % 10, new_head[1] % 10)
    # build new snake
    new_snake = [new_head] + snake
    apple_hit = (mod_head == apple)
    if not apple_hit:
        new_snake = new_snake[:-1]
    # check collision
    for seg in new_snake[1:]:
        if (seg[0] % 10, seg[1] % 10) == mod_head:
            return None, (dx, dy), 'collision'
    return new_snake, (dx, dy), 'apple' if apple_hit else 'ok'

def find_path_to_apple(snake, direction, apple):
    start_sig = (tuple((x%10, y%10) for x,y in snake), direction)
    queue = deque([(list(snake), direction, [])])
    visited = {start_sig}
    while queue:
        snake, direction, path = queue.popleft()
        for action in ACTIONS:
            new_snake, new_dir, status = step_state(list(snake), direction, action, apple)
            if status == 'collision':
                continue
            new_path = path + [action]
            if status == 'apple':
                return new_path
            sig = (tuple((x%10, y%10) for x,y in new_snake), new_dir)
            if sig not in visited:
                visited.add(sig)
                queue.append((new_snake, new_dir, new_path))
    return None

def find_crash_sequence(snake, direction, apple, max_len=6):
    from itertools import product
    for length in range(1, max_len+1):
        for seq in product(ACTIONS, repeat=length):
            cur_snake = [tuple(s) for s in snake]
            cur_dir = direction
            valid = True
            for action in seq:
                cur_snake, cur_dir, status = step_state(cur_snake, cur_dir, action, apple)
                if status == 'collision':
                    return list(seq)
                if status == 'apple':  # avoid sequences that eat apple
                    valid = False
                    break
            if not valid:
                continue
    return None
