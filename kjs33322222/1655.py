import sys
import heapq
input = sys.stdin.readline

n = int(input())

left = []
right = []

for _ in range(n):
    x = int(input())

    if len(left) == len(right):
        heapq.heappush(left, -x)
    else:
        heapq.heappush(right, x)

    if right and -left[0] > right[0]:
        left_top = -heapq.heappop(left)
        right_top = heapq.heappop(right)

        heapq.heappush(left, -right_top)
        heapq.heappush(right, left_top)

    print(-left[0])