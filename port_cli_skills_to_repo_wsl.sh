#!/usr/bin/env bash
# Port Claude Code CLI skills from ~/.claude/skills into this repo's .claude/skills,
# so cloud Claude Code sessions (which only see the repo) can load them too.
#
# Run on the machine that has the skills (WSL/Linux/macOS), from anywhere:
#   ./port_cli_skills_to_repo_wsl.sh --dry-run     # show what would be copied
#   ./port_cli_skills_to_repo_wsl.sh               # copy, commit on a new branch
#   ./port_cli_skills_to_repo_wsl.sh --push        # ...and push the branch
#
# Options:
#   --src DIR       source skills dir (default: ~/.claude/skills)
#   --force         overwrite repo skills whose contents differ from the CLI copy
#   --also-agents   mirror ported skills into .agents/skills as well
#   --push          push the new branch to origin
#   --dry-run       report only; change nothing
#
# Safety: symlinks are resolved; .git, node_modules, virtualenvs, caches and .env/key files
# are never copied; a skill containing something that looks like a secret is skipped and
# reported, so it is never committed. Work is committed on a new branch, never on main.
set -euo pipefail

SRC="$HOME/.claude/skills"
FORCE=0; ALSO_AGENTS=0; PUSH=0; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --src) SRC="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --also-agents) ALSO_AGENTS=1; shift ;;
    --push) PUSH=1; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
DEST="$REPO/.claude/skills"
[ -d "$SRC" ] || { echo "Source $SRC not found." >&2; exit 1; }
mkdir -p "$DEST"

if [ "$DRY" = 0 ] && [ -n "$(git -C "$REPO" status --porcelain)" ]; then
  echo "The repo has uncommitted changes; commit or stash them first." >&2; exit 1
fi

EXCLUDES=(.git node_modules __pycache__ .venv venv .pytest_cache .mypy_cache .DS_Store
          '.env' '.env.*' '*.pem' '*.key' 'id_rsa*' 'id_ed25519*' '*.p12' '*.pfx')
SECRET_RE='(sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'

copy_skill() {  # copy_skill <src> <dst>: resolve symlinks, drop excluded paths
  local src="$1" dst="$2"
  rm -rf "$dst"; mkdir -p "$dst"
  if command -v rsync >/dev/null 2>&1; then
    local args=(); for e in "${EXCLUDES[@]}"; do args+=(--exclude "$e"); done
    rsync -aL "${args[@]}" "$src/" "$dst/"
  else
    cp -RL "$src/." "$dst/"
    for e in "${EXCLUDES[@]}"; do find "$dst" -name "$e" -prune -exec rm -rf {} +; done
  fi
}

frontmatter_ok() {  # SKILL.md starts with --- and has name: and description:
  local f="$1/SKILL.md"
  [ -f "$f" ] && [ "$(head -1 "$f")" = "---" ] || return 1
  local fm; fm="$(awk 'NR==1{next} /^---$/{exit} {print}' "$f")"
  grep -q '^name:' <<<"$fm" && grep -q '^description:' <<<"$fm"
}

added=(); updated=(); same=(); differs=(); skipped=()
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

for entry in "$SRC"/*; do
  name="$(basename "$entry")"
  src="$(readlink -f "$entry" 2>/dev/null || echo "$entry")"
  [ -d "$src" ] || continue
  case "$name" in google-agents-cli-*|.*) skipped+=("$name (excluded package)"); continue ;; esac
  frontmatter_ok "$src" || { skipped+=("$name (no SKILL.md with name/description)"); continue; }

  copy_skill "$src" "$TMP/$name"
  if hits="$(grep -rIlE "$SECRET_RE" "$TMP/$name" 2>/dev/null)" && [ -n "$hits" ]; then
    skipped+=("$name (possible secret in: $(echo "$hits" | sed "s#$TMP/$name/##" | tr '\n' ' '))"); continue
  fi
  big="$(find "$TMP/$name" -type f -size +20M | sed "s#$TMP/$name/##" | tr '\n' ' ')"
  [ -n "$big" ] && { skipped+=("$name (files over 20 MB: $big)"); continue; }

  if [ -d "$DEST/$name" ]; then
    if diff -rq "$TMP/$name" "$DEST/$name" >/dev/null 2>&1; then same+=("$name"); continue; fi
    if [ "$FORCE" = 0 ]; then differs+=("$name"); continue; fi
    updated+=("$name")
  else
    added+=("$name")
  fi
  if [ "$DRY" = 0 ]; then
    rm -rf "$DEST/$name"; cp -a "$TMP/$name" "$DEST/$name"
    [ "$ALSO_AGENTS" = 1 ] && { mkdir -p "$REPO/.agents/skills"; rm -rf "$REPO/.agents/skills/$name"; cp -a "$TMP/$name" "$REPO/.agents/skills/$name"; }
  fi
done

report() { local label="$1"; shift; [ $# -gt 0 ] && { echo "$label ($#):"; printf '  %s\n' "$@"; } || true; }
echo "Source: $SRC"; echo "Target: $DEST"; [ "$DRY" = 1 ] && echo "(dry run: nothing changed)"
report "Added" "${added[@]+"${added[@]}"}"
report "Updated (--force)" "${updated[@]+"${updated[@]}"}"
report "Already identical" "${same[@]+"${same[@]}"}"
report "Differs from repo copy, left alone (rerun with --force to overwrite)" "${differs[@]+"${differs[@]}"}"
report "Skipped" "${skipped[@]+"${skipped[@]}"}"

changed=$(( ${#added[@]} + ${#updated[@]} ))
[ "$DRY" = 1 ] && { echo "Dry run complete: rerun without --dry-run to copy and commit."; exit 0; }
[ "$changed" = 0 ] && { echo "Nothing new to commit."; exit 0; }

branch="skills/cli-port-$(date +%Y%m%d-%H%M)"
git -C "$REPO" checkout -q -b "$branch"
git -C "$REPO" add .claude/skills
[ "$ALSO_AGENTS" = 1 ] && git -C "$REPO" add .agents/skills
msg="feat(skills): port ${changed} Claude Code CLI skills into .claude/skills"
body="Copied from ~/.claude/skills with symlinks resolved."
[ ${#added[@]} -gt 0 ] && body+=$'\n\nAdded: '"${added[*]}"
[ ${#updated[@]} -gt 0 ] && body+=$'\n\nUpdated: '"${updated[*]}"
git -C "$REPO" commit -q -m "$msg" -m "$body"
echo "Committed on branch $branch: $msg"
if [ "$PUSH" = 1 ]; then
  git -C "$REPO" push -u origin "$branch"
  echo "Pushed. Open a PR from $branch, or tell Claude to open one."
else
  echo "Not pushed. Run: git -C \"$REPO\" push -u origin $branch"
fi
