# Installing Skillstack

Skillstack works with both **Codex CLI** and **Claude Code**.

## Quick Install (Both Systems)

```bash
# 1. Clone skillstack
git clone https://github.com/jphetphoumy/skillstack ~/.skillstack

# 2. Install skills to both Codex and Claude Code
~/.skillstack/skillstack bootstrap --target=both

# 3. (Optional) Add CLI to PATH
ln -s ~/.skillstack/skillstack ~/.local/bin/skillstack
```

This installs skills to:
- `~/.codex/skills/` (for Codex CLI)
- `~/.claude/skills/` (for Claude Code)

## Install for Specific System Only

**Codex CLI only:**
```bash
~/.skillstack/skillstack bootstrap --target=codex
```

**Claude Code only:**
```bash
~/.skillstack/skillstack bootstrap --target=claude
```

## Using Skills

### With Codex CLI

1. Add AGENTS.md to your project:
```bash
cp ~/.skillstack/templates/AGENTS.md ./AGENTS.md
```

2. Start codex:
```bash
codex
```

3. Codex will automatically discover and use skills based on AGENTS.md instructions.

### With Claude Code

Skills are automatically discovered from `~/.claude/skills/` - no setup needed!

Claude Code reads SKILL.md files directly and uses them when relevant.

## Checking Installed Skills

```bash
# Using skillstack CLI
skillstack list

# Or directly (works for both)
ls -la ~/.claude/skills/
ls -la ~/.codex/skills/

# Or using Python script
uv run ~/.skillstack/list-skills.py --format=summary
```

## Creating New Skills

Use the skill-builder skill:

```bash
# View instructions
skillstack use skill-builder

# Create new skill
~/.codex/skills/skill-builder/create_skill.sh my-new-skill "Description here"

# Bootstrap to install
skillstack bootstrap --target=both
```

## Updating

```bash
# Pull latest
cd ~/.skillstack
git pull

# Re-install
./skillstack bootstrap --target=both
```

## Uninstalling

```bash
# Remove skills
rm -rf ~/.codex/skills
rm -rf ~/.claude/skills

# Remove skillstack
rm -rf ~/.skillstack
rm ~/.local/bin/skillstack  # if you symlinked
```

## Troubleshooting

### Skills not found in Codex

- Check AGENTS.md exists in your project
- Check skills installed: `ls ~/.codex/skills/`
- Try: `skillstack bootstrap --target=codex`

### Skills not found in Claude Code

- Check skills installed: `ls ~/.claude/skills/`
- Try: `skillstack bootstrap --target=claude`

### "No skills found" when listing

- Run bootstrap: `skillstack bootstrap --target=both`
- Check repo has skills: `ls ~/.skillstack/skills/`
