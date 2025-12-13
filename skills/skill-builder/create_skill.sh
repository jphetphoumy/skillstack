#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: create_skill.sh <slug> [description]

Scaffolds a new skill directory under $HOME/.codex/skillstack/skills (override with SKILLSTACK_ROOT).
Example:
    ~/.codex/skillstack/skills/skill-builder/create_skill.sh async-review "Helps review async workflows"
USAGE
    exit 1
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
fi

if [[ $# -lt 1 ]]; then
    usage
fi

slug="$1"
description="${2:-Describe what this skill does.}"

if [[ ! "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
    echo "Error: slug must be lowercase alphanumerics and dashes (got '$slug')." >&2
    exit 2
fi

SKILLSTACK_ROOT="${SKILLSTACK_ROOT:-$HOME/.codex/skillstack}"
skills_dir="$SKILLSTACK_ROOT/skills"
skill_dir="$skills_dir/$slug"
skill_file="$skill_dir/SKILL.md"

mkdir -p "$skill_dir"

if [[ -e "$skill_file" ]]; then
    echo "Error: $skill_file already exists. Remove it or choose another slug." >&2
    exit 3
fi

cat >"$skill_file" <<EOF
---
name: $slug
description: $description
---

Describe the workflow this skill unlocks. Include concrete commands, expected inputs,
and success criteria so Codex can execute the process reliably.
EOF

echo "Created $skill_file"
