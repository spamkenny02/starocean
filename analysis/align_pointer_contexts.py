from pathlib import Path
from collections import defaultdict,Counter
import json
root=Path(__file__).resolve().parent
eng=(root/'Star_Ocean.smc').read_bytes();fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes();rows=json.loads((root/'dynamic_reference.json').read_text());refs={}
for r in rows:
 if 'verified_length' in r:
  ptr=r['bank']<<16|(r['source_file']&65535)
  if ptr not in refs or r['verified_length']>refs[ptr]['verified_length']:refs[ptr]=r
lo=0x8000;hi=0xd0000
def ptr(b,i):return int.from_bytes(b[i:i+3],'little')
def masked(b):
 a=bytearray(b)
 for i in range(lo,hi-2):
  if b[i+2]>=0xc0:a[i:i+3]=b'\0\0\0'
 return a
me=masked(eng);mf=masked(fr);index=defaultdict(list)
for j in range(lo+24,hi-24):
 if fr[j+2]>=0xc0:
  key=bytes(mf[j-24:j+27])
  if len(set(key))>=5:index[key].append(j)
result=[];stats=Counter()
for i in range(lo+24,hi-24):
 p=ptr(eng,i)
 if p not in refs:continue
 key=bytes(me[i-24:i+27]);hits=index.get(key,[])
 if len(hits)!=1:stats['nonunique_or_absent']+=1;continue
 j=hits[0];q=ptr(fr,j);r=refs[p]
 result.append({'english_location':i,'french_location':j,'english_pointer':p,'french_pointer':q,'length':r['verified_length'],'source_page_delta':r['source_file']-(p&0x3fffff),'method':'unique masked 51-byte context'})
print('contexts',len(result),'relocated',sum(x['english_location']!=x['french_location'] for x in result),'unique sources',len(set(x['french_pointer'] for x in result)),stats)
(root/'aligned_pointer_contexts.json').write_text(json.dumps(result,indent=2))
