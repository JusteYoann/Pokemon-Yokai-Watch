#!/usr/bin/env python3
"""Extract supplied music archives to a private directory, safely, using libarchive.

No resources are downloaded. Do not publish the extracted recordings or samples.
"""
import argparse,ctypes as C,ctypes.util,hashlib,json
from pathlib import Path,PurePosixPath

def extract(archives,destination):
 lib=C.CDLL(ctypes.util.find_library('archive'))
 signatures=[('archive_read_new',[],C.c_void_p),('archive_read_support_filter_all',[C.c_void_p],C.c_int),('archive_read_support_format_all',[C.c_void_p],C.c_int),('archive_read_open_filename',[C.c_void_p,C.c_char_p,C.c_size_t],C.c_int),('archive_read_next_header',[C.c_void_p,C.POINTER(C.c_void_p)],C.c_int),('archive_entry_pathname_utf8',[C.c_void_p],C.c_char_p),('archive_entry_filetype',[C.c_void_p],C.c_uint),('archive_read_data',[C.c_void_p,C.c_void_p,C.c_size_t],C.c_longlong),('archive_read_free',[C.c_void_p],C.c_int),('archive_error_string',[C.c_void_p],C.c_char_p)]
 for name,args,result in signatures:f=getattr(lib,name);f.argtypes=args;f.restype=result
 rows=[];destination=destination.resolve();assert not destination.is_relative_to(Path(__file__).resolve().parents[2]), 'Extract protected references outside checkout';destination.mkdir(parents=True,exist_ok=True)
 for archive in archives:
  handle=lib.archive_read_new();lib.archive_read_support_filter_all(handle);lib.archive_read_support_format_all(handle)
  try:
   if lib.archive_read_open_filename(handle,str(archive).encode(),65536)!=0:raise RuntimeError(lib.archive_error_string(handle))
   entry=C.c_void_p()
   while True:
    status=lib.archive_read_next_header(handle,C.byref(entry))
    if status==1:break
    if status<0:raise RuntimeError(lib.archive_error_string(handle))
    member=lib.archive_entry_pathname_utf8(entry).decode();relative=PurePosixPath(member.replace('\\','/'))
    if lib.archive_entry_filetype(entry)!=0o100000 or relative.suffix.lower() not in {'.mp3','.wav','.ogg','.flac'}:continue
    assert not relative.is_absolute() and '..' not in relative.parts,member
    output=destination/archive.stem/Path(*relative.parts);assert output.resolve().is_relative_to(destination)
    output.parent.mkdir(parents=True,exist_ok=True);digest=hashlib.sha256();buffer=C.create_string_buffer(65536)
    with output.open('wb') as stream:
     while True:
      count=lib.archive_read_data(handle,buffer,len(buffer))
      if count==0:break
      if count<0:raise RuntimeError(lib.archive_error_string(handle))
      block=buffer.raw[:count];stream.write(block);digest.update(block)
    rows.append({'archive':archive.name,'member':member,'private_path':str(output),'bytes':output.stat().st_size,'sha256':digest.hexdigest()})
  finally:lib.archive_read_free(handle)
 return rows
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('archives',type=Path,nargs='+');args=parser.parse_args()
 rows=extract(args.archives,args.output);(args.output/'manifest-private.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'files_extracted':len(rows),'private_directory':str(args.output)}))
