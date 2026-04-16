import sys

def solve():
    s1 = sys.stdin.readline().strip()
    s2 = sys.stdin.readline().strip()
    
    n, m = len(s1), len(s2)
    dp = [0] * (m + 1)
    
    for i in range(1, n + 1):
        prev = 0
        for j in range(1, m + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev + 1
            else:
                if dp[j-1] > dp[j]:
                    dp[j] = dp[j-1]
            prev = temp
            
    print(dp[m])

if __name__ == "__main__":
    solve()
