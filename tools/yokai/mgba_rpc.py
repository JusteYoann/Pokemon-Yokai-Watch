#!/usr/bin/env python3
"""Headless libretro/mGBA harness. Injects a test-only Thumb callback in unused RAM.

Never modifies the ROM. Native calls are fixtures, not a complete adventure playthrough.
"""
import ctypes as C
import os
import struct
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


class Descriptor(C.Structure):
    _fields_ = [('flags',C.c_uint64),('ptr',C.c_void_p),('offset',C.c_size_t),
                ('start',C.c_size_t),('select',C.c_size_t),('disconnect',C.c_size_t),
                ('len',C.c_size_t),('addrspace',C.c_char_p)]


class MemoryMap(C.Structure):
    _fields_ = [('descriptors',C.POINTER(Descriptor)),('num_descriptors',C.c_uint)]


class GameInfo(C.Structure):
    _fields_ = [('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]


class Variable(C.Structure):
    _fields_ = [('key',C.c_char_p),('value',C.c_char_p)]


ENV = C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO = C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO = C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH = C.CFUNCTYPE(C.c_size_t,C.c_void_p,C.c_size_t)
POLL = C.CFUNCTYPE(None)
INPUT = C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)


class Emulator:
    STUB = 0x0203FE00
    PARAMS = 0x0203FF00

    def __init__(self, rom=None, library=None):
        library = library or os.environ.get('MGBA_LIBRETRO_PATH','/workspace/.setup/mgba-build/mgba_libretro.so')
        self.lib = C.CDLL(str(library))
        self.maps, self.pixel_format, self.frame_packet, self.keys = [], 0, None, set()
        self.directories = C.create_string_buffer(str(Path(tempfile.mkdtemp(prefix='yokai-mgba-'))).encode())
        self.variables = {'mgba_use_bios':b'OFF','mgba_skip_bios':b'ON','mgba_frameskip':b'0','mgba_idle_optimization':b'Detect and Remove'}
        self.callbacks = [ENV(self.environment),VIDEO(self.video),AUDIO(lambda l,r:None),
                          BATCH(lambda data,frames:frames),POLL(lambda:None),
                          INPUT(lambda port,device,index,key: int(key in self.keys))]
        for name,callback in zip(['environment','video_refresh','audio_sample','audio_sample_batch','input_poll','input_state'],self.callbacks):
            function=getattr(self.lib,'retro_set_'+name);function.argtypes=[type(callback)];function(callback)
        self.lib.retro_load_game.argtypes=[C.POINTER(GameInfo)];self.lib.retro_load_game.restype=C.c_bool
        self.lib.retro_serialize_size.restype=C.c_size_t
        self.lib.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];self.lib.retro_serialize.restype=C.c_bool
        self.lib.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];self.lib.retro_unserialize.restype=C.c_bool
        self.lib.retro_init()
        path=Path(rom or ROOT/'pokefirered.gba')
        self.rom_buffer=C.create_string_buffer(path.read_bytes())
        info=GameInfo(str(path).encode(),C.cast(self.rom_buffer,C.c_void_p),path.stat().st_size,None)
        assert self.lib.retro_load_game(C.byref(info)), 'mGBA ROM load failed'
        self.symbols={}
        for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only','pokefirered.elf'],cwd=ROOT,text=True).splitlines():
            fields=line.split()
            if len(fields)==3:self.symbols[fields[2]]=int(fields[0],16)
        for name in ['GetMonData','GetBoxMonData']:
            if name not in self.symbols:self.symbols[name]=self.symbols[name+'3']
        self.run(600)
        self.assemble_stub()

    def environment(self, command, data):
        command &= 0xFFFF
        if command in [9,30,31]:
            C.cast(data,C.POINTER(C.c_char_p))[0]=C.cast(self.directories,C.c_char_p)
            return True
        if command == 10:
            self.pixel_format=C.cast(data,C.POINTER(C.c_uint))[0]
            return True
        if command == 15:
            variable=C.cast(data,C.POINTER(Variable)).contents
            value=self.variables.get(variable.key.decode())
            if value is None:return False
            variable.value=value
            return True
        if command == 17:
            C.cast(data,C.POINTER(C.c_bool))[0]=False
            return True
        if command == 36:
            mapping=C.cast(data,C.POINTER(MemoryMap)).contents
            self.maps=[(int(x.start),int(x.len),int(x.ptr or 0)+int(x.offset))
                       for x in mapping.descriptors[:mapping.num_descriptors] if x.ptr and x.len]
            return True
        if command in [6,7,8,11,16,18,32,35,42]:return True
        return False

    def video(self, data, width, height, pitch):
        if not data:return
        raw=C.string_at(data,pitch*height)
        self.frame_packet=(raw,width,height,pitch)

    @property
    def frame(self):
        if self.frame_packet is None:return None
        raw,width,height,pitch=self.frame_packet
        if self.pixel_format == 1:
            image=Image.frombytes('RGB',(width,height),raw,'raw','BGRX',pitch)
        else:
            output=bytearray()
            for y in range(height):
                for value, in struct.iter_unpack('<H',raw[y*pitch:y*pitch+width*2]):
                    if self.pixel_format == 2:
                        output.extend((((value>>11)&31)*255//31,((value>>5)&63)*255//63,(value&31)*255//31))
                    else:output.extend((((value>>10)&31)*255//31,((value>>5)&31)*255//31,(value&31)*255//31))
            image=Image.frombytes('RGB',(width,height),bytes(output))
        return image

    def run(self, frames=1):
        for _ in range(frames):self.lib.retro_run()

    def address(self, address, size):
        for start,length,pointer in self.maps:
            if start<=address and address+size<=start+length:return pointer+address-start
        raise ValueError(f'Unmapped RAM address {address:08x}, maps={self.maps}')

    def read(self, address, size):return C.string_at(self.address(address,size),size)
    def write(self, address, data):C.memmove(self.address(address,len(data)),data,len(data))
    def u32(self,address):return struct.unpack('<I',self.read(address,4))[0]
    def w32(self,address,value):self.write(address,struct.pack('<I',value))

    def assemble_stub(self):
        assembly=f'''.syntax unified
.thumb
.global entry
.thumb_func
entry:
 push {{r4-r7,lr}}
 sub sp, #20
 ldr r4, ={self.PARAMS}
 ldr r0,[r4,#16]
 str r0,[sp,#0]
 ldr r0,[r4,#20]
 str r0,[sp,#4]
 ldr r0,[r4,#24]
 str r0,[sp,#8]
 ldr r0,[r4,#28]
 str r0,[sp,#12]
 ldr r0,[r4,#0]
 ldr r1,[r4,#4]
 ldr r2,[r4,#8]
 ldr r3,[r4,#12]
 ldr r5,[r4,#32]
 adr r6, finished
 adds r6,#1
 mov lr,r6
 bx r5
.align 2
finished:
 ldr r4, ={self.PARAMS}
 str r0,[r4,#36]
 ldr r6, ={self.symbols['gMain']+4}
 ldr r5,[r6]
 ldr r7, ={self.STUB|1}
 cmp r5,r7
 bne keep_callback
 ldr r5,[r4,#40]
 str r5,[r6]
keep_callback:
 movs r5,#1
 str r5,[r4,#44]
 add sp,#20
 pop {{r4-r7,pc}}
.pool
'''
        directory=Path(tempfile.mkdtemp(prefix='yokai-rpc-'))
        (directory/'stub.s').write_text(assembly)
        subprocess.run(['arm-none-eabi-as','-mcpu=arm7tdmi','-mthumb',str(directory/'stub.s'),'-o',str(directory/'stub.o')],check=True)
        subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(directory/'stub.o'),str(directory/'stub.bin')],check=True)
        self.stub=(directory/'stub.bin').read_bytes()
        assert len(self.stub)<256

    def call(self, function, *args, max_frames=600):
        assert len(args)<=8
        address=self.symbols[function] if isinstance(function,str) else function
        callback=self.u32(self.symbols['gMain']+4)
        values=list(args)+[0]*(8-len(args))+[address|1,0,callback,0]
        self.write(self.STUB,self.stub)
        self.write(self.PARAMS,struct.pack('<12I',*values))
        self.w32(self.symbols['gMain']+4,self.STUB|1)
        for _ in range(max_frames):
            self.run()
            if self.u32(self.PARAMS+44):return self.u32(self.PARAMS+36)
        raise RuntimeError(f'Native call did not return: {function}, callback={self.u32(self.symbols["gMain"]+4):08x}')

    def snapshot(self):
        size=self.lib.retro_serialize_size();buffer=C.create_string_buffer(size)
        assert self.lib.retro_serialize(buffer,size)
        return buffer.raw

    def restore(self, snapshot):
        buffer=C.create_string_buffer(snapshot)
        assert self.lib.retro_unserialize(buffer,len(snapshot))

    def close(self):
        self.lib.retro_unload_game();self.lib.retro_deinit()
