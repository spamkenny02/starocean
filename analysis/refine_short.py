exec(open('analysis/dynamic.py').read().split('rows=[]')[0])
rows=json.loads((root/'dynamic_reference.json').read_text());ptrs=sorted(set(r['target_cpu'] for r in rows));length={a:b-a for a,b in zip(ptrs,ptrs[1:])};stats=collections.Counter()
for r in rows:
 r['allocation']=length.get(r['target_cpu'],128)
 if not r.get('unresolved'):continue
 n=min(32,r['allocation']);d=rom[r['target_cpu']:r['target_cpu']+n]
 for shift in range(128):
  off=((r['bank']&63)<<16)+((r['slot']-shift)&65535)
  if dec(src,off,n)==d:
   r.update(source_file=off,shift=shift);r.pop('unresolved');stats['resolved']+=1;break
 else:stats['unresolved']+=1
print(stats)
(root/'dynamic_reference.json').write_text(json.dumps(rows,indent=2))
