import sys

def solve():
    # 단어의 개수 N 입력
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    # 집합에는 중복된 단어가 있을 수 있으므로 set으로 중복 제거 후 다시 리스트화
    words = list(set(input_data[1:n+1]))
    
    # 단어들을 길이에 따라 오름차순 정렬
    # 길이가 짧은 단어가 긴 단어의 접두사가 될 수 있으므로 순서대로 확인하기 위함
    words.sort(key=len)
    
    count = 0
    num_unique_words = len(words)
    
    for i in range(num_unique_words):
        is_prefix = False
        # 현재 단어 words[i]가 자신보다 뒤에 있는(즉, 더 긴) 단어들의 접두사인지 확인
        for j in range(i + 1, num_unique_words):
            if words[j].startswith(words[i]):
                is_prefix = True
                break
        
        # 어떤 단어의 접두사도 아니라면 그 단어는 Prefix-X 집합의 원소가 될 수 있음
        if not is_prefix:
            count += 1
            
    print(count)

if __name__ == "__main__":
    solve()
