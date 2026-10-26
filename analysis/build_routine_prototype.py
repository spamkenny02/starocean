from pathlib import Path
import ctypes,json,collections,hashlib
root=Path(__file__).resolve().parent
src=(root.parent/'upload/Star Ocean FR.smc').read_bytes();assert hashlib.sha256(src).hexdigest()=='a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd','Unexpected French input ROM';ref=json.loads((root/'observed_fr.json').read_text());fr=bytearray(src)
# A tiny label assembler for the audited instruction sequence below.
code=bytearray();labels={};fix=[]
def emit(h):code.extend(bytes.fromhex(h))
def label(s):labels[s]=len(code)
def branch(op,target):emit(op);fix.append((len(code),target));emit('00')
label('entry');emit('08 c2 30 48 da 8b e2 20 a9 00 48 ab')
emit('ad 00 43 29 08');branch('f0','pass')
emit('ad 04 43 c9 c0');branch('90','pass')
emit('48 c2 20 ad 02 43 48 e2 20 ad 00 43 48 ae 02 43 a3 04')
label('lookup');emit('df 00 00 60');branch('f0','found')
emit('48 bf 00 00 60');branch('f0','missing');emit('68 e8');branch('80','lookup')
label('found');emit('bf 00 00 61 8d 02 43 bf 00 00 62 8d 03 43 bf 00 00 63 8d 04 43 ad 00 43 29 f7 8d 00 43 a3 08 8d 0b 42 68 8d 00 43 c2 20 68 8d 02 43 e2 20 68 8d 04 43');branch('80','done')
label('pass');emit('a3 04 8d 0b 42')
label('done');emit('ab c2 30 fa 68 28 6b')
label('missing');emit('68');label('trap');branch('80','trap')
for at,target in fix:
 delta=labels[target]-(at+1);assert -128<=delta<128,(at,target,delta);code[at]=delta&255
# The SPC700 upload reads raw data through the original S-DD1 page-4 window.
audio_signature=bytes.fromhex('a9048f064800a9058f0748008ba20000a97f48ab')
audio_start=src.find(audio_signature);assert audio_start>=0 and src.find(audio_signature,audio_start+1)<0
bank_at=audio_start+len(audio_signature)+4
assert src[bank_at-1:bank_at+2]==bytes.fromhex('a9e322')
fr[bank_at]=0x43
# Port the two raw-bank table readers used by SPC700 uploads.
helper=bytes.fromhex('bd0200c9e0900338e9a060')
helper_at=0x7ada;assert src[helper_at:helper_at+len(helper)]==b'\xff'*len(helper)
fr[helper_at:helper_at+len(helper)]=helper
for call_at in [0x863d,0x86dd]:
 assert src[call_at:call_at+3]==bytes.fromhex('bd0200')
 fr[call_at:call_at+3]=bytes([0x20,helper_at&255,helper_at>>8])
# Move original SRAM references to the address window retained by this mapper.
for i in range(0x8000,0xd400-3):
 if src[i] in [0x8f,0xaf,0xbf,0x9f] and src[i+3]==0x70:fr[i+3]=0x30
linear=bytearray(0xc00000)
for o in range(0,0x400000,65536):
 linear[0x800000+o:0x808000+o]=fr[o:o+32768]
 linear[o:o+32768]=fr[o+32768:o+65536]
linear[0x400000:0x600000]=fr[0x400000:0x600000]
# Populate the open-addressed lookup by CPU source address. This corpus covers only the observed opening.
streams={}
for r in ref:
 key=(r['cpu_bank'],r['cpu_address'])
 if key in streams:assert streams[key]['source_file']==r['source_file']
 if key not in streams or r['length']>streams[key]['length']:streams[key]=r
lib=ctypes.CDLL(str(root/'sdd1.so'));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
end=0x650000;placed=[]
for (bank,addr),r in sorted(streams.items()):
 n=r['length'];off=r['source_file'];a=ctypes.create_string_buffer(src[off:off+max(65536,n*2)]+bytes(65536));b=ctypes.create_string_buffer(n);fn(b,a,n)
 if (end&65535)+n>65536:end=(end+65535)&~65535
 assert end+n<0x7e0000
 linear[end:end+n]=b.raw
 slot=addr
 while linear[0x600000+slot]:slot=(slot+1)&65535
 linear[0x600000+slot]=bank;linear[0x610000+slot]=end&255;linear[0x620000+slot]=end>>8&255;linear[0x630000+slot]=end>>16
 placed.append(dict(r,slot=slot,target_cpu=end));end+=n
linear[0x648000:0x648000+len(code)]=code
# Replace full verified instruction signatures, preserving the preceding LDA #$01 effect.
hooks=[]
for old in [bytes.fromhex('a9018d01488d0b42'),bytes.fromhex('a9018f01480048688f0b4200')]:
 pos=0
 while True:
  i=src.find(old,pos,0xd0000)
  if i<0:break
  replacement=bytes.fromhex('a90122008064')+bytes([0xea])*(len(old)-6)
  fr[i:i+len(old)]=replacement;hooks.append({'source_offset':i,'old':old.hex(),'new':replacement.hex()});pos=i+len(old)
# All executed compressed DMA call sites must be inside one of these replacements.
executed=set(json.loads((root/'observed_callsites.json').read_text()))
for pc in executed:
 endoff=(pc>>16&63)*65536+(pc&65535)
 assert any(x['source_offset']<=endoff-1<x['source_offset']+len(bytes.fromhex(x['old'])) for x in hooks),hex(pc)
# Recopy modified code, preserving the lookup/data regions.
for o in range(0,0x400000,65536):
 linear[0x800000+o:0x808000+o]=fr[o:o+32768];linear[o:o+32768]=fr[o+32768:o+65536]
# Bank $00:$8000 mirrors the first 32 KiB for vectors and reset.
linear[0x8000:0x10000]=fr[:32768]
# Keep the S-DD1 cartridge ID only to trigger the explicit decompressed mapper; core disables the chip for this 12MiB image.
gd=bytearray()
for i in range(192):gd+=linear[i*65536+32768:(i+1)*65536]
for i in range(192):gd+=linear[i*65536:i*65536+32768]
(root/'FR_routines_opening_experimental.sfc').write_bytes(gd)
(root/'routine_handler.bin').write_bytes(code)
(root/'routine_port.json').write_text(json.dumps({'prototype':'opening corpus only; incomplete game coverage','raw_audio_bank_patch':{'offset':bank_at,'old':0xe3,'new':0x43},'bank_reader_helper':{'offset':helper_at,'bytes':helper.hex(),'call_offsets':[0x863d,0x86dd]},'sram_references_changed':[i+3 for i in range(0x8000,0xd400-3) if src[i] in [0x8f,0xaf,0xbf,0x9f] and src[i+3]==0x70],'code_cpu':0x648000,'code_size':len(code),'labels':labels,'hooks':hooks,'streams':placed,'data_end':end,'sha256':hashlib.sha256(gd).hexdigest()},indent=2))
print('Built',len(gd),'bytes;',len(hooks),'hooks;',len(streams),'source addresses;',len(code),'code bytes')
