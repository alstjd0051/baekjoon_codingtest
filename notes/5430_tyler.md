# 5430 풀이

## 알고리즘/증명

1. 입력 줄 `[x1,...,xn]`에서 대괄호를 제거하고 쉼표로 나눈 뒤 `deque`에 넣는다. $n = 0$이면 빈 덱이다.
2. `reversed_flag = False`로 두고, 함수 문자열 `p`의 각 문자에 대해:
   - `R`이면 `reversed_flag`를 토글한다.
   - `D`이면 덱이 비어 있으면 에러로 종료한다. 비어 있지 않으면 `reversed_flag`가 참이면 `pop()`, 거짓이면 `popleft()`로 한 칸 버린다.
3. 에러가 없고 `reversed_flag`가 참이면 덱을 한 번 뒤집은 뒤, `[`와 `]` 사이에 원소를 쉼표로 이어 출력한다.

**불변식(직관)**: `reversed_flag`가 거짓일 때의 “앞”은 덱의 왼쪽이고, 참일 때의 “앞”은 덱의 오른쪽이다. `R`을 실제로 적용하는 대신 이 플래그만 바꾸면, 이후 `D`는 항상 “현재의 앞”에 해당하는 쪽에서 제거하는 것과 같다.

## 코드 해석

아래는 제출용 코드 전체인 `notes/5430_tyler.py`와 동일하다.

```python
import sys
from collections import deque

input = sys.stdin.readline

T = int(input())
for _ in range(T):
    p = input().strip()
    n = int(input())
    arr = input().strip()

    if n == 0:
        dq = deque()
    else:
        dq = deque(arr[1:-1].split(","))

    reversed_flag = False
    error = False

    for cmd in p:
        if cmd == "R":
            reversed_flag = not reversed_flag
        else:
            if not dq:
                error = True
                break
            if reversed_flag:
                dq.pop()
            else:
                dq.popleft()

    if error:
        print("error")
    else:
        if reversed_flag:
            dq.reverse()
        print("[" + ",".join(dq) + "]")
```

## 복잡도

테스트 케이스 하나에서 명령 길이를 $|p|$, 배열 길이를 $n$이라 하자.

- **시간**: $O(|p| + n)$ — 명령 순회 $O(|p|)$, 각 `D`는 $O(1)$, 성공 시 마지막 `reverse`가 최대 한 번 $O(n)$.
- **공간**: $O(n)$ — 덱에 원소를 저장한다.
