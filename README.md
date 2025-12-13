# Skillstack

**Skillstack** is a skills management system for AI coding agents (Codex CLI and Claude Code).

Skills are reusable automation bundles that help AI agents perform common tasks more effectively.

## Features

- ✅ **Dual System Support**: Works with both Codex CLI and Claude Code
- ✅ **Skill Discovery**: Automatic skill detection and listing
- ✅ **Versioning**: Track skill versions and changes
- ✅ **CLI Tool**: Manage skills with simple commands
- ✅ **Proactive Usage**: Agents automatically use relevant skills
- ✅ **Extensible**: Easy to create new skills

## Quick Start

```bash
# Install
git clone https://github.com/jphetphoumy/skillstack ~/.skillstack
~/.skillstack/skillstack bootstrap --target=both

# List skills
skillstack list

# Use a skill
skillstack use hello-world
```

See [INSTALL.md](INSTALL.md) for detailed instructions.

## What's a Skill?

A skill is a directory with a `SKILL.md` file containing:
- **Frontmatter**: Metadata (name, version, description)
- **Instructions**: Step-by-step guide for AI agents
- **Supporting Files**: Scripts, templates, etc.

Example:
```yaml
---
name: ansible-fix
version: 1.0.0
description: Auto-fix ansible-lint errors after creating roles
---

# Ansible Fix

## Instructions
1. Run ansible-galaxy init
2. Run the fixer script
3. Verify with ansible-lint
```

## Available Skills

Run `skillstack list` to see all installed skills.

Default skills:
- **hello-world**: Test skill to verify installation
- **skill-builder**: Create new skills

## Creating Skills

```bash
# Use the skill-builder
skillstack use skill-builder

# Create new skill
~/.codex/skills/skill-builder/create_skill.sh my-skill "Description"

# Install
skillstack bootstrap --target=both
```

## How It Works

### For Codex CLI

1. Add `AGENTS.md` to your project (template in `templates/AGENTS.md`)
2. Codex reads AGENTS.md on startup
3. Codex checks for skills with `skillstack list`
4. When relevant, Codex reads and follows SKILL.md instructions

### For Claude Code

1. Skills installed to `~/.claude/skills/`
2. Claude Code automatically discovers them
3. When task matches skill description, Claude Code uses it
4. Claude Code reads SKILL.md directly for instructions

## Project Structure

```
skillstack/
├── skillstack              # Main CLI tool
├── list-skills.py          # Discovery script (Claude Code compatible)
├── templates/
│   └── AGENTS.md           # Template for Codex projects
├── skills/                 # Bundled skills
│   ├── hello-world/
│   └── skill-builder/
└── prompts/                # Saved prompts
```

## Contributing

See [PLAN.md](PLAN.md) for development roadmap.

## License

MIT
