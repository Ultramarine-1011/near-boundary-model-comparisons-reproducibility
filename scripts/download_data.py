"""Download published archives; verify SHA-256 before accepting any input.

Uses independently checked ranges to tolerate interrupted large HTTP responses.
Only public requests; no credentials, model calls, or external mutations.
"""
from pathlib import Path
import urllib.request,concurrent.futures,hashlib,json,argparse
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'atlas.zip':('https://raw.githubusercontent.com/Peiyu-Georgia-Li/ATLAS/a42e4d174de821f2f0ac2c1fee454afa4964d030/data/data.zip','4c58404271957478b5c64b1b734e7c0825b1303ddbe5ce2c29c8629798f79e64'),
 'mmlu-pro.zip':('https://raw.githubusercontent.com/skbwu/efficiently-evaluating-llms/857ee18607bd9c84e90431ce0b8f36fc3f72ae68/data/processed/mmlu-pro.zip','8e4e34cfb86659d3acae896aba56d01fc51ed5f8751077c33dd74b969054a874'),
 'composite.zip':('https://raw.githubusercontent.com/skbwu/efficiently-evaluating-llms/857ee18607bd9c84e90431ce0b8f36fc3f72ae68/data/processed/bbh%2Bgpqa%2Bifeval%2Bmath%2Bmusr.zip','550498f5e894e31a8acfd54becbc880f5ef4c58435ef205c60c472db1d4e871d')}
def download(name,url,digest):
 dest=ROOT/'data'/'raw'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():
  if hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:raise ValueError('Existing input hash mismatch: '+name)
  return {'file':name,'url':url,'sha256':digest,'bytes':dest.stat().st_size}
 with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=45) as r:size=int(r.headers['Content-Length'])
 cache=ROOT/'.cache'/'downloads';cache.mkdir(parents=True,exist_ok=True)
 def part(start):
  end=min(size-1,start+256*1024-1);p=cache/f'{name}.{start}'
  if p.exists() and p.stat().st_size==end-start+1:return p.read_bytes()
  for attempt in range(5):
   try:
    req=urllib.request.Request(url+f'?range={start}',headers={'Range':f'bytes={start}-{end}'})
    with urllib.request.urlopen(req,timeout=45) as r:
     if r.status!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/{size}':raise ValueError('Unverified HTTP range')
     b=r.read()
    if len(b)!=end-start+1:raise ValueError('Partial range')
    p.write_bytes(b);return b
   except Exception:
    if attempt==4:raise
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:raw=b''.join(pool.map(part,range(0,size,256*1024)))
 if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Downloaded hash mismatch: '+name)
 dest.write_bytes(raw)
 return {'file':name,'url':url,'sha256':digest,'bytes':len(raw)}
if __name__=='__main__':
 manifest=[]
 for name,(url,digest) in SOURCES.items():
  entry=download(name,url,digest);manifest.append(entry);print(name,'verified',flush=True)
 (ROOT/'data'/'raw'/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
