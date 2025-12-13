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
version: 0.1.0
description: $description
changelog: CHANGELOG.md
allowed-tools: Bash, Read, Write, Edit
---

# ${slug^}

## When to Use This Skill

[Describe when this skill should be invoked]

## What It Does

[Describe what the skill accomplishes]

## Instructions

[Step-by-step instructions for using this skill]

1. Step one
2. Step two
3. Step three

## Examples

[Show examples of the skill in action]

## Limitations

[Describe what the skill cannot do]
EOF

# Create CHANGELOG.md
changelog_file="$skill_dir/CHANGELOG.md"
cat >"$changelog_file" <<EOF
# Changelog - $slug

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - $(date +%Y-%m-%d)

### Added
- Initial version
- $description

## [Unreleased]

### Planned
- [Future enhancements]
EOF

echo "Created skill at $skill_dir"
echo "  - $skill_file"
echo "  - $changelog_file"
echo ""
echo "Next steps:"
echo "  1. Edit $skill_file to add detailed instructions"
echo "  2. Run: ./skillstack bootstrap"
echo "  3. Test: skillstack use $slug"
