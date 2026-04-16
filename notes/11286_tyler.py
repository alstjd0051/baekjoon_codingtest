import sys,heapq
input=sys.stdin.readline
h=[]
o=[]
for _ in[0]*int(input()):
 x=int(input())
 if x:heapq.heappush(h,(abs(x),x))
 else:o+=[str(heapq.heappop(h)[1])if h else'0']
print('\n'.join(o))
