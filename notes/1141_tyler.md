# 1141 풀이

## 아이디어

접두사X 집합의 최대 크기는, 결국 **다른 단어의 접두어가 되는 단어를 모두 제외**했을 때 남는 단어 수와 같다.

- 입력에 같은 단어가 여러 번 나올 수 있으므로 먼저 중복 제거
- 각 단어 `w[i]`에 대해 다른 단어 `w[j]`가 `w[i]`로 시작하면(`startswith`) `w[i]`는 선택 불가
- 끝까지 접두어 관계가 없던 단어만 카운트

`N <= 50`이라 모든 쌍 비교 `O(N^2)`로 충분하다.

## 코드 해석

```python
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
```

- `w`: 중복 제거된 단어 목록
- 바깥 루프는 기준 단어, 안쪽 루프는 비교 대상 단어
- `w[j].startswith(w[i])`가 하나라도 참이면 `w[i]`는 접두어이므로 제외한다.
