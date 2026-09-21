import importlib.machinery, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
loader=importlib.machinery.SourceFileLoader('profile_manager',str(ROOT/'scripts/skill-profile'))
spec=importlib.util.spec_from_loader(loader.name,loader);manager=importlib.util.module_from_spec(spec);loader.exec_module(manager)

class ProfileTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);root=Path(self.temp.name)
  for key,value in {'ROOT':root,'ACTIVE':root/'skills','LIBRARY':root/'library','PROFILES':root/'profiles','STATE':root/'state.json','SOURCE':root/'source','LOCK':root/'lock'}.items():setattr(manager,key,value)
  for p in [manager.ACTIVE,manager.LIBRARY,manager.PROFILES,manager.SOURCE/'shared',manager.SOURCE/'catalog']:p.mkdir(parents=True,exist_ok=True)
  for name in ['base','optional','curated','retired','interview']:
   p=manager.LIBRARY/name;p.mkdir();(p/'SKILL.md').write_text(name)
  p=manager.SOURCE/'shared/interview';p.mkdir();(p/'SKILL.md').write_text('current interview')
  (manager.SOURCE/'catalog/proposed-catalog.json').write_text(json.dumps([{'name':'curated'}]))
  (manager.SOURCE/'catalog/retired-names.json').write_text(json.dumps({'retired':{}}))
  (manager.PROFILES/'core.txt').write_text('base\ninterview\n');(manager.PROFILES/'extra.txt').write_text('optional\ncurated\nretired\n')
 def test_switch_filters_duplicates_preserves_owner_and_deactivates(self):
  manager.activate([]);before=manager.folder_digest(manager.ACTIVE)
  plan=manager.preview(['extra']);self.assertEqual(plan['skills'],['base','interview','optional']);self.assertEqual(manager.folder_digest(manager.ACTIVE),before)
  manager.activate(['extra']);self.assertEqual(set(manager.skill_dirs(manager.ACTIVE)),{'base','interview','optional'})
  self.assertEqual((manager.ACTIVE/'interview/SKILL.md').read_text(),'current interview')
  manager.activate([]);self.assertFalse((manager.ACTIVE/'optional').exists())
 def test_dirty_active_is_preserved(self):
  manager.activate([]);p=manager.ACTIVE/'base/SKILL.md';p.write_text('user edit')
  with self.assertRaisesRegex(SystemExit,'refusing'):manager.activate(['extra'])
  self.assertEqual(p.read_text(),'user edit')
 def test_curated_promotion_is_refused(self):
  manager.activate([])
  with self.assertRaisesRegex(SystemExit,'curated'):manager.promote('interview',['core'])
 def test_all_still_filters_and_mode_drift_blocks(self):
  manager.activate([],True);self.assertNotIn('retired',manager.skill_dirs(manager.ACTIVE));self.assertNotIn('curated',manager.skill_dirs(manager.ACTIVE))
  p=manager.ACTIVE/'base/SKILL.md';p.chmod(0o700)
  with self.assertRaises(SystemExit):manager.activate([])
