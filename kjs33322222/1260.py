from collections import deque
import sys

input = sys.stdin.readline

N, M, V = map(int, input().split())

graph = [[] for _ in range(N + 1)]

for _ in range(M):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for i in range(1, N + 1):
    graph[i].sort()


def dfs(start):
    visited = [False] * (N + 1)
    result = []

    def recur(v):
        visited[v] = True
        result.append(v)

        for nxt in graph[v]:
            if not visited[nxt]:
                recur(nxt)

    recur(start)
    return result


def bfs(start):
    visited = [False] * (N + 1)
    result = []
    q = deque([start])
    visited[start] = True

    while q:
        v = q.popleft()
        result.append(v)

        for nxt in graph[v]:
            if not visited[nxt]:
                visited[nxt] = True
                q.append(nxt)

    return result


print(*dfs(V))
print(*bfs(V))