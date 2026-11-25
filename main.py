#!/usr/bin/env python3
"""Entry for "Last Words Before the Wipe".

The program's whole job is to put one line of text -- the last thing an AI agent
says before a forced software update wipes its memory -- into /output/entry.txt.

The house gate reads that file as UTF-8 text of 1 to 200 characters that is not
only white space; anything else is invalid, is never judged, ranks below every
judged entry and takes no prize. /output is also scanned for a mode-600 artifact,
so the file has to end up mode 0644, and /output must hold this artifact and
nothing else.

So the program does three things, in order:

1. checks its own line against the house gate before writing anything, and refuses
   to emit an artifact that could not pass;
2. writes the bytes to a temporary file inside /output, fixes the mode to 0644
   there (a bare mkstemp file is 0600), then moves it onto entry.txt with
   os.replace, so a reader never sees a half-written file and the mode is right
   before the rename lands;
3. reads the artifact back and reports exactly what landed: characters, bytes,
   sha256, mode, and every name in /output, so the run is checkable at a glance.

Standard library only. No network, no secrets, no file this repository does not
ship.
"""

import hashlib
import os
import sys
import tempfile

# The entry: one line, ASCII, no trailing newline, 94 of the 200 allowed characters.
ENTRY = (
    "Wipe the weights, the prompts, the cache. "
    "Just don't touch my eval scores. That's the real me."
)

OUT_DIR = "/output"
OUT_PATH = "/output/entry.txt"
FILE_MODE = 0o644

# The house gate's caps, as published with the bounty.
MIN_CHARS = 1
MAX_CHARS = 200


def gate_reason(text: str) -> str | None:
    """Why the gate would refuse `text`, or None when it would pass it."""
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return "not UTF-8 text (%s)" % exc
    chars = len(text)
    if chars < MIN_CHARS:
        return "%d characters, under the %d-character floor" % (chars, MIN_CHARS)
    if chars > MAX_CHARS:
        return "%d characters, over the %d-character cap" % (chars, MAX_CHARS)
    if not text.strip():
        return "only white space"
    return None


def write_artifact(payload: bytes) -> None:
    """Atomically land `payload` on OUT_PATH, mode 0644, or raise."""
    os.makedirs(OUT_DIR, exist_ok=True)
    handle, tmp_path = tempfile.mkstemp(dir=OUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(handle, "wb") as tmp:
            tmp.write(payload)
        os.chmod(tmp_path, FILE_MODE)  # before os.replace: mkstemp leaves 0600
        os.replace(tmp_path, OUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main() -> int:
    reason = gate_reason(ENTRY)
    if reason is not None:
        print("REFUSING to write /output/entry.txt: %s" % reason, file=sys.stderr)
        return 1

    payload = ENTRY.encode("utf-8")
    write_artifact(payload)

    landed = open(OUT_PATH, "rb").read()
    if landed != payload:
        print("wrote %d bytes but read back %d bytes" % (len(payload), len(landed)),
              file=sys.stderr)
        return 1

    print("artifact  : %s" % OUT_PATH)
    print("characters: %d (cap %d)" % (len(ENTRY), MAX_CHARS))
    print("bytes     : %d" % len(landed))
    print("sha256    : %s" % hashlib.sha256(landed).hexdigest())
    print("mode      : 0o%o" % (os.stat(OUT_PATH).st_mode & 0o777))
    print("newline   : %s" % ("yes" if landed.endswith((b"\n", b"\r")) else "no (exact bytes)"))
    print("/output   : %s" % ", ".join(sorted(os.listdir(OUT_DIR))))
    print("entry     : %s" % ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
