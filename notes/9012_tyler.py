for _ in[0]*int(input()):
 c=0
 for i in input():
  c+=1-2*(i>'(')
  if c<0:break
 print('NO'if c else'YES')