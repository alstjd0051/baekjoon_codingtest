import sys
input = sys.stdin.readline

t = int(input())  # 테스트 케이스 수

for _ in range(t):
    n = int(input())  # mbti 개수
    mbti = input().split()  # mbti 리스트   

    if n > 32:  # 32명 이상이면 0 출력
        print(0)
        continue

    min_value = 100  # 최소 값 초기화

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                