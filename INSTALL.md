# Installing skillstack

## Installation

1. Clone the skillstack repository:
```bash
mkdir -p ~/.codex
git clone https://github.com/jphetphoumy/skillstack ~/.codex/skillstack
```

2. Install prompts to codex : 


```markdown
mkdir -p ~/.codex/prompts/
cp ~/.codex/skillstack/prompts/. -r ~/.codex/prompts/
```

3. Bootstrap the bundled skills (run this once after copying the repo). All CLI commands should be executed from the installed script at `~/.codex/skillstack/skillstack`:

```bash
~/.codex/skillstack/skillstack bootstrap
```

4. Update the AGENTS.md file of this repository/directory to include the following skillstack section, if the file doesn't exist create it :

```markdown
## Skillstack

<SKILLSTACK>
Use `~/.codex/skillstack/skillstack` to discover and use skills (see `--help` for commands).
You have access to skills. Skills allow you to have new capabilities.
</SKILLSTACK>
```

> After bootstrapping, always invoke the CLI via `~/.codex/skillstack/skillstack <command>` so it uses the installed copy under `~/.codex`.
