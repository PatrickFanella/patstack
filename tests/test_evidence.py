import json,pathlib,subprocess,sys,tempfile,unittest
SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'skills/verify-implementation/references/modes/ship-check/scripts/collect_repository_evidence.py'
class EvidenceTests(unittest.TestCase):
 def test_target_root_and_nested_rejection(self):
  with tempfile.TemporaryDirectory() as directory:
   root=pathlib.Path(directory);subprocess.run(['git','init','-q',str(root)],check=True)
   (root/'README.md').write_text('fixture');nested=root/'nested';nested.mkdir()
   run=subprocess.run([sys.executable,str(SCRIPT),str(root)],capture_output=True,text=True,check=True)
   data=json.loads(run.stdout);self.assertEqual(data['repository'],str(root));self.assertEqual(data['head'],'(unborn)');self.assertEqual(data['visible_file_count'],1)
   run=subprocess.run([sys.executable,str(SCRIPT),str(nested)],capture_output=True,text=True)
   self.assertNotEqual(run.returncode,0);self.assertIn('resolves to parent',run.stderr)
 def test_missing_target(self):
  with tempfile.TemporaryDirectory() as directory:
   run=subprocess.run([sys.executable,str(SCRIPT),directory+'/missing'],capture_output=True,text=True)
   self.assertNotEqual(run.returncode,0)
