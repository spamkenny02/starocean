from pathlib import Path
import json,collections,ctypes,hashlib
root=Path(__file__).resolve().parent
eng=(root/'Star_Ocean.smc').read_bytes();fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes();rows=json.loads((root/'dynamic_reference.json').read_text());ref={}
for r in rows:
 if 'verified_length' in r:
  p=(r['bank']<<16)|(r['source_file']&65535)
  if p not in ref or r['verified_length']>ref[p]['verified_length']:ref[p]=r

def ptr(b,i):return int.from_bytes(b[i:i+3],'little')
def sig(b,i,step):return b''.join(b[i+j*step+3:i+(j+1)*step] for j in range(4))
found={};stats={}
for step in [8,9,12]:
 index=collections.defaultdict(list)
 for j in range(0x8000,0xd0000-4*step):
  if all(ptr(fr,j+k*step)>=0xc00000 for k in range(4)):
   key=sig(fr,j,step)
   if len(set(key))>=4:index[key].append(j)
 candidates=0;unique=0
 for i in range(0x8000,0xd0000-4*step):
  if not all(ptr(eng,i+k*step) in ref for k in range(4)):continue
  if len({ptr(eng,i+k*step)&65535 for k in range(4)})<2:continue
  candidates+=1;matches=index.get(sig(eng,i,step),[])
  if len(matches)!=1:continue
  j=matches[0];unique+=1
  for k in range(4):
   p=ptr(eng,i+k*step);q=ptr(fr,j+k*step);r=ref[p]
   key=(i+k*step,j+k*step)
   found[key]={'english_location':key[0],'french_location':key[1],'english_pointer':p,'french_pointer':q,'length':r['verified_length'],'source_page_delta':r['source_file']-(p&0x3fffff),'step':step}
 stats[step]={'english_windows':candidates,'unique_correspondences':unique}
print(stats,'records',len(found),'relocated',sum(a!=b for a,b in found),'streams',len(set((x['french_pointer'],x['length']) for x in found.values())))
(root/'structural_tables.json').write_text(json.dumps(list(found.values()),indent=2))
