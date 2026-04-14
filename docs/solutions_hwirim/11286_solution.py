import sys
import heapq

def solve():
    # 대량 입력을 위한 readline 최적화
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # 절댓값 힙을 구현하기 위한 최소 힙
    # (abs(x), x) 튜플 형태로 저장하여 절댓값 기준 및 실제 값 기준 정렬을 동시에 해결
    abs_heap = []
    
    results = []
    
    for i in range(1, n + 1):
        x = int(input_data[i])
        
        if x != 0:
            # 0이 아니면 힙에 추가
            heapq.heappush(abs_heap, (abs(x), x))
        else:
            # 0이면 힙에서 제거 및 출력
            if not abs_heap:
                results.append("0")
            else:
                # pop 시 튜플의 (절댓값, 실제값) 중 실제값을 가져옴
                _, val = heapq.heappop(abs_heap)
                results.append(str(val))
                
    # 일괄 출력
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
