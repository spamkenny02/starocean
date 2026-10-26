from pathlib import Path
import ctypes,re,json,hashlib
root=Path(__file__).resolve().parent
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
def decompress(b,off,n):
 src=ctypes.create_string_buffer(b[off:]+bytes(65536));out=ctypes.create_string_buffer(n);fn(out,src,n);return out.raw
pattern=rb'\xa9([\x08\x09])\x8d\x00\x43\xa9.\x8d\x01\x43\xa2(..)\x8e\x02\x43\xa9(.)\x8d\x04\x43\xa2(..)\x8e\x05\x43'
eng=(root/'Star_Ocean.smc').read_bytes();target=(root/'ENG_96Mbit.bin').read_bytes()[512:]
manifest={}
for label,path in [('eng',root/'Star_Ocean.smc'),('fr',root.parent/'upload/Star Ocean FR.smc')]:
 b=path.read_bytes();entries=[];dest=root/'streams'/label;dest.mkdir(parents=True,exist_ok=True)
 for m in re.finditer(pattern,b):
  if bytes.fromhex('8d0048') not in b[max(0,m.start()-12):m.start()]:continue
  ptr=int.from_bytes(m[2],'little')+(m[3][0]<<16);off=ptr&0x3fffff;n=int.from_bytes(m[4],'little') or 65536
  if ptr<0xc00000:continue
  window=b[max(0,m.start()-60):m.start()]
  if bytes.fromhex('a9048d0648a9058d0748') in window and ptr>=0xe00000:off+=0x200000
  data=decompress(b,off,n);name=f'{ptr:06x}_{n:05x}.bin';(dest/name).write_bytes(data)
  row={'instruction_offset':m.start(),'source_cpu':ptr,'source_file':off,'size':n,'file':name,'sha256':hashlib.sha256(data).hexdigest()}
  if label=='eng':row['found_in_reference']=target.find(data)>=0
  entries.append(row)
 manifest[label]=entries
 print(label,'transfers',len(entries),'unique',len(set(x['file'] for x in entries)),'bytes',sum(p.stat().st_size for p in dest.glob('*.bin')))
 if label=='eng':print('verified reference',sum(x['found_in_reference'] for x in entries),'/',len(entries))
(root/'streams/manifest.json').write_text(json.dumps(manifest,indent=2))
