import csv,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/frontend-design'
class FrontendTests(unittest.TestCase):
 def run_search(self,root,*args):
  return subprocess.run([sys.executable,str(root/'scripts/tool-ui-ux-pro-max/search.py'),*args,'--json'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 def test_pinned_resources(self):
  manifest=json.loads((SKILL/'scripts/data/provenance.json').read_text())
  self.assertEqual(len(manifest['files']),16)
  for path,entry in manifest['files'].items():
   raw=(SKILL/'scripts/data'/path).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),entry['sha256'])
   self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),entry['gitBlob'])
   self.assertGreater(len(list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))),0)
  self.assertEqual(hashlib.sha256((SKILL/'notices/ui-ux-pro-max-MIT.txt').read_bytes()).hexdigest(),manifest['licenseSha256'])
 def test_each_domain_and_stack(self):
  for category,names in [('domain',['style','prompt','color','chart','landing','product','ux','typography']),('stack',['html-tailwind','react','nextjs','vue','svelte','swiftui','react-native','flutter'])]:
   for name in names:
    with self.subTest(name=name):
     result=self.run_search(SKILL,'responsive accessible dashboard','--'+category,name)
     self.assertEqual(result.returncode,0,result.stderr);payload=json.loads(result.stdout);self.assertNotIn('error',payload);self.assertIsInstance(payload['results'],list)
 def test_real_palette_result(self):
  result=self.run_search(SKILL,'saas dashboard','--domain','color');self.assertEqual(result.returncode,0);self.assertTrue(json.loads(result.stdout)['results'])
 def test_missing_data_and_invalid_mode(self):
  with tempfile.TemporaryDirectory() as directory:
   copy=pathlib.Path(directory);shutil.copytree(SKILL/'scripts/tool-ui-ux-pro-max',copy/'scripts/tool-ui-ux-pro-max')
   result=self.run_search(copy,'palette','--domain','color');self.assertNotEqual(result.returncode,0);self.assertIn('error',json.loads(result.stdout))
  result=self.run_search(SKILL,'palette','--domain','not-a-domain');self.assertNotEqual(result.returncode,0)
