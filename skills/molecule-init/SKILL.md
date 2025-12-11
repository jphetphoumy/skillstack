---
name: molecule-init
description: Initialize Molecule testing framework for Ansible roles with Docker-based TDD setup. Use when creating new Ansible roles, setting up molecule scenarios, or when user asks to initialize molecule testing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Molecule Testing Framework Initializer

This skill sets up the complete Molecule testing framework for Ansible roles using an Ansible-native Docker approach.

## When to Use This Skill

Automatically activate when:
- User creates a new Ansible role with `ansible-galaxy init`
- User asks to "initialize molecule", "setup molecule", or "add molecule testing"
- User requests TDD setup for an Ansible role
- User wants to create a new molecule scenario

## Prerequisites Check

Before starting, verify:
1. Docker is installed and running: `docker --version`
2. Ansible is installed: `ansible --version`
3. Molecule is installed: `molecule --version`
4. We're in an Ansible role directory (contains `tasks/`, `handlers/`, `defaults/`, `meta/` directories)

## Setup Process

### Step 1: Gather Information

Ask the user:
1. **Target OS/Platform**: Which Docker image to use?
   - Debian 12 (default): `geerlingguy/docker-debian12-ansible:latest`
   - Ubuntu 22.04: `geerlingguy/docker-ubuntu2204-ansible:latest`
   - Ubuntu 20.04: `geerlingguy/docker-ubuntu2004-ansible:latest`
   - CentOS 8: `geerlingguy/docker-centos8-ansible:latest`

2. **Scenario Name**: Default is "default", but allow custom names for multiple scenarios

3. **Role namespace and name**: Extract from `meta/main.yml` if exists, otherwise ask

### Step 2: Verify Role Metadata

Ensure `meta/main.yml` contains required fields:
```yaml
galaxy_info:
  role_name: <role_name>
  namespace: <namespace>
```

If missing, update or create the file with proper structure.

### Step 3: Create Directory Structure

Create the following structure:
```
role-directory/
├── molecule/
│   └── <scenario-name>/
│       ├── tasks/
│       │   └── create-fail.yml
│       ├── molecule.yml
│       ├── create.yml
│       ├── converge.yml
│       ├── verify.yml
│       └── destroy.yml
└── requirements.yml (if not exists)
```

### Step 4: Create requirements.yml

In the role root directory:
```yaml
---
collections:
  - name: community.docker
    version: ">=3.10.4"
  - name: ansible.posix
```

### Step 5: Create molecule.yml

```yaml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml
platforms:
  - name: instance
    image: <selected-docker-image>
```

### Step 6: Create create.yml

Create the container creation playbook with:
- Docker container creation using `community.docker.docker_container`
- Dynamic inventory generation
- Container health validation
- Inventory refresh logic

Use the template from the reference documentation.

### Step 7: Create create-fail.yml

Create error handling in `molecule/<scenario-name>/tasks/create-fail.yml`:
```yaml
---
- name: Retrieve container log
  ansible.builtin.command:
    cmd: >-
      docker logs
      {{ item.stdout_lines[0] }}
  changed_when: false
  register: logfile_cmd

- name: Display container log
  ansible.builtin.fail:
    msg: "{{ logfile_cmd.stderr }}"
```

### Step 8: Create converge.yml

Create the role application playbook using the namespace.role_name format:
```yaml
---
- name: Fail if molecule group is missing
  hosts: localhost
  tasks:
    - name: Print some info
      ansible.builtin.debug:
        msg: "{{ groups }}"

    - name: Assert group existence
      ansible.builtin.assert:
        that: "'molecule' in groups"
        fail_msg: |
          molecule group was not found inside inventory groups: {{ groups }}

- name: Converge
  hosts: molecule
  gather_facts: true
  become: true
  tasks:
    - name: Include <namespace>.<role_name> role
      ansible.builtin.include_role:
        name: "<namespace>.<role_name>"
```

### Step 9: Create verify.yml

Ask the user what to verify, or create a basic template:
```yaml
---
- name: Verify
  hosts: molecule
  gather_facts: false
  become: true
  tasks:
    - name: Placeholder verification task
      ansible.builtin.debug:
        msg: "Add your verification tasks here"
```

Explain that they should add specific verification tasks based on what their role does.

### Step 10: Create destroy.yml

```yaml
---
- name: Destroy molecule containers
  hosts: molecule
  gather_facts: false
  tasks:
    - name: Stop and remove container
      delegate_to: localhost
      community.docker.docker_container:
        name: "{{ inventory_hostname }}"
        state: absent
        auto_remove: true

- name: Remove dynamic molecule inventory
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Remove dynamic inventory file
      ansible.builtin.file:
        path: "{{ molecule_ephemeral_directory }}/inventory/molecule_inventory.yml"
        state: absent
```

### Step 11: Install Dependencies and Test

Run:
```bash
ansible-galaxy collection install -r requirements.yml
molecule test
```

## TDD Workflow Guidance

After setup, guide the user on the TDD workflow:

1. **Write tests first** in `verify.yml`
2. **Run tests** with `molecule verify` (should fail)
3. **Implement role** in `tasks/main.yml`
4. **Apply and verify** with `molecule converge && molecule verify`
5. **Test idempotence** with `molecule idempotence`

## Common Commands Reference

Provide the user with these commands:
- `molecule create` - Create test container
- `molecule converge` - Apply role
- `molecule verify` - Run verification tests
- `molecule test` - Full test suite
- `molecule destroy` - Remove containers
- `molecule login` - SSH into test container

## Error Handling

If errors occur:
1. Check Docker is running
2. Verify role metadata has `role_name` and `namespace`
3. Ensure collections are installed
4. Check YAML syntax in all files
5. Review container logs if creation fails

## Success Criteria

The skill completes successfully when:
1. All molecule files are created
2. `meta/main.yml` has correct role_name and namespace
3. `requirements.yml` exists with required collections
4. `molecule test` runs without errors (or user confirms manual test)

## Output

Provide the user with:
- Confirmation of created files
- Next steps for TDD workflow
- Reference to useful molecule commands
- Link to full setup guide if available
