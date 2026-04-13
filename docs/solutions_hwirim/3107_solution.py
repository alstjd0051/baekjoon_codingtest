import sys

def solve():
    # IPv6 주소 입력
    ipv6 = sys.stdin.readline().strip()
    if not ipv6:
        return

    # :: 를 기준으로 분리 (최대 한 번만 등장함)
    if "::" in ipv6:
        parts = ipv6.split("::")
        # :: 앞쪽 그룹들
        prefix = [p for p in parts[0].split(":") if p]
        # :: 뒤쪽 그룹들
        suffix = [p for p in parts[1].split(":") if p]
        
        # 부족한 만큼 0으로 채워진 그룹 삽입
        missing_count = 8 - (len(prefix) + len(suffix))
        full_groups = prefix + ["0000"] * missing_count + suffix
    else:
        # :: 이 없는 경우 단순히 콜론으로 분리
        full_groups = ipv6.split(":")

    # 각 그룹을 4자리 16진수로 복원 (앞에 0 채우기)
    result_groups = [g.zfill(4) for g in full_groups]
    
    # 다시 콜론으로 연결하여 출력
    print(":".join(result_groups))

if __name__ == "__main__":
    solve()
