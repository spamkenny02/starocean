from pathlib import Path
import json,collections
s=Path('analysis/Star_Ocean.smc').read_bytes();rows=json.load(open('analysis/dynamic_reference.json'))
keys={((r['source_file']&65535)+(r['bank']<<16)) for r in rows if 'source_file' in r}
hits=[];counts=collections.Counter()
for i in range(len(s)-2):
 p=s[i]|s[i+1]<<8|s[i+2]<<16
 if p in keys:hits.append((i,p));counts[i//32768]+=1
print(counts.most_common(30));print('sample',[(hex(a),hex(b)) for a,b in hits[:40]])
Path('analysis/pointer_hits.json').write_text(json.dumps(hits))
