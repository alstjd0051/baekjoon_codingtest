import sys
input = sys.stdin.readline

s = input().strip()

# "::"가 있는 경우
if "::" in s:
    left, right = s.split("::")

    left_parts = left.split(":") if left else []
    right_parts = right.split(":") if right else []

    # 부족한 그룹 개수 계산
    missing = 8 - (len(left_parts) + len(right_parts))

    parts = left_parts + ["0"] * missing + right_parts

# "::"가 없는 경우
else:
    parts = s.split(":")

# 각 그룹을 4자리로 맞추기
parts = [p.zfill(4) for p in parts]

# 출력
print(":".join(parts))