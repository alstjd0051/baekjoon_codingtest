import sys
from collections import deque

def solve():
    # 입력 처리 가속화
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    t = int(input_data[0])
    line_idx = 1
    
    results = []
    
    for _ in range(t):
        p = input_data[line_idx]
        n = int(input_data[line_idx + 1])
        arr_str = input_data[line_idx + 2]
        line_idx += 3
        
        # [1,2,3,4] 형태를 파싱
        if n == 0:
            dq = deque()
        else:
            # 양 끝의 [, ] 제거 후 쉼표로 분리
            dq = deque(arr_str[1:-1].split(','))
            
        is_reversed = False
        is_error = False
        
        for cmd in p:
            if cmd == 'R':
                is_reversed = not is_reversed
            elif cmd == 'D':
                if not dq:
                    is_error = True
                    break
                
                # 가상 뒤집기 상태에 따라 앞에서 뺄지 뒤에서 뺄지 결정
                if is_reversed:
                    dq.pop()
                else:
                    dq.popleft()
        
        if is_error:
            results.append("error")
        else:
            # 최종 상태가 역방향이면 실제로 뒤집어서 출력
            if is_reversed:
                dq.reverse()
            results.append("[" + ",".join(dq) + "]")
            
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
