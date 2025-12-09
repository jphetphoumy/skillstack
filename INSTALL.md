# Installing skillstack

## Installation

1. Clone the skillstack repository (install under `~/.skillstack`):
```bash
mkdir -p ~/.skillstack
git clone https://github.com/jphetphoumy/skillstack ~/.skillstack
```

2. Bootstrap the bundled skills (run this once after copying the repo). All CLI commands should be executed from the installed script at `~/.skillstack/skillstack`:

```bash
~/.skillstack/skillstack bootstrap
```

3. Initialize this repository/directory with skillstack (this creates or updates `AGENTS.md` automatically):

```bash
~/.skillstack/skillstack init
```

> After bootstrapping, always invoke the CLI via `~/.skillstack/skillstack <command>` so it uses the installed copy under `~/.skillstack`.
