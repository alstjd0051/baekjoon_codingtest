# 1655 풀이

## 핵심 아이디어

매번 전체를 정렬하면 $O(N^2)$이라 시간 초과이므로, **최대 힙**과 **최소 힙** 두 개로 “왼쪽 절반”과 “오른쪽 절반”을 나눠서 중앙값을 $O(\log N)$에 구한다.

- `a`: 왼쪽 절반을 **최대 힙**으로 저장 (`heapq`는 최소 힙만 되므로 값에 `-`를 붙여 저장)
- `b`: 오른쪽 절반을 **최소 힙**으로 저장

불변식: 항상 `len(a) == len(b)` 또는 `len(a) == len(b) + 1` (왼쪽이 하나 더 많거나 같음).  
이때 **중앙값(짝수 개일 때는 두 중앙값 중 작은 것)**은 항상 `a`의 루트, 즉 `-a[0]`이다.

## 숏코딩 트릭

매 수 `x`마다 “어느 힙에 넣을지” 분기하는 대신, 다음 순서로 처리한다.

1. `heapq.heappush(a, -x)` — 일단 왼쪽에 넣는다.
2. `heapq.heappush(b, -heapq.heappop(a))` — 왼쪽에서 가장 큰 값 하나를 빼서 오른쪽으로 보낸다.
3. 오른쪽이 더 많아지면(`len(a) < len(b)`), `b`에서 가장 작은 값을 다시 왼쪽으로 옮겨 균형을 맞춘다.

이렇게 하면 매 삽입 후에도 위 불변식이 유지된다.

## 코드 해석

```python
import heapq,sys
input=sys.stdin.readline
a,b=[],[]
for _ in[0]*int(input()):
 x=int(input());heapq.heappush(a,-x);heapq.heappush(b,-heapq.heappop(a))
 if len(a)<len(b):heapq.heappush(a,-heapq.heappop(b))
 print(-a[0])
```

- `input=sys.stdin.readline` — $N \le 10^5$이므로 입출력 속도에 유리하다.
- `heapq.heappush(a, -x)` — `x`를 최대 힙처럼 쓰기 위해 음수로 넣는다.
- `heapq.heappush(b, -heapq.heappop(a))` — 왼쪽에서 최댓값에 해당하는 원소를 오른쪽 최소 힙으로 보낸다.
- `if len(a)<len(b): ...` — 오른쪽이 더 길면 한 개를 왼쪽으로 되돌려, 왼쪽이 같거나 하나 더 많게 만든다.
- `print(-a[0])` — 왼쪽 최대 힙의 루트가 곧 답이다.

## 복잡도

- 시간: 삽입마다 힙 연산 $O(\log N)$, 총 $O(N \log N)$
- 공간: $O(N)$
