from collections import deque
import sys

input = sys.stdin.readline

n = int(input())
a, b = map(int, input().split())
m = int(input())

graph = [[] for _ in range(n + 1)]

for _ in range(m):
    x, y = map(int, input().split())
    graph[x].append(y)
    graph[y].append(x)

def bfs(start, target):
    visited = [-1] * (n + 1)
    queue = deque([start])
    visited[start] = 0

    while queue:
        now = queue.popleft()

        if now == target:
            return visited[now]

        for nxt in graph[now]:
            if visited[nxt] == -1:
                visited[nxt] = visited[now] + 1
                queue.append(nxt)

    return -1

print(bfs(a, b))
