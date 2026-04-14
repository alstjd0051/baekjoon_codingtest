import sys

def power(a, b, c):
    if b == 0:
        return 1
    if b == 1:
        return a % c
    
    half = power(a, b // 2, c)
    if b % 2 == 0:
        return (half * half) % c
    else:
        return (half * half * a) % c

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        a, b, c = map(int, line.split())
        print(power(a, b, c))
    except ValueError:
        pass

if __name__ == "__main__":
    solve()
