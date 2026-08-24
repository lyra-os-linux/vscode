from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VscodeRepoPackagingTests(unittest.TestCase):
    def test_repo_file_points_at_microsofts_official_repository(self) -> None:
        repo = (ROOT / "vscode.repo").read_text(encoding="utf-8")
        self.assertIn(
            "baseurl=https://packages.microsoft.com/yumrepos/vscode", repo
        )
        self.assertIn("gpgcheck=1", repo)
        self.assertIn("repo_gpgcheck=1", repo)
        self.assertIn(
            "gpgkey=file:///usr/share/distribution-gpg-keys/microsoft/microsoft.gpg",
            repo,
        )

    def test_package_ships_no_upstream_binary(self) -> None:
        spec = (ROOT / "vscode-repo.spec").read_text(encoding="utf-8")
        self.assertNotIn("_service", [p.name for p in ROOT.iterdir()])
        self.assertIn("Requires:       distribution-gpg-keys", spec)


if __name__ == "__main__":
    unittest.main()
