import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    unique_substrings = set()
    n = len(s)
    
    # Generate all substrings and add to set
    for i in range(n):
        for j in range(i + 1, n + 1):
            unique_substrings.add(s[i:j])
            
    print(len(unique_substrings))

if __name__ == "__main__":
    solve()
