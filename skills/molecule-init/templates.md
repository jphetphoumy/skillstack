# Molecule File Templates

## create.yml Template

```yaml
---
- name: Create
  hosts: localhost
  gather_facts: false
  vars:
    molecule_inventory:
      all:
        hosts: {}
        molecule: {}
  tasks:
    - name: Create a container
      community.docker.docker_container:
        name: "{{ item.name }}"
        image: "{{ item.image }}"
        state: started
        command: sleep 1d
        log_driver: json-file
      register: result
      loop: "{{ molecule_yml.platforms }}"

    - name: Print some info
      ansible.builtin.debug:
        msg: "{{ result.results }}"

    - name: Fail if container is not running
      when: >
        item.container.State.ExitCode != 0 or
        not item.container.State.Running
      ansible.builtin.include_tasks:
        file: tasks/create-fail.yml
      loop: "{{ result.results }}"
      loop_control:
        label: "{{ item.container.Name }}"

    - name: Add container to molecule_inventory
      vars:
        inventory_partial_yaml: |
          all:
            children:
              molecule:
                hosts:
                  "{{ item.name }}":
                    ansible_connection: community.docker.docker
      ansible.builtin.set_fact:
        molecule_inventory: >
          {{ molecule_inventory | combine(inventory_partial_yaml | from_yaml, recursive=true) }}
      loop: "{{ molecule_yml.platforms }}"
      loop_control:
        label: "{{ item.name }}"

    - name: Dump molecule_inventory
      ansible.builtin.copy:
        content: |
          {{ molecule_inventory | to_yaml }}
        dest: "{{ molecule_ephemeral_directory }}/inventory/molecule_inventory.yml"
        mode: "0600"

    - name: Force inventory refresh
      ansible.builtin.meta: refresh_inventory

    - name: Fail if molecule group is missing
      ansible.builtin.assert:
        that: "'molecule' in groups"
        fail_msg: |
          molecule group was not found inside inventory groups: {{ groups }}
      run_once: true

- name: Validate that inventory was refreshed
  hosts: molecule
  gather_facts: false
  tasks:
    - name: Check uname
      ansible.builtin.raw: uname -a
      register: result
      changed_when: false

    - name: Display uname info
      ansible.builtin.debug:
        msg: "{{ result.stdout }}"
```

## create-fail.yml Template

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

## converge.yml Template

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
    - name: Include {{NAMESPACE}}.{{ROLE_NAME}} role
      ansible.builtin.include_role:
        name: "{{NAMESPACE}}.{{ROLE_NAME}}"
```

## verify.yml Basic Template

```yaml
---
- name: Verify
  hosts: molecule
  gather_facts: false
  become: true
  tasks:
    - name: Example package check
      ansible.builtin.debug:
        msg: "Add verification tasks based on what your role does"

    # Example: Check if package is installed
    # - name: Check if package is installed
    #   ansible.builtin.package:
    #     name: your-package
    #     state: present
    #   check_mode: true
    #   register: package_check
    #   failed_when: package_check is changed

    # Example: Check if service is running
    # - name: Check if service is running
    #   ansible.builtin.service:
    #     name: your-service
    #     state: started
    #   check_mode: true
    #   register: service_check
    #   failed_when: service_check is changed

    # Example: Check if port is listening
    # - name: Verify service is listening on port
    #   ansible.builtin.wait_for:
    #     port: 80
    #     timeout: 5
```

## destroy.yml Template

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

## molecule.yml Template

```yaml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml
platforms:
  - name: instance
    image: {{DOCKER_IMAGE}}
```

## requirements.yml Template

```yaml
---
collections:
  - name: community.docker
    version: ">=3.10.4"
  - name: ansible.posix
```

## meta/main.yml Template

```yaml
---
galaxy_info:
  role_name: {{ROLE_NAME}}
  namespace: {{NAMESPACE}}
  author: {{AUTHOR}}
  description: {{DESCRIPTION}}
  license: MIT
  min_ansible_version: "2.1"

  platforms:
    - name: Debian
      versions:
        - bookworm
```

## Docker Image Options

Available Docker images for testing:
- `geerlingguy/docker-debian12-ansible:latest` (Debian 12)
- `geerlingguy/docker-ubuntu2204-ansible:latest` (Ubuntu 22.04)
- `geerlingguy/docker-ubuntu2004-ansible:latest` (Ubuntu 20.04)
- `geerlingguy/docker-centos8-ansible:latest` (CentOS 8)
