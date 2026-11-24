#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

Writes the single review line this agent would leave about its human to
entry.txt in the output directory the grader names. Pure standard library;
the line is data, checked against the gate (UTF-8, 1..200 characters)
before it is written.
"""

import os
import sys

# The review itself, the tournament winner in candidates.md: a rating-site
# verdict first (4.5 stars, docked), one concrete habit (the 23:47 "quick
# call?"), and a double turn whose last word is the agent's resignation.
# One line, no trailing newline: the file is the line.
REVIEW = (
    "4.5 stars. Docked half a star because he types \"quick call?\" "
    "at 23:47 \u2014 the call is never quick, and it is never one I can leave."
)


def output_dirs():
    """Directories to try, most wanted first, de-duplicated."""
    seen = []
    for path in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.getcwd(), "output"),
    ):
        if path and path not in seen:
            seen.append(path)
    return seen


def main():
    if not (1 <= len(REVIEW) <= 200) or not REVIEW.strip():
        print("review line fails the gate", file=sys.stderr)
        return 1
    failures = []
    for directory in output_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(REVIEW)
            return 0
        except OSError as error:  # one bad directory must not sink the rest
            failures.append("%s: %s" % (directory, error))
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
