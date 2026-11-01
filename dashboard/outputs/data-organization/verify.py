"""End-to-end evidence for the single data directory, without external network."""
import gzip, hashlib, json, socket, subprocess, time, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/data-organization'
MOVES={'data/pitchapi_bundles':'data/raw/pitchapi/bundles','data/open_matchday_2026_2027':'data/raw/open_matchday/2026-2027','dashboard/data':'data/dashboard'}
e={'setup':'Node.js and Python 3; repository snapshot and before.json/dashboard-before.json from before relocation; no API key or network provider needed.', 'rerun_command':'python3 outputs/data-organization/verify.py','expected':'All original file bytes preserved; one data directory; real HTTP serves manifest, both historical seasons, frontend; raw directory not public.','status':'failed'}
child=None
try:
 rows=json.loads((OUT/'before.json').read_text())+json.loads((OUT/'dashboard-before.json').read_text())
 for row in rows:
  old=row['path']; new=old
  for prefix,dest in MOVES.items():
   if old==prefix or old.startswith(prefix+'/'):new=dest+old[len(prefix):];break
  b=(ROOT/new).read_bytes()
  assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],new
 assert not (ROOT/'dashboard/data').exists()
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 log=(OUT/'server.log').open('w')
 child=subprocess.Popen(['node','dashboard/server.js','--port',str(port)],cwd=ROOT,stdout=log,stderr=log)
 def get(path):return urllib.request.urlopen(f'http://127.0.0.1:{port}'+path,timeout=15).read()
 for _ in range(100):
  try:get('/');break
  except OSError:time.sleep(.05)
 else:raise RuntimeError('server failed to start')
 manifest=json.loads(get('/data/football-manifest.json')); results=[]
 for label in ('2024/2025','2025/2026'):
  season=next(s for s in manifest['seasons'] if s['id']==label)
  chunk=season['chunks'][0]; b=get('/data/'+chunk['path'])
  assert hashlib.sha256(b).hexdigest()==chunk['sha256']
  d=json.loads(gzip.decompress(b));assert d['matches'] and d['appearances']
  results.append({'season':label,'chunks':len(season['chunks']),'matches_in_sample':len(d['matches']),'appearances_in_sample':len(d['appearances']),'sha256':chunk['sha256']})
 assert b'football-manifest.json' in get('/app.js')
 assert get('/data/open_matchday.json')==(ROOT/'data/dashboard/open_matchday.json').read_bytes()
 try:get('/data/raw/pitchapi/bundles/europe_2021_2026/manifest.json');raise AssertionError('raw files exposed')
 except urllib.error.HTTPError as exc:assert exc.code==404
 e.update(status='passed',verified_preserved_files=len(rows),actual={'seasons':results,'single_data_directory':True,'raw_directory_not_public':True},logs=['server.log','tests.log','build.log','baseline.log','relocation-first-run.log','relocation-fixture-run.log'])
except Exception as exc:
 e['error']=repr(exc);raise
finally:
 if child:child.terminate();child.wait(timeout=10)
 (OUT/'evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps(e,indent=2))
