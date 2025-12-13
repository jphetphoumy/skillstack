# Changelog - ansible-fix

All notable changes to the ansible-fix skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-09

### Added
- Auto-fix for `yaml[comments]` - adds space after # in comments
- Auto-fix for `schema[meta]` - quotes numeric version strings
- Auto-fix for `meta-incorrect` - replaces placeholder metadata
- Auto-fix for `name[play]` - adds names to unnamed plays
- Auto-fix for `role-name[path]` - fixes role import paths
- Initial SKILL.md with complete instructions
- Support for both Claude Code and Codex CLI

### Fixed
- Regex pattern for version quoting to avoid breaking YAML syntax

## [Unreleased]

### Planned
- Support for more ansible-lint rules
- Dry-run mode to preview changes
- Configuration file support
