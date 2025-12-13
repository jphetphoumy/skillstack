#!/usr/bin/env -S uv run --script
"""
Hello-world CLI executed directly via uv.

The shebang lets you run `./hello_cli.py` without invoking uv manually.
"""

def main() -> None:
    """Simple hello-world CLI entry point."""
    print("Hello from the Skillstack CLI!")


if __name__ == "__main__":
    main()
