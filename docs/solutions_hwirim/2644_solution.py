import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    target_a = int(input_data[1])
    target_b = int(input_data[2])
    m = int(input_data[3])
    
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u = int(input_data[4 + 2*i])
        v = int(input_data[5 + 2*i])
        adj[u].append(v)
        adj[v].append(u)
    
    queue = deque([(target_a, 0)])
    visited = [False] * (n + 1)
    visited[target_a] = True
    
    while queue:
        curr, dist = queue.popleft()
        
        if curr == target_b:
            print(dist)
            return
        
        for neighbor in adj[curr]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, dist + 1))
                
    print(-1)

if __name__ == "__main__":
    solve()
