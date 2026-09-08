import importlib.util,json,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('transaction_installer',ROOT/'scripts/install.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
class PrepareTests(unittest.TestCase):
 def test_plan_batches_idempotency_and_drift(self):
  with tempfile.TemporaryDirectory() as directory:
   root=pathlib.Path(directory);state=root/'state';personal=root/'installed';shared=root/'shared-installed';blacktower=root/'blacktower';exclude=blacktower/'.git/info/exclude'
   for p in [root/'catalog',root/'skills/frontend-design',root/'skills/ordinary',root/'shared/session-handoff',root/'repository-skills/blacktower-development',personal/'retired',personal/'ordinary',exclude.parent]:p.mkdir(parents=True,exist_ok=True)
   for p in [root/'skills/frontend-design',root/'skills/ordinary',root/'shared/session-handoff',root/'repository-skills/blacktower-development']:(p/'SKILL.md').write_text('candidate')
   (personal/'ordinary/SKILL.md').write_text('original');(personal/'retired/SKILL.md').write_text('old');exclude.write_text('# existing exclusion\nkeep-me\n')
   config={'personalRoot':str(personal),'sharedRoot':str(shared),'blacktowerRoot':str(blacktower),'excludePath':str(exclude)}
   baseline={str(p):installer.snapshot(p) for p in [personal/'ordinary',personal/'retired',exclude]}
   installer.save(root/'catalog/installation.json',config);installer.save(root/'catalog/baseline.json',baseline);installer.save(root/'catalog/proposed-catalog.json',[{'name':n,'scope':'personal'} for n in ['ordinary','frontend-design']])
   subprocess.run(['git','init','-q',str(root)],check=True)
   subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','--allow-empty','-qm','fixture'],check=True)
   first=installer.prepare(root,state);self.assertFalse(state.exists());self.assertEqual(first,installer.prepare(root,state))
   run=installer.apply(first,state,through=1);self.assertEqual(installer.read(run/'journal.json')['status'],'partial');self.assertEqual((personal/'ordinary/SKILL.md').read_text(),'original')
   installer.apply(None,state,resume=run,through=3);installer.verify(installer.prepare(root,state),state)
   self.assertTrue(all(op['action']=='unchanged' for op in installer.prepare(root,state)['operations']))
   self.assertIn('keep-me\n',exclude.read_text());self.assertEqual(exclude.read_text().count('/.agents/skills/blacktower-development/'),1)
   (personal/'ordinary/SKILL.md').write_text('intervening edit')
   with self.assertRaisesRegex(RuntimeError,'Drift'):installer.prepare(root,state)
   with self.assertRaisesRegex(RuntimeError,'intervening edits'):installer.rollback(run,state)
   self.assertEqual((personal/'ordinary/SKILL.md').read_text(),'intervening edit')
