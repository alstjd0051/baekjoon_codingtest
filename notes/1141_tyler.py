import sys

input = sys.stdin.readline

n = int(input())
w = list({input().rstrip() for _ in range(n)})

a = 0
for i in range(len(w)):
    ok = 1
    for j in range(len(w)):
        if i != j and w[j].startswith(w[i]):
            ok = 0
            break
    a += ok

print(a)
