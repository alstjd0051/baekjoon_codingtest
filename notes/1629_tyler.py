import sys

input = sys.stdin.readline


def mod_pow(a: int, b: int, c: int) -> int:
    a %= c
    r = 1
    while b:
        if b & 1:
            r = (r * a) % c
        a = (a * a) % c
        b >>= 1
    return r


A, B, C = map(int, input().split())
print(mod_pow(A, B, C))
