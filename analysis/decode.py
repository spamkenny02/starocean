from pathlib import Path
import zlib
class Reader:
 def __init__(self,b):self.b=b;self.p=0
 def byte(self):v=self.b[self.p];self.p+=1;return v
 def num(self):
  n=0
  while True:
   v=self.byte();n=n*128+(v&127)
   if v<128:return n
 def take(self,n):v=self.b[self.p:self.p+n];self.p+=n;return v
T=[[(0,0,0)]]+ [[(1,n,0)] for n in range(18)]
for m in range(9):T += [[(2,n,m)] for n in [0,*range(4,19)]]
for m in range(6):
 for a in range(1,5):
  for c in range(4,7):T.append([(1,a,0),(2,c,m)])
for m in range(6,9):
 for a in range(1,5):T.append([(1,a,0),(2,4,m)])
for m in range(9):T.append([(2,4,m),(1,1,0)])
assert len(T)==256
src=Path('analysis/Star_Ocean.smc').read_bytes()
r=Reader(next(Path('analysis').rglob('*ENG.xdelta')).read_bytes());assert r.take(5)==bytes.fromhex('d6c3c40004');r.take(r.num());out=bytearray()
while r.p<len(r.b):
 flag=r.byte();sl=r.num();sp=r.num();dl=r.num();end=r.p+dl;tl=r.num();assert r.byte()==0
 nd,ni,na=r.num(),r.num(),r.num();chk=int.from_bytes(r.take(4),'big');data=Reader(r.take(nd));inst=Reader(r.take(ni));addr=Reader(r.take(na));seg=src[sp:sp+sl];w=bytearray();near=[0]*4;same=[0]*768;slot=0
 while inst.p<len(inst.b):
  for op,n,m in T[inst.byte()]:
   if not n:n=inst.num()
   if op==0:w.extend(data.take(1)*n)
   elif op==1:w.extend(data.take(n))
   else:
    if m==0:a=addr.num()
    elif m==1:a=sl+len(w)-addr.num()
    elif m<6:a=near[m-2]+addr.num()
    else:a=same[(m-6)*256+addr.byte()]
    near[slot]=a;slot=(slot+1)%4;same[a%768]=a
    for i in range(n):
     j=a+i;w.append(seg[j] if j<sl else w[j-sl])
 assert len(w)==tl,(len(w),tl)
 assert zlib.adler32(w)==chk,(hex(zlib.adler32(w)),hex(chk))
 assert r.p==end
 out.extend(w)
Path('analysis/ENG_96Mbit.bin').write_bytes(out)
print('Decoded and verified',len(out),'bytes',out[:32])
