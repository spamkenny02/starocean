exec(open('analysis/dynamic.py').read().split('rows=[]')[0])
rows=json.loads((root/'dynamic_reference.json').read_text());stats=collections.Counter()
for r in rows:
 if 'source_file' not in r:continue
 n=r['allocation']
 if n>65536 or n<1:r['length_status']='gap';continue
 out=dec(src,r['source_file'],n)
 if out==rom[r['target_cpu']:r['target_cpu']+n]:r['verified_length']=n;stats['full']+=1
 else:r['length_status']='allocation_includes_other_bytes';stats['partial']+=1
print(stats)
(root/'dynamic_reference.json').write_text(json.dumps(rows,indent=2))
