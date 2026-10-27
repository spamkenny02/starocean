"""Record observed prototype requests, retaining inferred physical-source provenance.

Only accepts a physical mapping corroborated by original-ROM observations in the
same CPU bank. This is not a substitute for observing the new key on the original.
"""
from pathlib import Path
import argparse,gzip,json,collections
p=argparse.ArgumentParser();p.add_argument('samples',type=Path);p.add_argument('--requests',type=Path,default=Path(__file__).with_name('patched_runtime_requests.json'));p.add_argument('--catalog',type=Path,default=Path(__file__).with_name('catalog_extended.json.gz'));a=p.parse_args()
catalog=json.loads(gzip.decompress(a.catalog.read_bytes()));requests=json.loads(a.requests.read_text()) if a.requests.exists() else [];bykey={(r['cpu_bank'],r['cpu_address']):r for r in requests};found={}
for s in json.loads(a.samples.read_text()):
 if s['pc'] not in ('0x648096','0x648196'):continue
 assert s['pc']=='0x648096','Channel 1 diagnostics need a channel 1 source sample'
 key=int(s['dma0_source'],16);n=s['dma0_length'] or 65536;found[key]=max(n,found.get(key,0))
pending=collections.Counter()
for s in json.loads(a.samples.read_text()):
 key=int(s.get('dma0_source','0'),16);n=s.get('dma0_length',0)
 if key>=0xc00000 and n and not any(r['cpu_bank']==key>>16 and r['cpu_address']==key&65535 for r in catalog):pending[(key,n)]+=1
for (key,n),count in pending.items():
 if count>=3:found[key]=max(n,found.get(key,0))
for key,n in sorted(found.items()):
 bank=key>>16;addr=key&65535
 deltas={r['source_file']-(((r['cpu_bank']<<16)|r['cpu_address'])&0x3fffff) for r in catalog if r.get('priority')==10 and r['cpu_bank']==bank}
 assert len(deltas)==1,('Ambiguous or unobserved bank mapping',hex(key),deltas)
 off=(key&0x3fffff)+next(iter(deltas));assert 0<=off<0x600000
 old=bykey.get((bank,addr));assert not old or old['source_file']==off
 bykey[(bank,addr)]={'cpu_bank':bank,'cpu_address':addr,'source_file':off,'length':max(n,old['length'] if old else 0),'method':'requested by patched gameplay; physical page inferred from original observations in the same CPU bank; new key not observed on original','priority':9}
 print(hex(key),n,'physical source inferred',hex(off))
a.requests.write_text(json.dumps(sorted(bykey.values(),key=lambda x:(x['cpu_bank'],x['cpu_address'])),indent=2)+'\n')
