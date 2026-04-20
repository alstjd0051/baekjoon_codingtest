import sys
from collections import deque

def dfs(adj, v, visited, result):
    visited[v] = True
    result.append(v)
    for neighbor in adj[v]:
        if not visited[neighbor]:
            dfs(adj, neighbor, visited, result)

def bfs(adj, start, visited, result):
    queue = deque([start])
    visited[start] = True
    while queue:
        v = queue.popleft()
        result.append(v)
        for neighbor in adj[v]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    m = int(input_data[1])
    v = int(input_data[2])
    
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u = int(input_data[3 + 2*i])
        vv = int(input_data[4 + 2*i])
        adj[u].append(vv)
        adj[vv].append(u)
        
    # Standard requirement: visit smaller vertex first
    for i in range(1, n + 1):
        adj[i].sort()
        
    dfs_result = []
    dfs_visited = [False] * (n + 1)
    dfs(adj, v, dfs_visited, dfs_result)
    
    bfs_result = []
    bfs_visited = [False] * (n + 1)
    bfs(adj, v, bfs_visited, bfs_result)
    
    print(*(dfs_result))
    print(*(bfs_result))

if __name__ == "__main__":
    solve()
