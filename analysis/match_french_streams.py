from pathlib import Path
import ctypes,json,hashlib,collections,time
root=Path(__file__).resolve().parent
fr=(root.parent/'upload/Star Ocean FR.smc').read_bytes();linear=(root/'ENG_96Mbit_linear.bin').read_bytes();rows=json.loads((root/'dynamic_reference.json').read_text())
lookup=collections.defaultdict(dict)
for r in rows:
 if 'verified_length' not in r:continue
 n=r['verified_length'];off=r['target_cpu'];data=linear[off:off+n]
 if n not in (32,64):continue
 lookup[data[:32]][data]=(n,r['slot'])
candidates=collections.defaultdict(list)
for i in range(0x8000,0xd0000-2):
 if fr[i+2]>=0xc0:
  p=int.from_bytes(fr[i:i+3],'little');candidates[p&0x3fffff].append((i,p))
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
buf=ctypes.create_string_buffer(fr+bytes(0x20000));out=ctypes.create_string_buffer(65536);result=[];prefix_hits=0
for off,occ in sorted(candidates.items()):
 fn(out,ctypes.byref(buf,off),32);prefix=ctypes.string_at(out,32)
 options=lookup.get(prefix)
 if not options:continue
 prefix_hits+=1;matching=[]
 if prefix in options:matching.append(options[prefix])
 fn(out,ctypes.byref(buf,off),64);actual=ctypes.string_at(out,64)
 if actual in options:matching.append(options[actual])
 if not matching:continue
 n,slot=max(matching)
 result.append({'source_file':off,'length':n,'reference_slot':slot,'pointer_locations':[i for i,p in occ],'cpu_pointers':sorted(set(p for i,p in occ)),'distinct_matching_outputs':len(matching)})
print('candidate sources',len(candidates),'prefix_hits',prefix_hits,'fully matched',len(result),'bytes',sum(x['length'] for x in result),'lengths',collections.Counter(x['length'] for x in result).most_common(10))
(root/'matched_french_streams.json').write_text(json.dumps(result,indent=2))
