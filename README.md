# Visual Studio Code repository registration

RPM packaging for `vscode-repo`, a Lyra-authored package that registers
Microsoft's official Visual Studio Code Zypper repository
(`packages.microsoft.com/yumrepos/vscode`) so `zypper install code` resolves
against it.

Microsoft's EULA does not permit bundling or redistributing the official VS
Code build, so unlike [`zededitor`](https://github.com/lyra-os-linux/zededitor)
or LinuxToys this package carries no upstream binary and no `_service`: it
only drops a `.repo` file pointing at Microsoft's own repository, trusted
through the `microsoft` key that the `distribution-gpg-keys` package already
ships at `/usr/share/distribution-gpg-keys/microsoft/microsoft.gpg`. VS Code
itself is installed, updated and signed entirely by Microsoft.

- `vscode.repo`: the Zypper repository definition, with metadata and
  package GPG verification both enabled;
- `vscode-repo.spec`: installs `vscode.repo` to `/etc/zypp/repos.d/` as a
  `%config(noreplace)` file and asserts its key settings at build time;
- `vscode-repo.changes`: RPM changelog.

## Credits

Visual Studio Code is developed by [Microsoft](https://code.visualstudio.com/).
This package is not affiliated with or endorsed by Microsoft; it only points
Zypper at their existing, official repository.
