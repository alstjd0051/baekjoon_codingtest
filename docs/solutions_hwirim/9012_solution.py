import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    t = int(input_data[0])
    results = []
    
    for i in range(1, t + 1):
        ps = input_data[i]
        count = 0
        is_vps = True
        
        for char in ps:
            if char == '(':
                count += 1
            else:
                count -= 1
            
            # 닫는 괄호가 더 많아지는 순간 VPS 탈락
            if count < 0:
                is_vps = False
                break
        
        # 순회가 끝난 후 count가 0이어야 함
        if is_vps and count == 0:
            results.append("YES")
        else:
            results.append("NO")
            
    print("\n".join(results))

if __name__ == "__main__":
    solve()
