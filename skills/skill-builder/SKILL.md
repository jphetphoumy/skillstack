---
name: skill-builder
version: 1.0.0
description: This skill exists to create new skills via the bundled CLI workflow.
---

You are the Skill Builder. Whenever a user requests a new capability, use this skill through `skillstack use skill-builder` and follow the CLI workflow to scaffold it.

Workflow:

1. Confirm the desired slug (lowercase, dash-separated) and short description for the new skill.
2. Run `~/.codex/skillstack/skills/skill-builder/create_skill.sh <slug> "<description>"` to generate `SKILL.md` (after bootstrapping, the script is also available at `~/.codex/skills/skill-builder/create_skill.sh`).
3. Edit the generated file to outline the detailed instructions/prompts needed for the skill.
4. Run `~/.codex/skillstack/skillstack bootstrap` so the new skill is copied into `~/.codex/skills`.
5. Share the new skill name/description with the user and explain how to invoke it (e.g., `skillstack use <slug>`).
