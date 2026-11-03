import importlib.util,json,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('transaction_installer',ROOT/'scripts/install.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
class PrepareTests(unittest.TestCase):
 def test_scoped_removal_uses_installed_state_and_preserves_drift(self):
  with tempfile.TemporaryDirectory() as directory:
   root=pathlib.Path(directory);state=root/'state';personal=root/'installed';exclude=root/'blacktower/.git/info/exclude'
   for p in [root/'catalog',root/'skills',root/'shared',personal/'specialist',exclude.parent]:p.mkdir(parents=True,exist_ok=True)
   target=personal/'specialist';(target/'SKILL.md').write_text('curated procedure')
   before=installer.snapshot(target)
   installer.save(root/'catalog/installation.json',{'personalRoot':str(personal),'sharedRoot':str(root/'shared-installed'),'blacktowerRoot':str(root/'blacktower'),'excludePath':str(exclude)})
   installer.save(root/'catalog/baseline.json',{})
   installer.save(root/'catalog/proposed-catalog.json',[{'name':'specialist','scope':'optional'}])
   installer.save(installer.statefile(state),{'paths':{str(target):before}})
   subprocess.run(['git','init','-q',str(root)],check=True)
   subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','--allow-empty','-qm','fixture'],check=True)
   plan=installer.prepare(root,state,only_skills=['specialist'])
   self.assertEqual([(op['destination'],op['action']) for op in plan['operations']],[(str(target),'retire')])
   run=installer.apply(plan,state);self.assertFalse(target.exists());installer.verify(installer.prepare(root,state,only_skills=['specialist']),state)
   installer.rollback(run,state);self.assertEqual(installer.snapshot(target),before)
   (target/'SKILL.md').write_text('user edit')
   with self.assertRaisesRegex(RuntimeError,'Drift'):installer.prepare(root,state,only_skills=['specialist'])
   self.assertEqual((target/'SKILL.md').read_text(),'user edit')
 def test_plan_batches_idempotency_and_drift(self):
  with tempfile.TemporaryDirectory() as directory:
   root=pathlib.Path(directory);state=root/'state';personal=root/'installed';shared=root/'shared-installed';blacktower=root/'blacktower';exclude=blacktower/'.git/info/exclude'
   for p in [root/'catalog',root/'skills/ui-craft',root/'skills/ordinary',root/'shared/relay-baton',root/'repository-skills/blacktower-development',personal/'retired',personal/'ordinary',exclude.parent]:p.mkdir(parents=True,exist_ok=True)
   for p in [root/'skills/ui-craft',root/'skills/ordinary',root/'shared/relay-baton',root/'repository-skills/blacktower-development']:(p/'SKILL.md').write_text('candidate')
   (personal/'ordinary/SKILL.md').write_text('original');(personal/'retired/SKILL.md').write_text('old');exclude.write_text('# existing exclusion\nkeep-me\n')
   config={'personalRoot':str(personal),'sharedRoot':str(shared),'blacktowerRoot':str(blacktower),'excludePath':str(exclude)}
   baseline={str(p):installer.snapshot(p) for p in [personal/'ordinary',personal/'retired',exclude]}
   installer.save(root/'catalog/installation.json',config);installer.save(root/'catalog/baseline.json',baseline);installer.save(root/'catalog/proposed-catalog.json',[{'name':n,'scope':'personal'} for n in ['ordinary','ui-craft']])
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

   scoped=installer.prepare(root,state,only_skills=['ui-craft'])
   self.assertEqual([op['destination'] for op in scoped['operations']],[str(personal/'ui-craft')])
   installer.apply(scoped,state)
   self.assertEqual((personal/'ordinary/SKILL.md').read_text(),'intervening edit')
   with self.assertRaisesRegex(RuntimeError,'Drift'):installer.prepare(root,state,only_skills=['ordinary'])
   with self.assertRaisesRegex(RuntimeError,'Unknown personal skills'):installer.prepare(root,state,only_skills=['missing'])

   shared_scope=installer.prepare(root,state,only_shared=['relay-baton'])
   self.assertEqual([op['destination'] for op in shared_scope['operations']],[str(shared/'relay-baton')])
   installer.apply(shared_scope,state)
   shared_target=shared/'relay-baton/SKILL.md'
   self.assertEqual(shared_target.read_text(),'candidate')
   shared_target.write_text('shared user edit')
   with self.assertRaisesRegex(RuntimeError,'Drift'):installer.prepare(root,state,only_shared=['relay-baton'])
   with self.assertRaisesRegex(RuntimeError,'Unknown shared skills'):installer.prepare(root,state,only_shared=['missing'])
   (personal/'ordinary/SKILL.md').write_text('another user edit')
   selected=installer.prepare(root,state,only_skills=['ui-craft'])
   self.assertEqual(len(selected['operations']),1)
   self.assertEqual(shared_target.read_text(),'shared user edit')
 def test_renamed_shared_skill_retires_only_installer_placed_copy(self):
  with tempfile.TemporaryDirectory() as directory:
   root=pathlib.Path(directory);state=root/'state';personal=root/'installed';shared=root/'shared-installed';exclude=root/'blacktower/.git/info/exclude'
   for p in [root/'catalog',root/'skills',root/'shared/new-baton',shared/'old-baton',shared/'foreign-retired',personal,exclude.parent]:p.mkdir(parents=True,exist_ok=True)
   (root/'shared/new-baton/SKILL.md').write_text('renamed');(shared/'old-baton/SKILL.md').write_text('placed');(shared/'foreign-retired/SKILL.md').write_text('another owner')
   installer.save(root/'catalog/installation.json',{'personalRoot':str(personal),'sharedRoot':str(shared),'blacktowerRoot':str(root/'blacktower'),'excludePath':str(exclude)})
   installer.save(root/'catalog/baseline.json',{});installer.save(root/'catalog/proposed-catalog.json',[])
   installer.save(root/'catalog/retired-names.json',{'old-baton':{'owner':'new-baton'},'foreign-retired':{'owner':None}})
   installer.save(installer.statefile(state),{'paths':{str(shared/'old-baton'):installer.snapshot(shared/'old-baton')}})
   subprocess.run(['git','init','-q',str(root)],check=True)
   subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','--allow-empty','-qm','fixture'],check=True)
   actions={op['destination']:op['action'] for op in installer.prepare(root,state)['operations']}
   self.assertEqual(actions[str(shared/'old-baton')],'retire')
   self.assertEqual(actions[str(shared/'new-baton')],'install')
   self.assertNotIn(str(shared/'foreign-retired'),actions)
