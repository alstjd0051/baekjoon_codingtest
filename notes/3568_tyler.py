import sys

s = sys.stdin.readline().strip().split()
base = s[0]

for x in s[1:]:
    x = x.rstrip(",;")
    i = 0
    while i < len(x) and x[i].isalpha():
        i += 1

    name = x[:i]
    mod = x[i:]

    t = []
    j = len(mod) - 1
    while j >= 0:
        if mod[j] == "]":
            t.append("[]")
            j -= 2
        else:
            t.append(mod[j])
            j -= 1

    print(base + "".join(t), name + ";")
