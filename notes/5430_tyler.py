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
