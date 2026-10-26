from pathlib import Path
import ctypes,collections,json,hashlib
root=Path(__file__).resolve().parent
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
rows=json.loads((root/'dynamic_reference.json').read_text());eng=(root/'Star_Ocean.smc').read_bytes();fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes()
by_ptr={}
for r in rows:
 if 'verified_length' not in r:continue
 p=(r['bank']<<16)+(r['source_file']&65535)
 if p not in by_ptr or r['verified_length']>by_ptr[p]['verified_length']:by_ptr[p]=r
manifest=[];rejected=collections.Counter();dest=root/'dynamic_fr';dest.mkdir(exist_ok=True)
masked_eng=bytearray(eng);masked_fr=bytearray(fr)
for j in range(0x40000,0xc0000-3):
 p=int.from_bytes(eng[j:j+3],'little');q=int.from_bytes(fr[j:j+3],'little')
 if p in by_ptr and q>=0xc00000:
  masked_eng[j:j+3]=b'\x00'*3;masked_fr[j:j+3]=b'\x00'*3

for i in range(0x40000,0xc0000-3):
 p=int.from_bytes(eng[i:i+3],'little')
 if p not in by_ptr:continue
 # accept only structurally stable pointer locations, requiring 5 bytes before and 3 after identical.
 if masked_eng[i-8:i]!=masked_fr[i-8:i] or masked_eng[i+3:i+11]!=masked_fr[i+3:i+11]:rejected['changed_context']+=1;continue
 q=int.from_bytes(fr[i:i+3],'little')
 if q<0xc00000:rejected['non_rom_pointer']+=1;continue
 ref=by_ptr[p];page=ref['source_file']//0x100000
 # preserve the mapped 1MiB page group, replacing the low nibble of the bank and low16.
 off=(q&0x3fffff)+(ref['source_file']-(p&0x3fffff));n=ref['verified_length']
 buf=ctypes.create_string_buffer(fr[off:off+max(65536,n*2)]+bytes(65536));out=ctypes.create_string_buffer(n);fn(out,buf,n)
 filename=f'{off:06x}_{n:05x}.bin';(dest/filename).write_bytes(out.raw)
 manifest.append({'pointer_location':i,'english_pointer':p,'french_pointer':q,'french_file_offset':off,'length':n,'file':filename,'reference_slot':ref['slot'],'sha256':hashlib.sha256(out.raw).hexdigest()})
(root/'dynamic_fr_manifest.json').write_text(json.dumps(manifest,indent=2))
print('pointer locations',len(manifest),'distinct English streams',len(set(m['english_pointer'] for m in manifest)),'French blocks',len(set(m['file'] for m in manifest)),'bytes',sum(p.stat().st_size for p in dest.glob('*.bin')),'rejected',rejected)
