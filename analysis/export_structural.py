from pathlib import Path
import ctypes,json,hashlib,collections
root=Path(__file__).resolve().parent
fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes();enlinear=(root/'ENG_96Mbit_linear.bin').read_bytes();r=json.loads((root/'dynamic_reference.json').read_text());ref={}
for z in r:
 if 'verified_length' in z:
  p=(z['bank']<<16)|(z['source_file']&65535)
  if p not in ref or z['verified_length']>ref[p]['verified_length']:ref[p]=z
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
def dec(off,n):
 a=ctypes.create_string_buffer(fr[off:off+max(65536,2*n)]+bytes(65536));b=ctypes.create_string_buffer(n);fn(b,a,n);return b.raw
rows=json.loads((root/'structural_tables.json').read_text());dest=root/'structural_fr';dest.mkdir(exist_ok=True);same=0
for x in rows:
 off=(x['french_pointer']&0x3fffff)+x['source_page_delta'];n=x['length'];b=dec(off,n);h=2166136261
 name=f'{off:06x}_{n:05x}.bin';(dest/name).write_bytes(b);x.update(source_file=off,file=name,sha256=hashlib.sha256(b).hexdigest());z=ref[x['english_pointer']];a=z['target_cpu'];x['equals_english_block']=b==enlinear[a:a+n];same+=x['equals_english_block']
(root/'structural_tables.json').write_text(json.dumps(rows,indent=2));print('structural matches',len(rows),'identical blocks',same,'different',len(rows)-same)
trace=collections.Counter()
for l in (root/'runs/fr_verified/sdd1.csv').read_text().splitlines():
 bank,addr,off,n,checksum=l.split(',');trace[(int(bank,16),int(addr,16),int(off),int(n),int(checksum,16))]+=1
dest=root/'observed_fr';dest.mkdir(exist_ok=True);manifest=[]
for (bank,addr,off,n,expected_hash),count in sorted(trace.items()):
 b=dec(off,n);h=2166136261
 for value in b:h=((h^value)*16777619)&0xffffffff
 assert h==expected_hash,(off,n,h,expected_hash)
 name=f'{off:06x}_{n:05x}.bin';(dest/name).write_bytes(b);manifest.append({'cpu_bank':bank,'cpu_address':addr,'source_file':off,'length':n,'occurrences':count,'runtime_fnv1a32':f'{expected_hash:08x}','file':name,'sha256':hashlib.sha256(b).hexdigest()})
(root/'observed_fr.json').write_text(json.dumps(manifest,indent=2));print('observed',sum(trace.values()),'distinct transfers',len(trace),'bytes',sum(p.stat().st_size for p in dest.glob('*.bin')))
