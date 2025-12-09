#!/usr/bin/env python3
"""
Ansible Lint Auto-Fixer

This script fixes common ansible-lint errors that can be easily automated:
- yaml[comments]: Add space after # in comments
- schema[meta]: Quote numeric version strings
- meta-incorrect: Replace placeholder metadata values
- name[play]: Add names to unnamed plays
- role-name[path]: Fix role import paths

Usage:
    uv run ansible-lint-fix.py <role_path>
    uv run ansible-lint-fix.py roles/nginx
"""

import re
import sys
from pathlib import Path
import argparse


def fix_yaml_comments(content: str) -> tuple[str, int]:
    """
    Fix YAML comments by adding space after # where missing.
    Returns: (fixed_content, number_of_fixes)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Find comments that don't have a space after #
        # Pattern: # followed by non-whitespace (excluding #-- and empty comments)
        if match := re.match(r'^(\s*)#([^# \n].*)', line):
            indent = match.group(1)
            comment_text = match.group(2)
            fixed_lines.append(f"{indent}# {comment_text}")
            fixes += 1
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), fixes


def fix_schema_meta(content: str) -> tuple[str, int]:
    """
    Fix schema[meta] errors by quoting numeric version strings.
    Returns: (fixed_content, number_of_fixes)
    """
    fixes = 0

    # Fix min_ansible_version numeric values - match unquoted numbers only
    pattern = r'(min_ansible_version:\s+)(\d+(?:\.\d+)*)(\s*)$'

    def quote_version(match):
        nonlocal fixes
        key = match.group(1)
        value = match.group(2)
        trailing = match.group(3)
        fixes += 1
        return f'{key}"{value}"{trailing}'

    content = re.sub(pattern, quote_version, content, flags=re.MULTILINE)

    return content, fixes


def fix_meta_incorrect(content: str, file_path: Path) -> tuple[str, int]:
    """
    Fix meta-incorrect errors by replacing placeholder values.
    Returns: (fixed_content, number_of_fixes)
    """
    fixes = 0

    # Replace placeholder author
    if 'author: your name' in content:
        content = content.replace('author: your name', 'author: Ansible User')
        fixes += 1

    # Replace placeholder company
    if 'company: your company (optional)' in content:
        content = content.replace(
            'company: your company (optional)',
            'company: Community'
        )
        fixes += 1

    # Replace placeholder license
    if 'license: license (GPL-2.0-or-later, MIT, etc)' in content:
        content = content.replace(
            'license: license (GPL-2.0-or-later, MIT, etc)',
            'license: MIT'
        )
        fixes += 1

    return content, fixes


def fix_play_names(content: str) -> tuple[str, int]:
    """
    Fix name[play] errors by adding names to unnamed plays.
    Returns: (fixed_content, number_of_fixes)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a play definition (starts with "- hosts:" or "- name:")
        if re.match(r'^-\s+hosts:\s+', line):
            # Look ahead to see if there's already a name
            has_name = False
            if i > 0:
                prev_line = lines[i - 1]
                if re.match(r'^-?\s+name:\s+', prev_line):
                    has_name = True

            if not has_name:
                # Extract the host pattern
                host_match = re.search(r'hosts:\s+(\S+)', line)
                host_pattern = host_match.group(1) if host_match else 'target hosts'

                # Get indentation
                indent_match = re.match(r'^(\s*)-', line)
                indent = indent_match.group(1) if indent_match else ''

                # Add a name line before the hosts line
                fixed_lines.append(f"{indent}- name: Test playbook for {host_pattern}")
                # Adjust the current line to not have the dash
                line = line.replace('- hosts:', '  hosts:', 1)
                fixes += 1

        fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines), fixes


def fix_role_name_path(content: str, role_name: str) -> tuple[str, int]:
    """
    Fix role-name[path] errors by removing 'roles/' prefix from role imports.
    Returns: (fixed_content, number_of_fixes)
    """
    fixes = 0

    # Fix in roles list (e.g., "- roles/nginx" -> "- nginx")
    pattern = r'(\s+)-\s+roles/' + re.escape(role_name)
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\1- {role_name}', content)
        fixes += 1

    return content, fixes


def process_file(file_path: Path, role_name: str) -> dict:
    """
    Process a single file and apply all fixes.
    Returns: dict with fix counts by type
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        fix_counts = {
            'yaml_comments': 0,
            'schema_meta': 0,
            'meta_incorrect': 0,
            'play_names': 0,
            'role_name_path': 0
        }

        # Apply fixes
        content, count = fix_yaml_comments(content)
        fix_counts['yaml_comments'] = count

        if file_path.name == 'main.yml' and 'meta' in str(file_path.parent):
            content, count = fix_schema_meta(content)
            fix_counts['schema_meta'] += count

            content, count = fix_meta_incorrect(content, file_path)
            fix_counts['meta_incorrect'] = count

        if file_path.name == 'test.yml' or file_path.suffix in ['.yml', '.yaml']:
            content, count = fix_play_names(content)
            fix_counts['play_names'] = count

            content, count = fix_role_name_path(content, role_name)
            fix_counts['role_name_path'] = count

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fix_counts

        return None

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Fix common ansible-lint errors automatically'
    )
    parser.add_argument(
        'role_path',
        type=str,
        help='Path to the Ansible role directory (e.g., roles/nginx)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    role_path = Path(args.role_path)

    if not role_path.exists():
        print(f"Error: Role path '{role_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not role_path.is_dir():
        print(f"Error: '{role_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Extract role name from path
    role_name = role_path.name

    print(f"Fixing ansible-lint issues in: {role_path}")
    print(f"Role name: {role_name}")
    print()

    # Find all YAML files in the role
    yaml_files = list(role_path.rglob('*.yml')) + list(role_path.rglob('*.yaml'))

    if not yaml_files:
        print("No YAML files found in role directory")
        sys.exit(0)

    total_fixes = {
        'yaml_comments': 0,
        'schema_meta': 0,
        'meta_incorrect': 0,
        'play_names': 0,
        'role_name_path': 0
    }
    files_modified = 0

    for yaml_file in sorted(yaml_files):
        relative_path = yaml_file.relative_to(role_path.parent)
        fix_counts = process_file(yaml_file, role_name)

        if fix_counts:
            files_modified += 1
            file_total = sum(fix_counts.values())

            if args.verbose or file_total > 0:
                print(f"✓ {relative_path}")

                if fix_counts['yaml_comments'] > 0:
                    print(f"  - Fixed {fix_counts['yaml_comments']} comment spacing issue(s)")
                    total_fixes['yaml_comments'] += fix_counts['yaml_comments']

                if fix_counts['schema_meta'] > 0:
                    print(f"  - Fixed {fix_counts['schema_meta']} schema version issue(s)")
                    total_fixes['schema_meta'] += fix_counts['schema_meta']

                if fix_counts['meta_incorrect'] > 0:
                    print(f"  - Fixed {fix_counts['meta_incorrect']} metadata placeholder(s)")
                    total_fixes['meta_incorrect'] += fix_counts['meta_incorrect']

                if fix_counts['play_names'] > 0:
                    print(f"  - Added {fix_counts['play_names']} play name(s)")
                    total_fixes['play_names'] += fix_counts['play_names']

                if fix_counts['role_name_path'] > 0:
                    print(f"  - Fixed {fix_counts['role_name_path']} role import path(s)")
                    total_fixes['role_name_path'] += fix_counts['role_name_path']

                print()

    # Summary
    print("=" * 60)
    print("Summary:")
    print(f"  Files modified: {files_modified}")
    print(f"  Total fixes: {sum(total_fixes.values())}")

    if sum(total_fixes.values()) > 0:
        print()
        print("Fixes by type:")
        if total_fixes['yaml_comments'] > 0:
            print(f"  - yaml[comments]: {total_fixes['yaml_comments']}")
        if total_fixes['schema_meta'] > 0:
            print(f"  - schema[meta]: {total_fixes['schema_meta']}")
        if total_fixes['meta_incorrect'] > 0:
            print(f"  - meta-incorrect: {total_fixes['meta_incorrect']}")
        if total_fixes['play_names'] > 0:
            print(f"  - name[play]: {total_fixes['play_names']}")
        if total_fixes['role_name_path'] > 0:
            print(f"  - role-name[path]: {total_fixes['role_name_path']}")

    print("=" * 60)

    if files_modified > 0:
        print()
        print("Run 'ansible-lint roles/nginx 2>/dev/null' to verify fixes")


if __name__ == '__main__':
    main()
