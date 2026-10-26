from pathlib import Path
import json,collections,gzip
root=Path(__file__).resolve().parent
observed=json.loads((root/'observed_fr.json').read_text());catalog={};conflicts=[]
def add(bank,addr,off,n,method,priority):
 k=(bank,addr)
 if off<0 or off>=0x600000 or n<=0 or n>65536:return
 r={'cpu_bank':bank,'cpu_address':addr,'source_file':off,'length':n,'method':method,'priority':priority}
 old=catalog.get(k)
 if old and old['source_file']!=off:
  conflicts.append({'key':k,'old':old,'new':r})
  if priority<=old['priority']:return
 if not old or priority>old['priority'] or (old['source_file']==off and n>old['length']):catalog[k]=r
for x in json.loads((root/'matched_french_streams.json').read_text()):
 for p in x['cpu_pointers']:add(p>>16,p&65535,x['source_file'],x['length'],'byte-identical English 32/64-byte tile',1)
for filename in ['structural_tables.json','aligned_pointer_contexts.json']:
 for x in json.loads((root/filename).read_text()):
  p=x['french_pointer'];add(p>>16,p&65535,(p&0x3fffff)+x['source_page_delta'],x['length'],'structural correspondence',2)
for x in observed:add(x['cpu_bank'],x['cpu_address'],x['source_file'],x['length'],'observed opening',10)
for folder in sorted(root.glob('runs/fr_*')):
 trace=folder/'sdd1.csv'
 if not trace.exists():continue
 for line in trace.read_text().splitlines():
  f=line.split(',')
  if len(f)<5:continue
  add(int(f[0],16),int(f[1],16),int(f[2]),int(f[3]),'observed '+folder.name,10)
output=sorted(catalog.values(),key=lambda x:(x['cpu_bank'],x['cpu_address']))
text=json.dumps(output,indent=2)+'\n';(root/'catalog_extended.json').write_text(text)
with gzip.GzipFile(filename=str(root/'catalog_extended.json.gz'),mode='wb',mtime=0) as z:z.write(text.encode())
(root/'catalog_conflicts.json').write_text(json.dumps(conflicts,indent=2))
print('catalog',len(output),'maximum-size bytes',sum(x['length'] for x in output),'conflicts',len(conflicts),'observed',sum(x['priority']==10 for x in output))
