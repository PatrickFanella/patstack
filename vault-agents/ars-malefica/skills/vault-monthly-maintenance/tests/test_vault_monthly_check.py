import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "vault_monthly_check.py"
SPEC = importlib.util.spec_from_file_location("vault_monthly_check", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class HierarchyHealthTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_note(self, relative, **metadata):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        frontmatter = "\n".join(f"{key}: {value}" for key, value in metadata.items())
        path.write_text(f"---\n{frontmatter}\n---\nPRIVATE BODY\n")
        return relative

    def write_plain(self, relative):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("PLAIN BODY\n")
        return relative

    def write_frontmatter(self, relative, frontmatter):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}\n---\nPRIVATE BODY\n")
        return relative

    def write_complete_chain(self):
        base = Path("003 Resources/Periodic Notes/2026")
        self.write_note(base / "2026.md", period="yearly", year="2026", created="2026-09-03")
        self.write_note(base / "2026-Q3/2026-Q3.md", period="quarterly", quarter="2026-Q3", created="2026-09-03")
        self.write_note(base / "2026-Q3/2026-09/2026-09.md", period="monthly", month="2026-09", created="2026-09-03")
        self.write_note(
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-W36.md",
            period="weekly",
            week="2026-W36",
            **{
                "week-segment": "2026-09-W36",
                "week-start": "2026-09-01",
                "week-end": "2026-09-06",
                "month": "2026-09",
                "created": "2026-09-03",
            },
        )
        self.write_note(
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-03.md",
            period="daily",
            date="2026-09-03",
            created="2026-09-03",
        )

    def test_reports_only_paths_for_each_hierarchy_defect(self):
        self.write_complete_chain()
        periodic = Path("003 Resources/Periodic Notes")
        misplaced = self.write_note(
            periodic / "2026-10-01.md",
            period="daily",
            date="2026-10-01",
            created="2026-09-03",
        )
        invalid_range = self.write_note(
            periodic / "2026/2026-Q3/2026-09/2026-09-W37/2026-09-W37.md",
            period="weekly",
            week="2026-W37",
            **{
                "week-segment": "2026-09-W37",
                "week-start": "2026-09-01",
                "week-end": "2026-09-30",
                "month": "2026-09",
                "created": "2026-09-03",
            },
        )
        duplicate = self.write_note(
            periodic / "2026/2026-Q3/2026-09/2026-09-W36/duplicate.md",
            period="daily",
            date="2026-09-03",
            created="2026-09-03",
        )
        legacy_relative = periodic / "Daily"
        legacy = self.root / legacy_relative
        legacy.mkdir(parents=True)

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(misplaced.as_posix(), report["misplaced_periodic_notes"])
        self.assertIn(invalid_range.as_posix(), report["invalid_segment_ranges"])
        self.assertEqual(
            report["duplicate_period_keys"],
            sorted(
                [
                    duplicate.as_posix(),
                    "003 Resources/Periodic Notes/2026/2026-Q3/2026-09/2026-09-W36/2026-09-03.md",
                ]
            ),
        )
        self.assertIn(
            "003 Resources/Periodic Notes/2026/2026-Q4/2026-Q4.md",
            report["missing_required_parent_notes"],
        )
        self.assertEqual(report["legacy_type_folders"], [legacy_relative.as_posix()])
        self.assertNotIn("PRIVATE BODY", json.dumps(report))

    def test_complete_hierarchy_has_no_defects(self):
        self.write_complete_chain()

        report = CHECKER.hierarchy_health(self.root)

        self.assertTrue(all(not paths for paths in report.values()))

    def test_reports_periodic_daily_outside_hierarchy(self):
        outside = self.write_note(
            Path("002 Areas/Journal/2026-09-03.md"),
            period="daily",
            date="2026-09-03",
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(outside.as_posix(), report["misplaced_periodic_notes"])

    def test_reports_canonical_daily_missing_period(self):
        daily = self.write_note(
            Path("003 Resources/Periodic Notes/2026/2026-Q3/2026-09/2026-09-W36/2026-09-03.md"),
            date="2026-09-03",
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(daily.as_posix(), report["misplaced_periodic_notes"])

    def test_reports_canonical_daily_with_invalid_period(self):
        daily = self.write_note(
            Path("003 Resources/Periodic Notes/2026/2026-Q3/2026-09/2026-09-W36/2026-09-03.md"),
            period="day",
            date="2026-09-03",
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(daily.as_posix(), report["misplaced_periodic_notes"])

    def test_plain_markdown_does_not_satisfy_parent_identity(self):
        base = Path("003 Resources/Periodic Notes/2026")
        parents = [
            base / "2026.md",
            base / "2026-Q3/2026-Q3.md",
            base / "2026-Q3/2026-09/2026-09.md",
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-W36.md",
        ]
        for parent in parents:
            self.write_plain(parent)
        self.write_note(
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-03.md",
            period="daily",
            date="2026-09-03",
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertEqual(report["missing_required_parent_notes"], sorted(path.as_posix() for path in parents))

    def test_duplicate_period_key_makes_parent_malformed_and_missing(self):
        base = Path("003 Resources/Periodic Notes/2026")
        parent = self.write_frontmatter(
            base / "2026-Q3/2026-09/2026-09.md",
            "period: monthly\nperiod: monthly\nmonth: 2026-09",
        )
        self.write_note(
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-W36.md",
            period="weekly",
            week="2026-W36",
            **{
                "week-segment": "2026-09-W36",
                "week-start": "2026-09-01",
                "week-end": "2026-09-06",
                "month": "2026-09",
            },
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(parent.as_posix(), report["misplaced_periodic_notes"])
        self.assertIn(parent.as_posix(), report["missing_required_parent_notes"])
        self.assertNotIn("PRIVATE BODY", json.dumps(report))

    @unittest.skipUnless(CHECKER.yaml is not None, "nested mappings require PyYAML")
    def test_nested_duplicate_key_makes_parent_malformed_and_missing(self):
        base = Path("003 Resources/Periodic Notes/2026")
        parent = self.write_frontmatter(
            base / "2026-Q3/2026-09/2026-09.md",
            "period: monthly\nmonth: 2026-09\nmetadata:\n  owner: first\n  owner: second",
        )
        self.write_note(
            base / "2026-Q3/2026-09/2026-09-W36/2026-09-W36.md",
            period="weekly",
            week="2026-W36",
            **{
                "week-segment": "2026-09-W36",
                "week-start": "2026-09-01",
                "week-end": "2026-09-06",
                "month": "2026-09",
            },
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(parent.as_posix(), report["misplaced_periodic_notes"])
        self.assertIn(parent.as_posix(), report["missing_required_parent_notes"])

    def test_parentless_august_month_is_not_grandfathered(self):
        monthly = Path("003 Resources/Periodic Notes/2026/2026-Q3/2026-08/2026-08.md")
        self.write_note(monthly, period="monthly", month="2026-08")

        report = CHECKER.hierarchy_health(self.root)

        self.assertEqual(
            report["missing_required_parent_notes"],
            [
                "003 Resources/Periodic Notes/2026/2026-Q3/2026-Q3.md",
                "003 Resources/Periodic Notes/2026/2026.md",
            ],
        )

    def test_parentless_q3_is_not_grandfathered(self):
        quarterly = Path("003 Resources/Periodic Notes/2026/2026-Q3/2026-Q3.md")
        self.write_note(quarterly, period="quarterly", quarter="2026-Q3")

        report = CHECKER.hierarchy_health(self.root)

        self.assertEqual(
            report["missing_required_parent_notes"],
            ["003 Resources/Periodic Notes/2026/2026.md"],
        )

    def test_unquoted_integer_years_preserve_duplicate_identity(self):
        first = self.write_note(
            Path("003 Resources/Periodic Notes/2026/2026.md"),
            period="yearly",
            year=2026,
        )
        second = self.write_note(
            Path("002 Areas/Journal/duplicate-year.md"),
            period="yearly",
            year=2026,
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertEqual(report["duplicate_period_keys"], sorted([first.as_posix(), second.as_posix()]))

    def test_invalid_explicit_identity_key_does_not_fall_back_to_filename(self):
        yearly = self.write_note(
            Path("003 Resources/Periodic Notes/2026/2026.md"),
            period="yearly",
            year="[]",
        )

        report = CHECKER.hierarchy_health(self.root)

        self.assertIn(yearly.as_posix(), report["misplaced_periodic_notes"])


if __name__ == "__main__":
    unittest.main()
