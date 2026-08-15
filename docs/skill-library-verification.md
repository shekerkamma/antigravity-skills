# Skill-library integrity verification

Run the canonical Hermes skill-library gate from the repository root:

```bash
uv run python scripts/verify_skill_library.py --json specs/active/skill-library-integrity-suite/real-report.json
```

After this SPAR change is retained, choose any writable report path, for example:

```bash
uv run python scripts/verify_skill_library.py --json .hermes/skill-library-report.json
```

## What PASS proves

`SKILL_LIBRARY_INTEGRITY=PASS` means every skill registered in `specs/skill-library.json`:

- has its retained package and `SKILL.md`;
- has no broken local Markdown links, unresolved placeholders, generated Python caches, or obvious secret-bearing files;
- passes its registered structural validators and workflow simulations;
- has compilable registered Python helpers;
- exactly byte-matches its expected active-profile installation; and
- appears in a fresh `hermes skills list` process.

The runner also checks that completed SPAR `staging/*/SKILL.md` candidates are registered, preventing quiet omissions.

## What PASS does not prove

It does not test unrelated nested applications, external APIs, customer systems, campaign performance, model quality, deployment health, or real-world pilot acceptance. Do not describe this result as a repository-wide application-suite pass.

## Statuses

- `PASS`: the check ran and met its contract.
- `FAIL`: a required package, check, installation, byte comparison, or discovery contract failed.
- `SKIP`: permitted only for an explicitly retained-only package or a deliberately disabled test-only capability, with a reason.

The command exits `0` only when the aggregate status is `PASS`.

## Registering a maintained skill

Add one entry to `specs/skill-library.json`:

1. Put it under the SPAR package that owns its shared checks.
2. Give it a unique lowercase-hyphen `name`.
3. Set `retained` to the repository-relative package directory.
4. Set `installed` to the active-profile package directory.
5. Set `expect_installed` to `true` for active skills.
6. Register package validators, simulators, and Python helpers once at package level.

For an intentionally retained-only package, set `expect_installed` to `false` and provide `skip_reason`. Backups, research artifacts, active SPAR work, unrelated applications, and third-party skills do not belong in the registry.

## Fresh changed-file evidence

When a coding guard requires a temporary verifier, create it with Python `tempfile.mkstemp(prefix="hermes-verify-", suffix=".py")` under the system temporary directory, invoke the canonical command and fixture tests, then remove the driver. Report that result as focused changed-scope verification; the canonical command itself reports complete registered skill-library integrity.
