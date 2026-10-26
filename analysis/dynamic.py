from pathlib import Path
import ctypes,collections,json
root=Path(__file__).resolve().parent
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
def dec(b,off,n):
 src=ctypes.create_string_buffer(b[off:off+max(n*2,65536)]+bytes(65536));out=ctypes.create_string_buffer(n);fn(out,src,n);return out.raw
def untangle(b):return b''.join(b[0x600000+i*32768:0x600000+(i+1)*32768]+b[i*32768:(i+1)*32768] for i in range(192))
b=(root/'ENG_96Mbit.bin').read_bytes()[512:];rom=untangle(b);src=(root/'Star_Ocean.smc').read_bytes()
(root/'ENG_96Mbit_linear.bin').write_bytes(rom)
keys=rom[0x600000:0x610000];lo=rom[0x610000:0x620000];hi=rom[0x620000:0x630000];banks=rom[0x630000:0x640000]
rows=[]
for i,k in enumerate(keys):
 if not k:continue
 ptr=lo[i]+hi[i]*256+banks[i]*65536
 rows.append({'slot':i,'bank':k,'target_cpu':ptr})
print('entries',len(rows))
print('sample',rows[:10])
# lower banks 00-3f have ROM only above8000; destination pointer maps to linear ROM by cpu address.
def get_target(ptr,n):
 bank=ptr>>16
 if bank>=0xc0:ptr-=0x400000
 return rom[ptr:ptr+n]
stats=collections.Counter()
for r in rows:
 d=get_target(r['target_cpu'],64);matches=[]
 for shift in range(64):
  off=((r['bank']&0x3f)<<16)+((r['slot']-shift)&65535)
  if dec(src,off,64)==d:matches.append(shift)
 if matches:r['source_file']=((r['bank']&0x3f)<<16)+((r['slot']-matches[0])&65535);r['shift']=matches[0]
 else:r['unresolved']=True
 stats[tuple(matches)]+=1
print('MATCHED',sum(not r.get('unresolved') for r in rows),'UNRESOLVED',sum(bool(r.get('unresolved')) for r in rows),'MAX SHIFT',max(r.get('shift',0) for r in rows))
(root/'dynamic_reference.json').write_text(json.dumps(rows,indent=2))
