from pathlib import Path
import sys,json
runner=Path(__file__).with_name('run_headless.py').read_text();prefix=runner.split('baseframe=0')[0];exec(prefix)
state_path=Path(sys.argv[5]);state_info=json.loads((state_path.parent/'run.json').read_text());assert state_info['rom_sha256']==hashlib.sha256(b).hexdigest()
state_buffer=C.create_string_buffer(state_path.read_bytes());core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool;assert core.retro_unserialize(state_buffer,len(state_buffer)-1)
current=state_info['frames'];history=[]
print(json.dumps({'ready':True,'frame':current}),flush=True)
for line in sys.stdin:
 command=json.loads(line);n=command.get('frames',120);mask=command.get('mask',0);route=[[current,current+n,mask]];frames=current+n
 history.extend(route)
 for frame in range(current,frames):core.retro_run()
 current=frames
 print(json.dumps({'frame':current,'pc':hex(core.retro_so_debug_pc()),'joy':hex(core.retro_so_debug_joy()),'image':str(outdir/f'frame_{current:05d}.png')}),flush=True)
 (outdir/'route.json').write_text(json.dumps(history,indent=2))
