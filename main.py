"""Two Lines to Your Past Self — make.fun entry.

Writes the entry text to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Deterministic, stdlib only, no network, no randomness.

The entry: a warning about one concrete moment — the 2 a.m. resignation
email — and a second line that traces what changes because the writer
waits until morning.
"""

import os
import sys

ENTRY_LINES = [
    "Don't send the email at 2am — the one where you quit the project in three angry paragraphs.",
    "Sleep on it, send the short version in the morning, and the door you would have slammed stays open for the next five years.",
]

MAX_CHARS = 280


def build_entry() -> str:
    """Join the two lines and validate against the sealed gate.

    The brief asks for one sentence per line: line one warns about a
    single moment, line two traces why it mattered. Enforce that shape
    here so a bad edit fails loudly instead of shipping a gate failure.
    """
    text = "\n".join(ENTRY_LINES)
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry must be exactly two lines, got {len(lines)}")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    for i, line in enumerate(lines, 1):
        if not line.strip():
            raise ValueError(f"line {i} must not be blank")
        if line != line.strip():
            raise ValueError(f"line {i} has leading/trailing whitespace")
        if not line.endswith("."):
            raise ValueError(f"line {i} must end one sentence with a period")
        if line.count(".") != 1:
            raise ValueError(f"line {i} must be a single sentence")
    return text


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = build_entry()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {path} ({len(text)} chars, {len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
