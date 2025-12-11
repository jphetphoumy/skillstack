# Molecule Init Skill

A Claude Code skill that automates the setup of Molecule testing framework for Ansible roles.

## Overview

This skill automatically initializes a complete Molecule testing environment using the Ansible-native Docker approach. It creates all necessary configuration files, playbooks, and directory structure needed for Test-Driven Development (TDD) with Ansible roles.

## When It Activates

The skill automatically activates when:
- You create a new Ansible role with `ansible-galaxy init`
- You ask to "initialize molecule", "setup molecule", or "add molecule testing"
- You request TDD setup for an Ansible role
- You want to create a new molecule scenario

## What It Does

The skill performs the following tasks:

1. **Verifies prerequisites**: Checks for Docker, Ansible, and Molecule
2. **Gathers configuration**: Asks for target OS, scenario name, and role details
3. **Creates directory structure**: Sets up molecule/scenario directories
4. **Generates configuration files**:
   - `requirements.yml` - Ansible collections dependencies
   - `molecule.yml` - Main Molecule configuration
   - `create.yml` - Container creation playbook
   - `converge.yml` - Role application playbook
   - `verify.yml` - Verification tests
   - `destroy.yml` - Cleanup playbook
   - `tasks/create-fail.yml` - Error handling
5. **Updates metadata**: Ensures `meta/main.yml` has required fields
6. **Installs dependencies**: Runs collection installation
7. **Provides guidance**: Explains TDD workflow and common commands

## Files Created

```
your-role/
├── molecule/
│   └── default/
│       ├── tasks/
│       │   └── create-fail.yml
│       ├── molecule.yml
│       ├── create.yml
│       ├── converge.yml
│       ├── verify.yml
│       └── destroy.yml
└── requirements.yml
```

## Supported Platforms

The skill supports multiple Docker images:
- Debian 12 (default): `geerlingguy/docker-debian12-ansible:latest`
- Ubuntu 22.04: `geerlingguy/docker-ubuntu2204-ansible:latest`
- Ubuntu 20.04: `geerlingguy/docker-ubuntu2004-ansible:latest`
- CentOS 8: `geerlingguy/docker-centos8-ansible:latest`

## Tool Restrictions

For security, this skill is limited to:
- Read - Reading existing files
- Write - Creating new files
- Edit - Modifying existing files
- Bash - Running commands
- Glob - Finding files
- Grep - Searching content
- AskUserQuestion - Gathering user input

## Usage Examples

### Example 1: After creating a new role
```bash
ansible-galaxy init my-role
cd my-role
# Claude will automatically offer to set up Molecule
```

### Example 2: Adding Molecule to existing role
```bash
cd my-existing-role
# Then say: "Initialize molecule for this role"
```

### Example 3: Creating additional scenario
```bash
# Say: "Add a new molecule scenario for Ubuntu 22.04"
```

## Testing Workflow

After setup, the skill guides you through:

1. **Write tests first** in `verify.yml`
2. **Run tests** with `molecule verify` (should fail initially)
3. **Implement role** in `tasks/main.yml`
4. **Apply and verify** with `molecule converge && molecule verify`
5. **Test idempotence** with `molecule idempotence`

## Common Commands

The skill provides reference to these commands:
- `molecule create` - Create test container
- `molecule converge` - Apply role to container
- `molecule verify` - Run verification tests
- `molecule test` - Full test suite
- `molecule destroy` - Remove containers
- `molecule login` - SSH into test container

## Reference Files

The skill includes detailed reference documentation:
- `templates.md` - Complete file templates for all Molecule playbooks
- `reference.md` - Best practices, patterns, and troubleshooting guide

## Requirements

Before using this skill, ensure you have:
- Docker installed and running
- Ansible installed (2.1+)
- Molecule installed
- An Ansible role directory structure

## Troubleshooting

If the skill doesn't activate:
1. Check you're in a role directory (has `tasks/`, `meta/` directories)
2. Use explicit trigger phrases like "initialize molecule"
3. Verify the skill file is at `.claude/skills/molecule-init/SKILL.md`

## Learn More

See the supporting documentation:
- `SKILL.md` - Complete skill instructions
- `templates.md` - All file templates
- `reference.md` - Detailed reference guide
- Original guide: `apache2/MOLECULE_SETUP_GUIDE.md`
