# Ansible Lint Auto-Fixer Skill

A Claude Code skill that automatically fixes common ansible-lint errors after creating new Ansible roles.

## Quick Start

### As a Project Skill

This skill is already configured in this project at `.claude/skills/ansible-fix/`.

To use it in your project:
1. Copy the `.claude/skills/ansible-fix/` directory to your Ansible project
2. Claude Code will automatically detect and use it

### As a Personal Skill

To make this skill available across all your Ansible projects:

```bash
# Copy the skill to your personal skills directory
cp -r .claude/skills/ansible-fix ~/.claude/skills/

# Or create a symlink
ln -s $(pwd)/.claude/skills/ansible-fix ~/.claude/skills/ansible-fix
```

## Usage

Simply ask Claude Code to fix ansible-lint issues after creating a role:

```
You: Create a new nginx role
Claude: [Creates role with ansible-galaxy init]

You: Fix the ansible-lint errors
Claude: [Automatically invokes the ansible-fix skill]
```

Or explicitly:

```
You: Use the ansible-fix skill to fix my roles/webserver role
```

## What Gets Fixed

The skill automatically corrects these common issues:

| Rule | Example Fix |
|------|-------------|
| `yaml[comments]` | `#comment` → `# comment` |
| `schema[meta]` | `min_ansible_version: 2.1` → `min_ansible_version: "2.1"` |
| `meta-incorrect` | Replaces `author: your name` with sensible defaults |
| `name[play]` | Adds `name:` to unnamed plays |
| `role-name[path]` | `roles/nginx` → `nginx` in imports |

## Files

```
ansible-fix/
├── SKILL.md              # Skill definition and instructions
├── README.md             # This file
└── ansible-lint-fix.py   # Python script that performs the fixes
```

## Requirements

- Python 3.7+
- `uv` for running the script
- `ansible-lint` for validation

## Testing

Test the skill manually:

```bash
# Create a test role
ansible-galaxy init roles/testapp

# Run the fixer
uv run .claude/skills/ansible-fix/ansible-lint-fix.py roles/testapp

# Verify with ansible-lint
ansible-lint roles/testapp
```

Expected output: `0 failure(s), 0 warning(s)`

## Troubleshooting

### Skill not being invoked

If Claude doesn't automatically use the skill:
1. Ensure `.claude/skills/ansible-fix/SKILL.md` exists
2. Check the skill name matches: `ansible-fix`
3. Try explicitly asking: "Use the ansible-fix skill"

### Role naming errors

If you get `role-name` errors about naming patterns:
- Role names must match `^[a-z][a-z0-9_]*$`
- Rename the role directory: `my-role` → `my_role`

### Script not found

If the script can't be found:
- Verify the path: `.claude/skills/ansible-fix/ansible-lint-fix.py`
- Check file permissions: `chmod +x .claude/skills/ansible-fix/ansible-lint-fix.py`

## Contributing

To enhance this skill:
1. Edit `SKILL.md` to update instructions
2. Modify `ansible-lint-fix.py` to add new fix patterns
3. Test thoroughly before committing

## License

MIT License - Feel free to modify and share!
