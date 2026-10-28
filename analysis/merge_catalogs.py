from pathlib import Path
import json,collections,gzip,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--base',type=Path,help='Incremental mode: retain the published catalog instead of rebuilding private analyses');parser.add_argument('--trace',action='append',type=Path,default=[]);args=parser.parse_args()
catalog={};conflicts=[]
def add(bank,addr,off,n,method,priority):
 k=(bank,addr)
 if off<0 or off>=0x600000 or n<=0 or n>65536:return
 r={'cpu_bank':bank,'cpu_address':addr,'source_file':off,'length':n,'method':method,'priority':priority}
 old=catalog.get(k)
 if old and old['source_file']!=off:
  conflicts.append({'key':k,'old':old,'new':r})
  if priority<=old['priority']:return
 if old and old['source_file']==off:
  r['length']=max(n,old['length'])
  if old['priority']>priority or (old['priority']==priority and n<=old['length']):r['method']=old['method'];r['priority']=old['priority']
 if not old or r!=old:catalog[k]=r
if args.base:
 raw=args.base.read_bytes()
 for x in json.loads(gzip.decompress(raw) if args.base.suffix=='.gz' else raw):add(x['cpu_bank'],x['cpu_address'],x['source_file'],x['length'],x['method'],x['priority'])
else:
 observed=json.loads((root/'observed_fr.json').read_text())
 for x in json.loads((root/'matched_french_streams.json').read_text()):
  for p in x['cpu_pointers']:add(p>>16,p&65535,x['source_file'],x['length'],'byte-identical English 32/64-byte tile',1)
 for filename in ['structural_tables.json','aligned_pointer_contexts.json']:
  for x in json.loads((root/filename).read_text()):
   p=x['french_pointer'];add(p>>16,p&65535,(p&0x3fffff)+x['source_page_delta'],x['length'],'structural correspondence',2)
 for x in observed:add(x['cpu_bank'],x['cpu_address'],x['source_file'],x['length'],'observed opening',10)
traces=args.trace if args.base else [folder/'sdd1.csv' for folder in sorted(root.glob('runs/fr_*'))]
for trace in traces:
 folder=trace.parent
 if args.base:
  meta=json.loads((folder/'run.json').read_text())
  assert meta['rom_sha256']=='a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd','Trace must come from the original French ROM'
 if not trace.exists():
  assert not args.base, f'Missing requested trace: {trace}'
  continue
 for line in trace.read_text().splitlines():
  f=line.split(',')
  if len(f)<5:continue
  add(int(f[0],16),int(f[1],16),int(f[2]),int(f[3]),'observed '+folder.name,10)
paired=root/'paired_dma_sources.json.gz'
if paired.exists():
 for x in json.loads(gzip.decompress(paired.read_bytes())):
  key=x['second_pointer'];add(key>>16,key&65535,x['source_file'],x['length'],'derived second 64-byte DMA from structured nine-byte table run',3)
requests=root/'patched_runtime_requests.json'
if requests.exists():
 for x in json.loads(requests.read_text()):add(x['cpu_bank'],x['cpu_address'],x['source_file'],x['length'],x['method'],9)
assert not conflicts, 'Conflicting physical sources; inspect before merging'
output=sorted(catalog.values(),key=lambda x:(x['cpu_bank'],x['cpu_address']))
text=json.dumps(output,indent=2)+'\n';(root/'catalog_extended.json').write_text(text)
with gzip.GzipFile(filename=str(root/'catalog_extended.json.gz'),mode='wb',mtime=0) as z:z.write(text.encode())
(root/'catalog_conflicts.json').write_text(json.dumps(conflicts,indent=2))
print('catalog',len(output),'maximum-size bytes',sum(x['length'] for x in output),'conflicts',len(conflicts),'observed',sum(x['priority']==10 for x in output))
