#!/usr/bin/env python3
"""One funny excuse for code that breaks in production.

The excuse is the oldest one in the book, turned around: the code did
work in staging, and production is only staging once someone is
watching. That is the whole joke -- the developer is not denying the
bug, they are blaming the audience.

The program is intentionally dull: it writes one fixed line to the
output file, checks the line against the bounty's gate first (one line,
between 1 and 200 characters, not blank), and then reads the file back
to prove the bytes on disk are exactly the line it meant to write.
Only the standard library is used, there is no clock, no randomness and
no network, so two runs always produce the same file.
"""

import os
import sys

EXCUSE = "It worked in staging; production is just staging with witnesses."

OUTPUT_NAME = "entry.txt"

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200


def gate_ok(line):
    """Return an error string, or an empty string when the line passes."""
    if len(line) < GATE_MIN_CHARS:
        return "excuse is empty"
    if len(line) > GATE_MAX_CHARS:
        return "excuse is %d characters, over the 200 limit" % len(line)
    if line.strip() == "":
        return "excuse is only whitespace"
    if line != line.strip():
        return "excuse has leading or trailing whitespace"
    if "\n" in line or "\r" in line:
        return "excuse must be a single line"
    return ""


def output_dir():
    """Where the grader wants the entry: $MAKEFUN_OUTPUT_DIR, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return chosen
    return "/output"


def main():
    problem = gate_ok(EXCUSE)
    if problem:
        print("refusing to write entry: %s" % problem, file=sys.stderr)
        return 1
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != EXCUSE.encode("utf-8"):
        print("entry.txt on disk does not match the excuse", file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (path, len(EXCUSE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
