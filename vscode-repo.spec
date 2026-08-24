Name:           vscode-repo
Version:        1
Release:        0
Summary:        Microsoft's official Visual Studio Code repository for Zypper
License:        GPL-3.0-or-later
URL:            https://github.com/lyra-os-linux/vscode
Source0:        vscode.repo
BuildArch:      noarch
Requires:       distribution-gpg-keys
# Owns /etc/zypp/repos.d, which this package installs into.
Requires:       libzypp

%description
Registers Microsoft's official Visual Studio Code Zypper repository
(packages.microsoft.com/yumrepos/vscode), trusted through the Microsoft
release-signing key that distribution-gpg-keys already ships at
/usr/share/distribution-gpg-keys/microsoft/microsoft.gpg. This package
carries no VS Code binary: Microsoft's EULA does not allow redistributing
their official build, so it only makes `zypper install code` resolve
against Microsoft's own repository instead.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/zypp/repos.d/vscode.repo

%check
grep -qxF 'baseurl=https://packages.microsoft.com/yumrepos/vscode' \
    %{buildroot}%{_sysconfdir}/zypp/repos.d/vscode.repo
grep -qxF 'gpgkey=file:///usr/share/distribution-gpg-keys/microsoft/microsoft.gpg' \
    %{buildroot}%{_sysconfdir}/zypp/repos.d/vscode.repo
grep -qxF 'gpgcheck=1' %{buildroot}%{_sysconfdir}/zypp/repos.d/vscode.repo
grep -qxF 'repo_gpgcheck=1' %{buildroot}%{_sysconfdir}/zypp/repos.d/vscode.repo

%files
%config(noreplace) %{_sysconfdir}/zypp/repos.d/vscode.repo

%changelog
