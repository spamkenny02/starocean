"""Compare private replay evidence; export metrics only, never ROM/state/pixels."""
from pathlib import Path
import argparse, collections, gzip, hashlib, json, ctypes as C
from PIL import Image, ImageChops
p=argparse.ArgumentParser();p.add_argument('reference',type=Path);p.add_argument('target',type=Path);p.add_argument('--catalog',type=Path,default=Path(__file__).with_name('catalog_extended.json.gz'));p.add_argument('--source',type=Path,default=Path(__file__).resolve().parent.parent/'upload/Star Ocean FR.smc');p.add_argument('--min-redirected',type=int,default=1);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def lines(path):
 return [x.split(',') for x in path.read_text().splitlines() if x.strip()] if path.exists() else []
r=lines(a.reference/'sdd1.csv');t=lines(a.target/'plain_dma.csv')
known={(int(x[3]),x[4]) for x in r};unknown=collections.Counter((int(x[0]),x[1]) for x in t if (int(x[0]),x[1]) not in known)
catalog={(x['cpu_bank'],x['cpu_address']):x for x in json.loads(gzip.decompress(a.catalog.read_bytes()))}
target_errors=[];target_checks=0;target_sources=set()
if t and all(len(x)>=4 for x in t):
 source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd'
 lib=C.CDLL(str(Path(__file__).with_name('sdd1.so')));fn=getattr(lib,'_Z15SDD1_decompressPhS_i');fn.argtypes=[C.c_void_p,C.c_void_p,C.c_int]
 for key,n,h in sorted({(int(x[3],16),int(x[0]),x[1]) for x in t}):
  target_sources.add(key);rec=catalog.get((key>>16,key&65535))
  if rec is None or rec['length']<n:target_errors.append({'key':hex(key),'length':n,'reason':'missing or insufficient catalog entry'});continue
  off=rec['source_file'];ib=C.create_string_buffer(source[off:off+max(65536,n*2)]+bytes(65536));ob=C.create_string_buffer(n);fn(ob,ib,n);v=2166136261
  for byte in ob.raw:v=((v^byte)*16777619)&0xffffffff
  target_checks+=1
  if f'{v:08x}'!=h:target_errors.append({'key':hex(key),'length':n,'expected_fnv32':f'{v:08x}','actual_fnv32':h})
missing=[];short=[];wrong=[]
for f in r:
 key=(int(f[0],16),int(f[1],16));x=catalog.get(key)
 if x is None:missing.append(key);continue
 if x['length']<int(f[3]):short.append(key)
 if x['source_file']!=int(f[2]):wrong.append(key)
images=[]
for rp in sorted(a.reference.glob('frame_*.png')):
 tp=a.target/rp.name
 if not tp.exists():continue
 im1=Image.open(rp).convert('RGB');im2=Image.open(tp).convert('RGB')
 images.append({'frame':int(rp.stem.split('_')[1]),'pixel_identical':im1.size==im2.size and ImageChops.difference(im1,im2).getbbox() is None,'reference_png_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'target_png_sha256':hashlib.sha256(tp.read_bytes()).hexdigest()})
samples=json.loads((a.target/'cpu_samples.json').read_text());ri=json.loads((a.reference/'run.json').read_text());ti=json.loads((a.target/'run.json').read_text())
result={'status':'experimental; incomplete game coverage','source_sha256':ri['rom_sha256'],'target_sha256':ti['rom_sha256'],'frames':ti['frames'],'reference_frames':ri['frames'],'reference_start_frame':ri.get('start_frame',0),'target_start_frame':ti.get('start_frame',0),'reference_transfers':len(r),'reference_unique_cpu_sources':len({(x[0],x[1]) for x in r}),'reference_callsites':sorted({x[5] for x in r}),'reference_channels':sorted({int(x[6]) for x in r}),'catalog_addresses':len(catalog),'catalog_observed_addresses':sum(x['priority']==10 for x in catalog.values()),'catalog_requested_only_addresses':sum(x['priority']==9 for x in catalog.values()),'catalog_other_inferred_addresses':sum(x['priority']<9 for x in catalog.values()),'missing_sources':len(set(missing)),'insufficient_catalog_lengths':len(set(short)),'wrong_physical_sources':len(set(wrong)),'redirected_transfers':len(t),'minimum_redirected_required':a.min_redirected,'target_handler_pcs':sorted({x[2] for x in t}),'distinct_redirected_length_fnv32_pairs':len({(x[0],x[1]) for x in t}),'unknown_transfer_hash_pairs':[{'length':k[0],'fnv32':k[1],'count':v} for k,v in sorted(unknown.items())],'target_unique_cpu_sources':len(target_sources),'target_source_length_hash_checks':target_checks,'target_decompression_errors':target_errors,'handler_trap_samples':sum(x['pc'] in ('0x648096','0x648196') for x in samples),'trap_dma_sources':sorted({x.get('dma0_source','not recorded') for x in samples if x['pc'] in ('0x648096','0x648196')}),'target_remaining_sdd1_transfers':len(lines(a.target/'sdd1.csv')),'all_sampled_sdd1_flags_false':bool(samples) and all(not x['sdd1_enabled'] for x in samples),'sdd1_samples':len(samples),'image_comparisons':images,'caveats':['Hash set membership does not establish order or universal visual correctness.','Sparse captures are not a complete frame-by-frame comparison.','No cartridge save/load validation; emulator states are separate.']}
pending=collections.Counter((x.get('dma0_source'),x.get('dma0_length')) for x in samples if x.get('dma0_length') and int(x.get('dma0_source','0'),16)>=0xc00000 and (int(x['dma0_source'],16)>>16,int(x['dma0_source'],16)&65535) not in catalog)
result['persistent_unresolved_dma_sources']=[{'source':k[0],'length':k[1],'samples':v} for k,v in pending.items() if v>=3]
result['dma_checks_passed']=not result['persistent_unresolved_dma_sources'] and not (missing or short or wrong or target_errors or result['handler_trap_samples'] or result['target_remaining_sdd1_transfers']) and result['all_sampled_sdd1_flags_false'] and len(t)>=a.min_redirected and (not unknown or bool(target_checks))
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['image_comparisons','reference_callsites','caveats']},indent=2));print('images',len(images),'identical',sum(x['pixel_identical'] for x in images))
assert not missing and not short and not wrong and not target_errors
assert not unknown or target_checks, 'Unknown output hash requires per-source verification'
assert not result['persistent_unresolved_dma_sources'], 'Persistent unresolved DMA source, possibly masked by NMI'
assert not result['handler_trap_samples'], 'Handler missing-source trap reached'
assert result['all_sampled_sdd1_flags_false'] and not result['target_remaining_sdd1_transfers'] and len(t)>=a.min_redirected
