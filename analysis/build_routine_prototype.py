from pathlib import Path
import ctypes,json,collections,hashlib,argparse,gzip
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Build the experimental Star Ocean FR no-S-DD1 image')
parser.add_argument('--catalog',default='observed_fr.json')
parser.add_argument('--callsites',default='observed_callsites.json')
parser.add_argument('--output',default='FR_routines_opening_experimental.sfc')
parser.add_argument('--report',default='routine_port.json')
parser.add_argument('--channels',default='0')
parser.add_argument('--full-keys',action='store_true',help='Compare all 24 bits of each source address')
args=parser.parse_args();channels=[int(x) for x in args.channels.split(',')];assert channels and len(set(channels))==len(channels) and all(0<=x<=7 for x in channels)

catalog_path=root/args.catalog;catalog_bytes=catalog_path.read_bytes();ref=json.loads(gzip.decompress(catalog_bytes) if catalog_path.suffix=='.gz' else catalog_bytes)
src=(root.parent/'upload/Star Ocean FR.smc').read_bytes();assert hashlib.sha256(src).hexdigest()=='a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd','Unexpected French input ROM';fr=bytearray(src)
# A tiny label assembler for the audited instruction sequence below.
code=bytearray();labels={};fix=[]
def emit(h):code.extend(bytes.fromhex(h))
def label(s):labels[s]=len(code)
def branch(op,target):emit(op);fix.append((len(code),target));emit('00')
label('entry');emit('08 c2 30 48 da 8b e2 20 a9 00 48 ab')
emit('ad 00 43 29 08');branch('f0','pass')
emit('ad 04 43 c9 c0');branch('90','pass')
emit('48 c2 20 ad 02 43 48 e2 20 ad 00 43 48 ae 02 43 a3 04')
label('lookup');emit('df 00 00 60');branch('f0','bank_match' if args.full_keys else 'found')
emit('48 bf 00 00 60');branch('f0','missing');emit('68 e8');branch('80','lookup')
if args.full_keys:
 label('bank_match');emit('48 bf 00 00 65 c3 03');branch('d0','key_mismatch');emit('bf 00 00 66 c3 04');branch('d0','key_mismatch');emit('68');branch('80','found')
 label('key_mismatch');emit('68 e8');branch('80','lookup')
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
data_start=0x670000 if args.full_keys else 0x650000
end=data_start;placed=[]
regions=[(data_start,0x7e0000)]+[(bank*65536+0x8000,(bank+1)*65536) for bank in list(range(1,64))+list(range(0x80,0xc0))]
region_index=0

for (bank,addr),r in sorted(streams.items()):
 n=r['length'];off=r['source_file'];a=ctypes.create_string_buffer(src[off:off+max(65536,n*2)]+bytes(65536));b=ctypes.create_string_buffer(n);fn(b,a,n)
 while True:
  if (end&65535)+n>65536:end=(end+65535)&~65535
  if end+n<=regions[region_index][1]:break
  region_index+=1
  assert region_index<len(regions),'Decompressed data exceeds available ROM space'
  end=regions[region_index][0]
 assert end>>16 not in (0x7e,0x7f)

 linear[end:end+n]=b.raw
 slot=addr
 while linear[0x600000+slot]:slot=(slot+1)&65535
 if args.full_keys:linear[0x650000+slot]=addr&255;linear[0x660000+slot]=addr>>8
 linear[0x600000+slot]=bank;linear[0x610000+slot]=end&255;linear[0x620000+slot]=end>>8&255;linear[0x630000+slot]=end>>16
 placed.append(dict(r,slot=slot,target_cpu=end));end+=n
for item in placed:
 slot=item['cpu_address'];probes=0
 while not (linear[0x600000+slot]==item['cpu_bank'] and (not args.full_keys or (linear[0x650000+slot]|linear[0x660000+slot]<<8)==item['cpu_address'])):
  assert linear[0x600000+slot] and probes<65536,'Missing source in lookup table'
  slot=(slot+1)&65535;probes+=1
 destination=linear[0x610000+slot]|linear[0x620000+slot]<<8|linear[0x630000+slot]<<16
 assert destination==item['target_cpu'],'Ambiguous legacy lookup: rebuild with --full-keys'
code_stride=256 if args.full_keys else 128
for channel in channels:
 channel_code=bytes(code)
 for operand in [0,2,3,4]:
  for opcode in [0xad,0xae,0x8d]:
   old=bytes([opcode,operand,0x43]);new=bytes([opcode,operand+channel*16,0x43]);channel_code=channel_code.replace(old,new)
 address=0x648000+channel*code_stride;assert len(channel_code)<=code_stride
 linear[address:address+len(channel_code)]=channel_code

# Replace full verified instruction signatures, preserving the preceding LDA #$01 effect.
hooks=[]
for channel,old in [(ch,bytes([0xa9,1<<ch])+bytes.fromhex(suffix)) for ch in channels for suffix in ['8d01488d0b42','8f01480048688f0b4200']]:
 pos=0
 while True:
  i=src.find(old,pos,0xd0000)
  if i<0:break
  address=0x648000+channel*code_stride
  replacement=bytes([0xa9,1<<channel,0x22,address&255,address>>8&255,address>>16])+bytes([0xea])*(len(old)-6)
  fr[i:i+len(old)]=replacement;hooks.append({'channel':channel,'source_offset':i,'old':old.hex(),'new':replacement.hex()});pos=i+len(old)
# All executed compressed DMA call sites must be inside one of these replacements.
executed=set(json.loads((root/args.callsites).read_text()))
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
(root/args.output).write_bytes(gd)
(root/'routine_handler.bin').write_bytes(code)
(root/args.report).write_text(json.dumps({'prototype':'experimental; incomplete game coverage','catalog':args.catalog,'channels':channels,'full_keys':args.full_keys,'code_stride':code_stride,'raw_audio_bank_patch':{'offset':bank_at,'old':0xe3,'new':0x43},'bank_reader_helper':{'offset':helper_at,'bytes':helper.hex(),'call_offsets':[0x863d,0x86dd]},'sram_references_changed':[i+3 for i in range(0x8000,0xd400-3) if src[i] in [0x8f,0xaf,0xbf,0x9f] and src[i+3]==0x70],'code_cpu':0x648000,'code_size':len(code),'labels':labels,'hooks':hooks,'streams':placed,'data_end':end,'sha256':hashlib.sha256(gd).hexdigest()},indent=2))
print('Built',len(gd),'bytes;',len(hooks),'hooks;',len(streams),'source addresses;',len(code),'code bytes')
