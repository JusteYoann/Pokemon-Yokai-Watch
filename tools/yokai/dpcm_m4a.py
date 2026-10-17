#!/usr/bin/env python3
"""Public, source-independent codec for the native m4a 33-byte/64-sample DPCM.

Input: mono PCM16 WAV at the intended mixer rate. No copyrighted audio included.
Output: WaveData header and native blocks; no engine/music replacement by this tool.
"""
import argparse,json,math,struct,wave
from pathlib import Path
DELTAS=(0,1,4,9,16,25,36,49,-64,-49,-36,-25,-16,-9,-4,-1)
def signed(value):return ((value+128)&255)-128
def encode(samples):
 out=bytearray()
 for start in range(0,len(samples),64):
  block=list(samples[start:start+64]);block.extend([block[-1]]*(64-len(block)))
  current=block[0];out.append(current&255);codes=[]
  for target in block[1:]:
   code=min(range(16),key=lambda k:abs(signed(current+DELTAS[k])-target))
   codes.append(code);current=signed(current+DELTAS[code])
  out.append(codes[0]) # first high nibble is unused by the native decoder
  out.extend((codes[i]<<4)|codes[i+1] for i in range(1,63,2))
 return bytes(out)
def decode(data,count):
 assert len(data)>=((count+63)//64)*33
 out=[]
 for offset in range(0,((count+63)//64)*33,33):
  block=data[offset:offset+33];current=signed(block[0]);out.append(current)
  codes=[block[1]&15]
  for byte in block[2:]:codes.extend([byte>>4,byte&15])
  for code in codes:current=signed(current+DELTAS[code]);out.append(current)
 return out[:count]
def wave_data(samples,rate,loop_start=None):
 assert samples and 1<=rate<=65535
 assert loop_start is None or 0<=loop_start<len(samples)
 return struct.pack('<HHIII',1,0 if loop_start is None else 0x4000,rate*1024,loop_start or 0,len(samples))+encode(samples)
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('input',type=Path);parser.add_argument('output',type=Path);parser.add_argument('--loop-start',type=int)
 args=parser.parse_args()
 with wave.open(str(args.input),'rb') as wav:
  assert wav.getnchannels()==1 and wav.getsampwidth()==2 and wav.getcomptype()=='NONE','Need mono uncompressed PCM16 WAV'
  rate=wav.getframerate();pcm=wav.readframes(wav.getnframes())
 samples=[max(-128,min(127,int(round(x[0]/256)))) for x in struct.iter_unpack('<h',pcm)]
 encoded=wave_data(samples,rate,args.loop_start);args.output.write_bytes(encoded)
 restored=decode(encoded[16:],len(samples));error=sum((a-b)**2 for a,b in zip(samples,restored));power=sum(a*a for a in samples)
 report={'format':'native m4a DPCM, 33 bytes/64 samples +16 header','rate_hz':rate,'samples':len(samples),'duration_seconds':len(samples)/rate,'bytes':len(encoded),'loop_start_samples':args.loop_start,'rms_error_pcm8':math.sqrt(error/len(samples)),'snr_db':10*math.log10(power/error) if power and error else None,'quality_note':'Greedy encoder; numerical error is not listening or natural-loop validation. Private audio output must remain private.'}
 args.output.with_suffix(args.output.suffix+'.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
