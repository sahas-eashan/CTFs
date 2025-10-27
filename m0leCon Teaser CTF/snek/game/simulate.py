import ctypes

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

RAND_MAX = 0x7fffffff

def rand():
    return libc.rand()

# initial snake positions
snake = [(6,5),(5,5),(4,5)]
length = 3

available = [1]*100
count = 100
for (x,y) in snake:
    idx = (y % 10)*10 + (x % 10)
    if available[idx]:
        available[idx] = 0
        count -= 1

r = rand() % count
idx = -1
for i in range(100):
    if available[i]:
        if r == 0:
            idx = i
            break
        r -= 1
apple = (idx % 10, idx // 10)
print("first apple:", apple)
