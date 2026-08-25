from __future__ import annotations

import configparser
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VscodeRepoPackagingTests(unittest.TestCase):
    def test_repo_file_points_at_microsofts_official_repository(self) -> None:
        parser = configparser.ConfigParser(interpolation=None)
        parser.read(ROOT / "vscode.repo", encoding="utf-8")
        self.assertEqual(parser.sections(), ["code"])
        repo = parser["code"]
        self.assertEqual(repo["baseurl"], "https://packages.microsoft.com/yumrepos/vscode")
        self.assertEqual(repo["gpgcheck"], "1")
        self.assertEqual(repo["repo_gpgcheck"], "1")
        self.assertEqual(
            repo["gpgkey"],
            "file:///usr/share/distribution-gpg-keys/microsoft/microsoft.gpg",
        )
        self.assertEqual(repo["priority"], "90")

    def test_package_ships_no_upstream_binary(self) -> None:
        spec = (ROOT / "vscode-repo.spec").read_text(encoding="utf-8")
        self.assertNotIn("_service", [p.name for p in ROOT.iterdir()])
        self.assertIn("Requires:       distribution-gpg-keys", spec)
        self.assertIn("%config(noreplace)", spec)

    def test_repo_file_install_and_removal_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "etc/zypp/repos.d/vscode.repo"

            def install() -> None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / "vscode.repo", destination)
                destination.chmod(0o644)

            def remove() -> None:
                destination.unlink(missing_ok=True)

            install()
            first = destination.read_bytes()
            install()
            self.assertEqual(destination.read_bytes(), first)
            self.assertEqual(destination.stat().st_mode & 0o777, 0o644)
            remove()
            remove()
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
