import sys

s = sys.stdin.readline().strip()
n = len(s)

b1, m1 = 911382323, 1_000_000_007
b2, m2 = 972663749, 1_000_000_009

p1 = [1] * (n + 1)
p2 = [1] * (n + 1)
h1 = [0] * (n + 1)
h2 = [0] * (n + 1)

for i, ch in enumerate(s, 1):
    x = ord(ch) - 96
    p1[i] = p1[i - 1] * b1 % m1
    p2[i] = p2[i - 1] * b2 % m2
    h1[i] = (h1[i - 1] * b1 + x) % m1
    h2[i] = (h2[i - 1] * b2 + x) % m2

st = set()
for i in range(n):
    for j in range(i + 1, n + 1):
        a = (h1[j] - h1[i] * p1[j - i]) % m1
        b = (h2[j] - h2[i] * p2[j - i]) % m2
        st.add((a, b))

print(len(st))
