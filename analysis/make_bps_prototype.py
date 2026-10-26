from pathlib import Path
import zlib,struct,hashlib,json,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--target',default='FR_routines_opening_experimental.sfc');parser.add_argument('--output',default='Star_Ocean_FR_routines_EXPERIMENTAL.bps');args=parser.parse_args()
src=(root.parent/'upload/Star Ocean FR.smc').read_bytes();target=(root/args.target).read_bytes()
def var(n):
 b=bytearray()
 while True:
  x=n&127;n>>=7
  if not n:b.append(x|128);return b
  b.append(x);n-=1
metadata=b'Star Ocean FR: experimental DMA routine port; incomplete game coverage; consult the build report.'
p=bytearray(b'BPS1')+var(len(src))+var(len(target))+var(len(metadata))+metadata
mapping={0:0}
for bank in range(64):mapping[(0x80+bank+192)*32768]=bank*65536;mapping[(bank+192)*32768]=bank*65536+32768
for bank in range(0x40,0x60):mapping[bank*32768]=bank*65536+32768;mapping[(bank+192)*32768]=bank*65536
source_relative=0
for offset in range(0,len(target),32768):
 data=target[offset:offset+32768];source=mapping.get(offset)
 if source is None:p+=var((len(data)-1)*4+1)+data;continue
 cursor=0
 while cursor<len(data):
  eq=data[cursor]==src[source+cursor];end=cursor+1
  while end<len(data) and (data[end]==src[source+end])==eq:end+=1
  if eq:
   p+=var((end-cursor-1)*4+2);delta=source+cursor-source_relative;p+=var((abs(delta)<<1)|(delta<0));source_relative=source+end
  else:p+=var((end-cursor-1)*4+1)+data[cursor:end]
  cursor=end
p+=struct.pack('<II',zlib.crc32(src),zlib.crc32(target));p+=struct.pack('<I',zlib.crc32(p))
patch=root/args.output;patch.write_bytes(p)
# Independently decode the BPS action stream and verify all three checksums.
pos=4
def num():
 global pos
 n=0;shift=1
 while True:
  x=p[pos];pos+=1;n+=(x&127)*shift
  if x&128:return n
  shift<<=7;n+=shift
assert num()==len(src);assert num()==len(target);metadata_length=num();pos+=metadata_length
output=bytearray();sr=0;tr=0
while pos<len(p)-12:
 a=num();n=(a>>2)+1;mode=a&3
 if mode==0:output+=src[len(output):len(output)+n]
 elif mode==1:output+=p[pos:pos+n];pos+=n
 else:
  d=num();delta=-(d>>1) if d&1 else d>>1
  if mode==2:sr+=delta;output+=src[sr:sr+n];sr+=n
  else:
   tr+=delta
   for i in range(n):output.append(output[tr]);tr+=1
assert bytes(output)==target
assert zlib.crc32(src)==struct.unpack_from('<I',p,len(p)-12)[0]
assert zlib.crc32(output)==struct.unpack_from('<I',p,len(p)-8)[0]
assert zlib.crc32(p[:-4])==struct.unpack_from('<I',p,len(p)-4)[0]
print('BPS verified',len(p),'bytes; source SHA256',hashlib.sha256(src).hexdigest(),'target SHA256',hashlib.sha256(target).hexdigest())
