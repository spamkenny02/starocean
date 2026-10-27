"""Derive second 64-byte transfers from repeated, structured sprite table runs.

The French routine at source 0x39900 reads a 24-bit first pointer at Y, an
8-bit displacement at Y+3, then performs two 64-byte DMAs. The second source
wraps within the same CPU bank. These are static deductions, not runtime reads.
"""
from pathlib import Path
import ctypes as C,collections,gzip,hashlib,json
root=Path(__file__).resolve().parent
source=(root.parent/'upload/Star Ocean FR.smc').read_bytes();assert hashlib.sha256(source).hexdigest()=='a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd'
signature=bytes.fromhex('b900008f024300b9030029ff00187900008500e220')
assert source[0x39906:0x39906+len(signature)]==signature
rows=json.loads(gzip.decompress((root/'paired_dma_anchors.json.gz').read_bytes()));by={(r['cpu_bank']<<16)|r['cpu_address']:r for r in rows};lib=C.CDLL(str(root/'sdd1.so'));decode=getattr(lib,'_Z15SDD1_decompressPhS_i');decode.argtypes=[C.c_void_p,C.c_void_p,C.c_int];lib.SO_SDD1_input_span.argtypes=[C.c_void_p];spans={};candidates={}
for i in range(0x8000,0xd0000-8):
 first=int.from_bytes(source[i:i+3],'little');d=source[i+3];r=by.get(first)
 if not r or r['length']<64 or not d:continue
 off=r['source_file']
 if off not in spans:
  ib=C.create_string_buffer(source[off:off+65536]+bytes(65536));ob=C.create_string_buffer(64);decode(ob,ib,64);spans[off]=lib.SO_SDD1_input_span(ib)
 if d not in (spans[off]-1,spans[off]):continue
 second=(first&0xff0000)|((first+d)&65535);physical=(off&~65535)|(second&65535)
 if physical<0x600000:candidates[i]={'table_offset':i,'first_pointer':first,'displacement':d,'second_pointer':second,'source_file':physical,'length':64,'decoder_read_span':spans[off]}
accepted=[]
for i,r in candidates.items():
 # At least two consecutive nine-byte entries; isolated pointer-like bytes fail.
 if any(all(j in candidates for j in [start,start+9]) for start in [i-9,i]):accepted.append(r)
text=json.dumps(accepted,indent=2)+'\n'
with gzip.GzipFile(filename=str(root/'paired_dma_sources.json.gz'),mode='wb',mtime=0) as z:z.write(text.encode())
keys={r['second_pointer'] for r in accepted};expected={0xf64345,0xf42349,0xebc443,0xebc3d8,0xf2fd90,0xf2aca4,0xed4576,0xec3032}
print(json.dumps({'candidate_entries':len(candidates),'accepted_entries':len(accepted),'distinct_second_sources':len(keys),'second_keys_not_in_anchor_set':len(keys-by.keys()),'identified_missing_keys_covered':[hex(k) for k in sorted(expected&keys)],'missing_identified_keys':[hex(k) for k in sorted(expected-keys)]},indent=2))
