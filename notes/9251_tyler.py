import sys

input = sys.stdin.readline

a = input().strip()
b = input().strip()

n, m = len(a), len(b)
dp = [0] * (m + 1)

for i in range(n):
    ndp = [0] * (m + 1)
    ai = a[i]
    for j in range(1, m + 1):
        if ai == b[j - 1]:
            ndp[j] = dp[j - 1] + 1
        else:
            x = ndp[j - 1]
            y = dp[j]
            ndp[j] = x if x >= y else y
    dp = ndp

print(dp[m])
