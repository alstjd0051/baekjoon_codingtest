import sys

s = sys.stdin.readline().strip()

if "::" in s:
    l, r = s.split("::")
    a = l.split(":") if l else []
    b = r.split(":") if r else []
    g = a + ["0"] * (8 - len(a) - len(b)) + b
else:
    g = s.split(":")

print(":".join(x.zfill(4) for x in g))
