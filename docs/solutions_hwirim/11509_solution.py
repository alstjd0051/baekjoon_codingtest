import sys

def solve():
    # 입력 속도 향상
    input = sys.stdin.read().split()
    if not input:
        return
    
    n = int(input[0])
    h_list = list(map(int, input[1:]))
    
    # 각 높이에서 날아오고 있는 화살의 개수를 저장하는 배열
    # 최대 높이가 1,000,000이므로 크기를 1,000,001로 설정
    arrows = [0] * 1000001
    count = 0
    
    for h in h_list:
        if arrows[h] > 0:
            # 현재 높이에 날아오는 화살이 있으면 사용
            arrows[h] -= 1
            arrows[h-1] += 1
        else:
            # 현재 높이에 화살이 없으면 새로 쏨
            count += 1
            arrows[h-1] += 1
            
    print(count)

if __name__ == "__main__":
    solve()
