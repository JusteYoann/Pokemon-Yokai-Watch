import ctypes as c,ctypes.util,json,pathlib
L=c.CDLL(ctypes.util.find_library('archive'))
for name,args,result in [('archive_read_new',[],c.c_void_p),('archive_read_support_filter_all',[c.c_void_p],c.c_int),('archive_read_support_format_all',[c.c_void_p],c.c_int),('archive_read_open_filename',[c.c_void_p,c.c_char_p,c.c_size_t],c.c_int),('archive_read_next_header',[c.c_void_p,c.POINTER(c.c_void_p)],c.c_int),('archive_entry_pathname_utf8',[c.c_void_p],c.c_char_p),('archive_entry_size',[c.c_void_p],c.c_longlong),('archive_entry_filetype',[c.c_void_p],c.c_uint),('archive_read_data',[c.c_void_p,c.c_void_p,c.c_size_t],c.c_longlong),('archive_read_free',[c.c_void_p],c.c_int),('archive_error_string',[c.c_void_p],c.c_char_p)]:
 f=getattr(L,name);f.argtypes=args;f.restype=result
root=pathlib.Path('/workspace/scratch/music-analysis');rows=[]
for game,file in [('YW1','/workspace/attachments/6e44f538-77ac-4ea7-85b9-90884c7bca73/yokaiwatch_1.rar'),('BUSTERS2','/workspace/attachments/477eb8a6-7466-4a0e-895c-6ef5329815f3/yokai watch_busters_2.rar'),('BLASTERS','/workspace/attachments/1ef9875b-a06d-4ab6-9d2e-fa7de405f7be/yokaiwatch_blasters_part2.rar'),('SANGOKUSHI','/workspace/attachments/5db4bd36-00f2-4660-9ca6-d3f3291ea953/yokai_watchsangokushi_part2.rar'),('YW2','/workspace/attachments/1f8c9d41-5225-4221-b36d-4a79d65a9f8f/yokaiwatch_2.rar'),('YW2','/workspace/attachments/a6b79056-71b6-4143-ae1f-96cd98336779/yokaiwatch_2_part2.rar'),('YW2','/workspace/attachments/0afbf776-2cf1-4c50-bbb7-1f390b8b2b3c/yokaiwatch_2_part3.rar'),('YW4','/workspace/attachments/506d8226-7d14-40d9-a4da-eaa0cce85ef6/yokaiwatch_4.rar'),('YW4','/workspace/attachments/e12ca22d-6ab5-423e-9cec-1a4e75f087ce/yokaiwatch4_part2.rar'),('YW3','/workspace/attachments/80d52ec6-e5ce-40b2-a012-f3a6f21605ed/yokaiwatch_3.rar'),('YW3','/workspace/attachments/05cedfa5-7216-47cf-876b-a7391856bbb4/yokaiwatch3part2.rar'),('YW3','/workspace/attachments/f9c157a9-62a7-443f-8528-75fc4d4ae608/yokaiwatch3part3.rar'),('BLASTERS','/workspace/attachments/34beb70d-2a86-48bc-b4ab-765ba6d0d781/yokaiwatch_blasters.rar'),('SANGOKUSHI','/workspace/attachments/9d1eda8c-bbe9-458d-9bae-ce2e73926cb9/Yokaiwatch_sangokushi.rar')]:
 a=L.archive_read_new();L.archive_read_support_filter_all(a);L.archive_read_support_format_all(a);assert L.archive_read_open_filename(a,file.encode(),10240)==0
 e=c.c_void_p()
 while True:
  code=L.archive_read_next_header(a,c.byref(e))
  if code==1:break
  if code<0:raise RuntimeError((code,L.archive_error_string(a)))
  name=L.archive_entry_pathname_utf8(e).decode();dest=(root/'extracted'/game/name).resolve();assert dest.is_relative_to(root/'extracted'/game)
  if L.archive_entry_filetype(e)!=0o100000:continue
  dest.parent.mkdir(parents=True,exist_ok=True);buf=c.create_string_buffer(65536);size=0
  with dest.open('wb') as out:
   while True:
    n=L.archive_read_data(a,buf,len(buf))
    if n==0:break
    if n<0:raise RuntimeError(L.archive_error_string(a))
    out.write(buf.raw[:n]);size+=n
  rows.append({'game':game,'archive':pathlib.Path(file).name,'member':name,'size':size,'local_path':str(dest)})
 L.archive_read_free(a)
(root/'archive-members.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('Extracted',len(rows));print('\n'.join(x['game']+' '+x['member'] for x in rows))
