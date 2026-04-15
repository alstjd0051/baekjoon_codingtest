import sys

def get_dist(a, b):
    dist = 0
    for i in range(4):
        if a[i] != b[i]:
            dist += 1
    return dist

def solve():
    input = sys.stdin.read().split()
    if not input:
        return
    
    T = int(input[0])
    idx = 1
    
    results = []
    for _ in range(T):
        N = int(input[idx])
        idx += 1
        mbtis = input[idx:idx+N]
        idx += N
        
        if N > 32:
            results.append("0")
            continue
            
        min_dist = float('inf')
        for i in range(N):
            for j in range(i+1, N):
                for k in range(j+1, N):
                    d = get_dist(mbtis[i], mbtis[j]) + get_dist(mbtis[j], mbtis[k]) + get_dist(mbtis[i], mbtis[k])
                    if d < min_dist:
                        min_dist = d
        results.append(str(min_dist))
    
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
