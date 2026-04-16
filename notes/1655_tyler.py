import heapq,sys
input=sys.stdin.readline
a,b=[],[]
for _ in[0]*int(input()):
 x=int(input());heapq.heappush(a,-x);heapq.heappush(b,-heapq.heappop(a))
 if len(a)<len(b):heapq.heappush(a,-heapq.heappop(b))
 print(-a[0])
