# Required CI for main

The GitHub branch protection for `main` requires the check named `validate`,
published by GitHub Actions (app ID `15368`). The check name comes from the
published check run, rather than the workflow title `Packaging contracts`.

The branch must be up to date before merging (`strict=true`). Protection applies
to administrators (`enforce_admins=true`). Changes use pull requests; no extra
reviewer approval is required. Force pushes and branch deletion are disabled.
This policy is configured in GitHub settings, not by this Markdown file.

## Coverage and limits

The existing workflow runs three Python tests and parses the RPM spec with
`rpmspec -P`. It checks the configured Microsoft HTTPS repository URL,
`gpgcheck`/`repo_gpgcheck`, the distribution-provided key path and priority.
It also checks recipe declarations for the key package and `%config(noreplace)`,
and simulates repeatable file installation/removal in a temporary directory.

The tests do not download repository metadata, inspect the key fingerprint or
verify a live signature. File copying in a temporary directory is not an RPM
transaction and does not exercise RPM upgrade/removal or `%config(noreplace)`
behavior. Spec parsing does not build or install the package.

PRs have no path or branch filter, and the required job has no job-level skip
condition. These checks do not replace native GNOME acceptance, signed OBS
artifact qualification, installed RPM validation or the Lyra ISO gates.

## Qualification

On 2026-09-15 the API returned HTTP 404 (`Branch not protected`) for `main`.
The branch reported `protected=false`, and its applicable-rules query returned
an empty list. Protection therefore had to be created.

Merge-blocking and passing-run evidence is recorded in
[issue #1](https://github.com/lyra-os-linux/vscode/issues/1).

## Exceptions and recovery

No user, team or app bypass is configured in this branch protection. Repository
administrators can still deliberately edit or remove the rules; administrator
enforcement constrains merges while the policy is in effect.

GitHub also accepts `neutral` and `skipped` check conclusions. Keep the required
job executing when changing workflow conditions. If the check name or producer
changes, update protection to the exact published name and app identity.

If an explicitly approved recovery requires reverting this change, restore the
recorded unprotected baseline by removing this branch protection. That also
removes its PR, CI, force-push and deletion safeguards. Diagnose a failing check
before considering that recovery; do not disable protection for routine merges.
