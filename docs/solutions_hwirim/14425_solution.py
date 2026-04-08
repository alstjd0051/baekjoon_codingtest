import sys

def solve():
    # 입력 속도 향상
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])
    
    # 집합 S에 포함된 문자열들을 set에 저장 (평균 O(1) 탐색 가능)
    s_set = set(input_data[2:2+n])
    
    # 검사해야 하는 문자열들
    queries = input_data[2+n:2+n+m]
    
    count = 0
    for query in queries:
        if query in s_set:
            count += 1
            
    print(count)

if __name__ == "__main__":
    solve()
