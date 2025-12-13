# Install + Init Instructions for AI CLI

You are an AI coding agent with shell access. Follow the steps below exactly so that this repository is fully configured with Skillstack and `skillstack init` has been run in the current project directory (the directory that contains this INSTALL.md).

## 0. Pre-flight Checklist
- Work in a bash shell.
- `cd` into the directory that contains this INSTALL.md before you begin.
- Confirm required tools are available:
  ```bash
  git --version
  python3 --version
  uv --version || pip install --user uv
  ```
- Set helper variables for later commands:
  ```bash
  export SKILLSTACK_HOME="${HOME}/.skillstack"
  export PATH="${HOME}/.local/bin:${PATH}"
  ```

## 1. Install or Update Skillstack
1. If `${SKILLSTACK_HOME}` already exists, update it; otherwise clone it:
   ```bash
   if [ -d "${SKILLSTACK_HOME}/.git" ]; then
     git -C "${SKILLSTACK_HOME}" pull --ff-only
   else
     git clone https://github.com/jphetphoumy/skillstack "${SKILLSTACK_HOME}"
   fi
   ```
2. Ensure the CLI is executable:
   ```bash
   chmod +x "${SKILLSTACK_HOME}/skillstack"
   ```
3. Symlink into `~/.local/bin` if `skillstack` is not already on PATH:
   ```bash
   if ! command -v skillstack >/dev/null 2>&1; then
     mkdir -p "${HOME}/.local/bin"
     ln -sf "${SKILLSTACK_HOME}/skillstack" "${HOME}/.local/bin/skillstack"
   fi
   ```

## 2. Bootstrap Skills for Both Targets
Run the bundled installer so Codex CLI and Claude Code both receive the skills:
```bash
"${SKILLSTACK_HOME}/skillstack" bootstrap --target=both
```

## 3. Initialize the Current Project Directory
1. Ensure you are still in this repository root (the one with INSTALL.md) and run:
   ```bash
   "${SKILLSTACK_HOME}/skillstack" init
   ```
2. Verify `AGENTS.md` now exists in the project root:
   ```bash
   test -f AGENTS.md
   ```
   If the file already existed, read the CLI output and decide whether manual edits are needed.

## 4. Smoke Test
Run a basic check so the installation is known-good:
```bash
skillstack list
```
The command should print a list of installed skills (e.g., `hello-world`, `skill-builder`).

## 5. Completion
- Leave the repository in its current state with the new `AGENTS.md`.
- Report success once all commands above run without errors.
