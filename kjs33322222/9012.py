T = int(input())

for _ in range(T):
    s = input().strip()
    count = 0
    valid = True

    for ch in s:
        if ch == '(':
            count += 1
        else:
            count -=1

        if count < 0:
            valid = False
            break

    if count == 0 and valid:
        print("YES")
    else:
        print("NO")