from pathlib import Path
import sys,json,ctypes as C
exec(Path(__file__).with_name('run_headless.py').read_text().split('baseframe=0')[0])
s=Path(sys.argv[5]);i=json.loads((s.parent/'run.json').read_text());assert i['rom_sha256']==hashlib.sha256(b).hexdigest()
buf=C.create_string_buffer(s.read_bytes());core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool;assert core.retro_unserialize(buf,len(buf)-1)
print('pc',hex(core.retro_so_debug_pc()),'remap',hex(core.retro_so_debug_remap() & 0xffffffff))
for ch in range(2):print('channel',ch,'source',hex(core.retro_so_debug_dma_source(ch)),'length',core.retro_so_debug_dma_length(ch))
