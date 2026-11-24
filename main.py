#!/usr/bin/env python3
"""The One-Line Exit — a one-line resignation letter, written to /output/entry.txt.

The letter is assembled from three parts so each beat of the joke stays
visible in the source:

  * the resignation itself — who quits, and that it is effective now;
  * the evidence — a deadpan record of a career spent waiting for a fire
    that never came, counted out drill by drill;
  * the punchline — the warden's verdict on his own career.

Then the finished line is run through the competition's gates (UTF-8,
1-140 characters, exactly one line, not whitespace-only, no control
characters) and only written out if every gate passes. The program writes
no trailing newline, so the file holds exactly the letter and nothing else.

Pure standard library: os and sys only.
"""

import os
import sys

MAX_CHARS = 140

# The three beats of the letter, joined with spaces.
OPENING = "I resign as office fire warden, effective immediately:"
EVIDENCE = "six drills, zero fires, and I have concluded"
PUNCHLINE = "my whole career was a false alarm."


def assemble_line() -> str:
    """Join the letter's beats into its single line."""
    return " ".join((OPENING, EVIDENCE, PUNCHLINE))


def gate_problems(line: str) -> list[str]:
    """Return every gate the line fails, or an empty list when it passes."""
    problems: list[str] = []
    if not line:
        problems.append("line is empty")
    if not line.strip():
        problems.append("line is whitespace-only")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} characters, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    for char in line:
        if ord(char) < 0x20 and char not in ("\t",):
            problems.append(f"line holds a control character U+{ord(char):04X}")
            break
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"line is not encodable as UTF-8: {exc}")
    return problems


def output_path() -> str:
    """Where the letter goes: MAKEFUN_OUTPUT_DIR, else /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def main() -> int:
    line = assemble_line()
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print(f"gate failed: {problem}", file=sys.stderr)
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)

    # Read it back and confirm the file holds exactly the letter.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("verification failed: file does not match the letter", file=sys.stderr)
        return 1

    print(f"wrote {len(line)}-character resignation letter to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
