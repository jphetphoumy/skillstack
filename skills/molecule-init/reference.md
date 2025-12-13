# Molecule Setup Reference Guide

## Directory Structure Overview

```
ansible-role/
├── molecule/
│   └── default/              # Scenario name (can be: default, ubuntu, debian, etc.)
│       ├── tasks/
│       │   └── create-fail.yml
│       ├── molecule.yml      # Main configuration
│       ├── create.yml        # Container creation playbook
│       ├── converge.yml      # Role application playbook
│       ├── verify.yml        # Verification tests
│       └── destroy.yml       # Cleanup playbook
├── requirements.yml          # Ansible collections requirements
├── tasks/
├── handlers/
├── defaults/
└── meta/
    └── main.yml             # MUST contain role_name and namespace
```

## Key Configuration Points

### 1. Role Metadata (meta/main.yml)

**Critical fields:**
- `galaxy_info.role_name`: Short name for the role
- `galaxy_info.namespace`: Organization or username namespace

These MUST match the name used in `converge.yml`:
```yaml
# meta/main.yml
galaxy_info:
  role_name: apache2
  namespace: community

# converge.yml must use:
name: "community.apache2"
```

### 2. Container Connection Method

Molecule uses `ansible_connection: community.docker.docker` for container connections.

This is set in the dynamic inventory created by `create.yml`:
```yaml
ansible_connection: community.docker.docker
```

**Important:** This is NOT the default Docker connection plugin. It's from the `community.docker` collection.

### 3. Molecule Test Sequence

When you run `molecule test`, it executes:
1. `dependency` - Install collections from requirements.yml
2. `cleanup` - Clean up from previous runs
3. `destroy` - Remove old containers
4. `syntax` - Check playbook syntax
5. `create` - Create test containers
6. `prepare` - Prepare containers (optional)
7. `converge` - Apply your role
8. `idempotence` - Apply role again (should be no changes)
9. `verify` - Run verification tests
10. `cleanup` - Clean up
11. `destroy` - Remove containers

### 4. TDD Development Workflow

**Red-Green-Refactor cycle:**

1. **Red** - Write failing test:
   ```yaml
   # verify.yml
   - name: Check Apache is installed
     ansible.builtin.package:
       name: apache2
       state: present
     check_mode: true
     register: result
     failed_when: result is changed
   ```

2. **Run** - See it fail:
   ```bash
   molecule verify
   ```

3. **Green** - Implement feature:
   ```yaml
   # tasks/main.yml
   - name: Install Apache
     ansible.builtin.package:
       name: apache2
       state: present
   ```

4. **Test** - Verify it passes:
   ```bash
   molecule converge
   molecule verify
   ```

5. **Refactor** - Check idempotence:
   ```bash
   molecule idempotence
   ```

### 5. Verification Test Patterns

**Pattern 1: Package installed check**
```yaml
- name: Check if package is installed
  ansible.builtin.package:
    name: package-name
    state: present
  check_mode: true
  register: pkg_check
  failed_when: pkg_check is changed
```

**Pattern 2: Service running check**
```yaml
- name: Check if service is running
  ansible.builtin.service:
    name: service-name
    state: started
    enabled: true
  check_mode: true
  register: svc_check
  failed_when: svc_check is changed
```

**Pattern 3: Port listening check**
```yaml
- name: Verify port is listening
  ansible.builtin.wait_for:
    port: 80
    timeout: 5
```

**Pattern 4: File exists check**
```yaml
- name: Check if file exists
  ansible.builtin.stat:
    path: /path/to/file
  register: file_stat
  failed_when: not file_stat.stat.exists
```

**Pattern 5: Configuration content check**
```yaml
- name: Verify configuration contains expected content
  ansible.builtin.lineinfile:
    path: /path/to/config
    line: "expected content"
    state: present
  check_mode: true
  register: config_check
  failed_when: config_check is changed
```

### 6. Multi-Platform Testing

Test against multiple OS versions:

```yaml
# molecule.yml
platforms:
  - name: debian12
    image: geerlingguy/docker-debian12-ansible:latest
  - name: ubuntu2204
    image: geerlingguy/docker-ubuntu2204-ansible:latest
```

Molecule will test your role against all platforms in parallel.

### 7. Container Customization

Add privileged mode for systemd services:

```yaml
# molecule.yml
platforms:
  - name: instance
    image: geerlingguy/docker-debian12-ansible:latest
    privileged: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    cgroupns_mode: host
```

Add port mappings:

```yaml
platforms:
  - name: instance
    image: geerlingguy/docker-debian12-ansible:latest
    published_ports:
      - "8080:80"
```

Add environment variables:

```yaml
platforms:
  - name: instance
    image: geerlingguy/docker-debian12-ansible:latest
    env:
      DEBIAN_FRONTEND: noninteractive
```

### 8. Multiple Scenarios

Create different test scenarios:

```bash
molecule/
├── default/          # Basic Debian 12 test
├── ubuntu/           # Ubuntu 22.04 test
└── multi-platform/   # Test multiple platforms
```

Run specific scenario:
```bash
molecule test --scenario-name ubuntu
```

### 9. Debugging Tips

**Container won't start:**
```bash
docker logs instance
```

**Role not found:**
- Check `meta/main.yml` has `role_name` and `namespace`
- Verify `converge.yml` uses `namespace.role_name` format

**Collections not found:**
```bash
ansible-galaxy collection install -r requirements.yml
```

**View molecule logs:**
```bash
molecule --debug create
```

**Login to container:**
```bash
molecule login
```

**Check container state:**
```bash
docker ps -a | grep instance
```

### 10. Best Practices

1. **Match production environment** - Use same OS version as production
2. **Test idempotence** - Role should be safe to run multiple times
3. **Keep scenarios focused** - One scenario per OS/configuration
4. **Use check_mode** - Verify state without making changes
5. **Test edge cases** - Missing files, empty configs, etc.
6. **Fast feedback loop** - Run `molecule converge` frequently
7. **Clean state** - Always `molecule destroy` when changing configs
8. **Document dependencies** - Note required packages in verify.yml comments

### 11. Common Molecule Commands

```bash
# Development cycle
molecule create          # Create container
molecule converge        # Apply role
molecule verify          # Run tests
molecule destroy         # Clean up

# Full test suite
molecule test            # Complete test sequence

# Debugging
molecule login           # SSH into container
molecule --debug test    # Verbose output

# Dependency management
molecule dependency      # Install collections

# Specific scenarios
molecule test --scenario-name ubuntu
molecule converge --scenario-name default

# Check syntax
molecule syntax
```

### 12. Requirements Installation

Before first run:
```bash
# Install required collections
ansible-galaxy collection install -r requirements.yml

# Or let molecule handle it
molecule dependency
```

### 13. CI/CD Integration

Molecule is designed for CI/CD. GitHub Actions example:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install molecule molecule-plugins[docker] ansible
      - run: molecule test
```

## Troubleshooting Checklist

- [ ] Docker is running: `docker ps`
- [ ] Molecule installed: `molecule --version`
- [ ] Collections installed: `ansible-galaxy collection list | grep docker`
- [ ] In role directory: Check for `meta/main.yml`
- [ ] Role metadata has `role_name` and `namespace`
- [ ] Converge uses `namespace.role_name` format
- [ ] All YAML files have valid syntax
- [ ] Docker image exists: `docker pull <image-name>`
