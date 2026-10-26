exec(open('analysis/dynamic.py').read().split('rows=[]')[0])
rows=json.loads((root/'dynamic_reference.json').read_text());stats=collections.Counter()
for r in rows:
 if not r.get('unresolved'):continue
 n=min(32,r['allocation']);d=rom[r['target_cpu']:r['target_cpu']+n]
 for page in range(6):
  for shift in range(128):
   off=page*0x100000+((r['bank']&15)<<16)+((r['slot']-shift)&65535)
   if dec(src,off,n)==d:
    r.update(source_file=off,shift=shift);r.pop('unresolved');stats[page]+=1;break
  if not r.get('unresolved'):break
print(stats,'left',sum(bool(r.get('unresolved')) for r in rows))
(root/'dynamic_reference.json').write_text(json.dumps(rows,indent=2))
