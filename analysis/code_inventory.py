from pathlib import Path
import json,collections
root=Path(__file__).resolve().parent
eng=(root/'Star_Ocean.smc').read_bytes();fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes();linear=(root/'ENG_96Mbit_linear.bin').read_bytes();patched=bytearray()
for o in range(0,0x400000,65536):patched+=linear[0x800000+o:0x808000+o]+linear[o:o+32768]
patched+=linear[0x400000:0x600000]
runs=[]
for i in range(0xd0000):
 if eng[i]!=patched[i]:
  if runs and i-runs[-1][1]<=8:runs[-1][1]=i+1
  else:runs.append([i,i+1])
result=[]
for a,b in runs:
 lo=max(0,a-8);hi=min(len(eng),b+8);pattern=eng[lo:hi];pos=0;hits=[]
 while True:
  p=fr.find(pattern,pos,0xd0000)
  if p<0:break
  hits.append(p+a-lo);pos=p+1
 result.append({'english_offset':a,'end':b,'old':eng[a:b].hex(),'new':bytes(patched[a:b]).hex(),'exact_context_hits_fr':hits,'same_offset_original_matches':eng[a:b]==fr[a:b]})
(root/'code_patch_inventory.json').write_text(json.dumps(result,indent=2))
print('edit groups',len(result),'unique exact contexts',sum(len(x['exact_context_hits_fr'])==1 for x in result),'original bytes at same offset',sum(x['same_offset_original_matches'] for x in result))
