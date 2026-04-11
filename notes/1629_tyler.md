# 1629 풀이

## 핵심 아이디어

## 알고리즘

지수 $B$를 이진수로 보면 $B = \sum b_i 2^i$이고,

$
A^B = \prod_i (A^{2^i})^{b_i}
$

이다. $b$의 최하위 비트가 1이면 현재 누적값에 $a$를 곱하고, 매 단계마다 $a$는 $a*a \pmod C$로 제곱하고 $b$는 $b >> 1$로 시프트한다.

## 코드 해석

```python
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
```

- `a %= c`: 곱셈 전에 베이스를 \(C\)로 줄여 중간값 폭주를 막는다.
- `b & 1`: 지수의 현재 비트가 1이면 `r`에 `a`를 반영한다.
- `a = (a * a) % c`: 다음 비트를 위해 \(a^{2^k}\)에 해당하는 값을 갱신한다.

## 복잡도

- 시간: $O(\log B)$ (지수 비트 수만큼 반복)
- 공간: $O(1)$
