"""Validate source/table packing independently of the builder's allocation loop."""
from pathlib import Path
import argparse,gzip,json,hashlib,ctypes
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--report',default='routine_port_extended.json');p.add_argument('--rom',default='FR_extended_experimental.sfc');args=p.parse_args()
r=json.loads((root/args.report).read_text());gd=(root/args.rom).read_bytes();source=(root.parent/'upload/Star Ocean FR.smc').read_bytes();assert hashlib.sha256(gd).hexdigest()==r['sha256']
linear=b''.join(gd[0x600000+i*32768:0x600000+(i+1)*32768]+gd[i*32768:(i+1)*32768] for i in range(192))
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
buf=ctypes.create_string_buffer(source+bytes(0x20000));out=ctypes.create_string_buffer(65536);spans=[];max_probe=0
for x in r['streams']:
 n=x['length'];dest=x['target_cpu'];assert (dest&65535)+n<=65536
 fn(out,ctypes.byref(buf,x['source_file']),n);assert ctypes.string_at(out,n)==linear[dest:dest+n]
 slot=x['cpu_address'];probes=0
 while not (linear[0x600000+slot]==x['cpu_bank'] and (not r.get('full_keys') or (linear[0x650000+slot]|linear[0x660000+slot]<<8)==x['cpu_address'])):
  assert linear[0x600000+slot]!=0,'lookup would trap';slot=(slot+1)&65535;probes+=1;assert probes<65536
 actual=linear[0x610000+slot]|linear[0x620000+slot]<<8|linear[0x630000+slot]<<16
 assert actual==dest,'lookup returns a different source with the same bank';max_probe=max(max_probe,probes);spans.append((dest,dest+n))
for a,b in zip(sorted(spans),sorted(spans)[1:]):assert a[1]<=b[0],'overlapping data'
for ch in r['channels']:
 code_start=0x648000+ch*r.get('code_stride',128)
 assert all(end<=code_start or start>=code_start+r['code_size'] for start,end in spans)
print(json.dumps({'streams_verified':len(spans),'max_lookup_probe_distance':max_probe,'sha256':r['sha256'],'channels':r['channels']},indent=2))
