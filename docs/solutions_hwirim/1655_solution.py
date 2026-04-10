import sys
import heapq

def solve():
    # 대량의 데이터를 빠르게 읽기 위해 sys.stdin.readline 사용
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # 두 개의 힙(Heap)을 활용하여 중간값 관리
    # left_heap: 중간값 이하의 수들을 저장 (최대 힙으로 구현)
    # right_heap: 중간값 초과의 수들을 저장 (최소 힙으로 구현)
    left_heap = []
    right_heap = []
    
    results = []
    
    for i in range(1, n + 1):
        val = int(input_data[i])
        
        # 1. 크기 균형 맞추기 (left_heap의 크기가 right_heap보다 같거나 1 크게 유지)
        if len(left_heap) == len(right_heap):
            heapq.heappush(left_heap, -val)
        else:
            heapq.heappush(right_heap, val)
            
        # 2. 값의 역전 방지 (left의 최대값이 right의 최소값보다 작거나 같아야 함)
        if right_heap and (-left_heap[0] > right_heap[0]):
            max_val = -heapq.heappop(left_heap)
            min_val = heapq.heappop(right_heap)
            
            heapq.heappush(left_heap, -min_val)
            heapq.heappush(right_heap, max_val)
            
        # left_heap의 루트값이 현재의 중간값
        results.append(str(-left_heap[0]))
        
    # 결과 출력
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
