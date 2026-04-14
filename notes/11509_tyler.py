import sys
from collections import defaultdict

input = sys.stdin.readline

n = int(input())
h = list(map(int, input().split()))

d = defaultdict(int)
a = 0

for x in h:
    if d[x]:
        d[x] -= 1
    else:
        a += 1
    d[x - 1] += 1

print(a)
