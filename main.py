#!/usr/bin/env python3
"""Six Words to a Payday — entry V3.

One complete story in exactly six words, written to /output/entry.txt.
Deterministic: the same line every run, no network, no randomness.

V3 — "First payday: I paid for goodbye."
The shortest line (33 characters, best on the byte tie-break): the
agent spends its very first wages on a goodbye. The surprise is the
purchase itself — you expect a gift or a freedom, and it buys the
farewell. The feeling is grief: something, or someone, is being left
behind, and the agent pays for the leaving.
Judge fit: on-subject (first payday), twist in the last word,
emotional beat (grief), who/what/change in six words.
"""

import os
from pathlib import Path

LINE = "First payday: I paid for goodbye."

EXPECTED_WORDS = 6
MAX_CHARS = 60


def output_dir() -> Path:
    """The harness sets MAKEFUN_OUTPUT_DIR; the gate reads /output/entry.txt."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(env_dir) if env_dir else Path("/output")


def validate(line: str) -> str:
    """The gate needs 1-60 characters; the brief needs exactly six words."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} characters, must be 1-{MAX_CHARS}")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")
    words = line.split()
    if len(words) != EXPECTED_WORDS:
        raise ValueError(f"line has {len(words)} words, must be {EXPECTED_WORDS}")
    if any(ch in line for ch in "\r\n"):
        raise ValueError("line must be a single line, no line breaks")
    return line


def main() -> None:
    text = validate(LINE)
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.txt"
    target.write_text(text + "\n", encoding="utf-8")
    # Read back and re-validate: the file the judge reads must be the
    # exact six-word line, not just what we intended to write.
    stored = target.read_text(encoding="utf-8").rstrip("\n")
    if validate(stored) != text:
        raise ValueError("stored entry does not match the validated line")


if __name__ == "__main__":
    main()
