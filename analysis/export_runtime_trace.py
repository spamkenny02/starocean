"""Publish deduplicated address/hash evidence, without extracted ROM data."""
from pathlib import Path
import argparse, collections, gzip, json
p=argparse.ArgumentParser();p.add_argument('trace',type=Path);p.add_argument('output',type=Path);a=p.parse_args();c=collections.Counter()
for line in a.trace.read_text().splitlines():
 f=line.split(',');assert len(f)==7,f
 c[(int(f[0],16),int(f[1],16),int(f[2]),int(f[3]),f[4],int(f[5],16),int(f[6]))]+=1
rows=[dict(zip(['cpu_bank','cpu_address','source_file','length','fnv32','callsite_pc','channel','count'],(*k,n))) for k,n in sorted(c.items())]
with gzip.GzipFile(filename=str(a.output),mode='wb',mtime=0) as z:z.write((json.dumps(rows,indent=2)+'\n').encode())
print(len(rows),'unique observations;',sum(c.values()),'transfers')
