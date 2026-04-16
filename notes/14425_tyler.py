import sys

input = sys.stdin.readline

n, m = map(int, input().split())
s = {input().rstrip() for _ in range(n)}

print(sum(input().rstrip() in s for _ in range(m)))
