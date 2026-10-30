from pathlib import Path
import ctypes as C,sys,os,json,hashlib
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent
rompath=Path(sys.argv[1]).resolve();label=sys.argv[2] if len(sys.argv)>2 else 'run';frames=int(sys.argv[3]) if len(sys.argv)>3 else 2400
outdir=root/'runs'/label;outdir.mkdir(parents=True,exist_ok=True)
route=json.loads(Path(sys.argv[4]).read_text()) if len(sys.argv)>4 else []
os.environ['SO_SDD1_TRACE']=str(outdir/'sdd1.csv')
os.environ['SO_PLAIN_TRACE']=str(outdir/'plain_dma.csv')
core=C.CDLL(str(root/'snes9x/libretro/snes9x_libretro.so'))
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p);VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t);AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16);BATCH=C.CFUNCTYPE(C.c_size_t,C.c_void_p,C.c_size_t);POLL=C.CFUNCTYPE(None);INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
extra_captures={int(x) for x in os.environ.get('SO_CAPTURE_FRAMES','').split(',') if x}
frame=0;pixel=0;directories=C.c_char_p(str(outdir).encode());captures=[]
@ENV
def env(cmd,data):
 global pixel
 if cmd==10:pixel=C.cast(data,C.POINTER(C.c_int))[0];return True
 if cmd in (9,30,31):C.cast(data,C.POINTER(C.c_char_p))[0]=directories;return True
 if cmd in (3,51):C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
 if cmd==2:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 return False
@VIDEO
def video(data,w,h,pitch):
 if not data or (frame not in extra_captures and frame not in [0,119,299,599,1199,2399,4799,7199,11999,17999,frames-1] and not (route and frame>=24000 and frame%600==599)):return
 if pixel==1:
  arr=np.frombuffer(C.string_at(data,pitch*h),dtype=np.uint32).reshape(h,pitch//4)[:,:w];rgb=np.stack(((arr>>16)&255,(arr>>8)&255,arr&255),-1).astype('uint8')
 else:
  arr=np.frombuffer(C.string_at(data,pitch*h),dtype=np.uint16).reshape(h,pitch//2)[:,:w]
  rgb=np.stack((((arr>>11)&31)*255//31,((arr>>5)&63)*255//63,(arr&31)*255//31),-1).astype('uint8') if pixel==2 else np.stack((((arr>>10)&31)*255//31,((arr>>5)&31)*255//31,(arr&31)*255//31),-1).astype('uint8')
 Image.fromarray(rgb).resize((w*2,h*2)).save(outdir/f'frame_{frame+1:05d}.png');captures.append(frame+1)
@AUDIO
def audio(a,b):pass
@BATCH
def batch(data,n):return n
@POLL
def poll():pass
@INPUT
def inp(port,device,index,id):
 if port:return 0
 buttons=0
 if 240<=frame<245 or 600<=frame<605:buttons|=1<<3
 if frame>800 and frame%180<5:buttons|=1<<8
 if frame>=24000 and route:
  buttons=0
  for start,end,mask in route:
   if start<=frame<end:buttons|=mask
 return buttons if id==256 else int(bool(buttons&(1<<id)))
for name,cb in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',inp)]:getattr(core,'retro_set_'+name)(cb)
core.retro_init()
class Info(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
b=rompath.read_bytes();buf=C.create_string_buffer(b);info=Info(str(rompath).encode(),C.cast(buf,C.c_void_p),len(b),None);core.retro_load_game.argtypes=[C.POINTER(Info)];core.retro_load_game.restype=C.c_bool
if not core.retro_load_game(C.byref(info)):raise RuntimeError('ROM load failed')
baseframe=0
if len(sys.argv)>5:
 state_path=Path(sys.argv[5]);state_info=json.loads((state_path.parent/'run.json').read_text());assert state_info['rom_sha256']==hashlib.sha256(b).hexdigest(),'State belongs to another ROM'
 state_buffer=C.create_string_buffer(state_path.read_bytes());core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool;assert core.retro_unserialize(state_buffer,len(state_buffer)-1)
 baseframe=state_info['frames']
pcs=[]
for frame in range(baseframe,frames):
 core.retro_run()
 if frame in extra_captures or frame%600==599 or frame==frames-1:pcs.append({'frame':frame+1,'pc':hex(core.retro_so_debug_pc()),'sdd1_enabled':bool(core.retro_so_debug_sdd1()),'joy_register':hex(core.retro_so_debug_joy()),'input_mask':hex(inp(0,1,0,256)),'dma0_source':hex(core.retro_so_debug_dma_source(0)),'dma0_length':core.retro_so_debug_dma_length(0)})
(outdir/'cpu_samples.json').write_text(json.dumps(pcs,indent=2))
core.retro_serialize_size.restype=C.c_size_t
state_size=core.retro_serialize_size();state_buffer=C.create_string_buffer(state_size);core.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_serialize.restype=C.c_bool
assert core.retro_serialize(state_buffer,state_size);(outdir/'end.state').write_bytes(state_buffer.raw)
core.retro_unload_game();core.retro_deinit()
(outdir/'run.json').write_text(json.dumps({'rom':rompath.name,'rom_sha256':hashlib.sha256(b).hexdigest(),'frames':frames,'start_frame':baseframe,'captures':captures,'pixel_format':pixel},indent=2));print('completed',frames,'frames',captures)
