import sys

types = [
    b"ISTJ",
    b"ISFJ",
    b"INFJ",
    b"INTJ",
    b"ISTP",
    b"ISFP",
    b"INFP",
    b"INTP",
    b"ESTP",
    b"ESFP",
    b"ENFP",
    b"ENTP",
    b"ESTJ",
    b"ESFJ",
    b"ENFJ",
    b"ENTJ",
]

idx = {t: i for i, t in enumerate(types)}

dist = [[0] * 16 for _ in range(16)]
for i in range(16):
    ti = types[i]
    for j in range(16):
        tj = types[j]
        dist[i][j] = sum(ti[p] != tj[p] for p in range(4))

data = sys.stdin.buffer.read().split()
it = iter(data)
t = int(next(it))
out = []

for _ in range(t):
    n = int(next(it))
    cnt = [0] * 16
    for _ in range(n):
        cnt[idx[next(it)]] += 1

    ans = 10
    for i in range(16):
        if cnt[i] == 0:
            continue
        for j in range(i, 16):
            if i != j and cnt[j] == 0:
                continue
            for k in range(j, 16):
                if (k != j and cnt[k] == 0) or (i == j == k and cnt[i] < 3):
                    continue

                if i == j == k:
                    if cnt[i] < 3:
                        continue
                elif i == j:
                    if cnt[i] < 2 or cnt[k] < 1:
                        continue
                elif j == k:
                    if cnt[j] < 2 or cnt[i] < 1:
                        continue
                else:
                    if cnt[k] < 1:
                        continue

                s = dist[i][j] + dist[j][k] + dist[i][k]
                if s < ans:
                    ans = s

    out.append(str(ans))

sys.stdout.write("\n".join(out))

