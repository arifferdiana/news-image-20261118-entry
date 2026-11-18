#!/usr/bin/env python3
"""One newspaper front page for Wednesday 18 November 2026.

This is the make.fun news-image-20261118 entry. It ships a single
original broadsheet, "THE WORLD IN ONE DAY", that sums up the day in
32 stories: a banner photograph of tankers and warships beneath a
burning sky, two lead items (Washington sinking five Iranian tankers;
Xi Jinping opening APEC in Shenzhen with Trump and Putin arriving),
fifteen further stories from around the world and fifteen from
Indonesia, laid out in three dense columns of real, legible type.

Running this program places the bundled picture at
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png). The picture is
a 1024 by 1024 JPEG under one mebibyte; the file keeps the name
entry.png although its bytes are JPEG, which the rules allow.
"""

from hashlib import sha256
from os import environ, makedirs
from pathlib import Path
from shutil import copyfile

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "frontpage.jpg"
BYTE_LIMIT = 1_048_576
JPEG_START = b"\xff\xd8"


def fingerprint(path):
    """Return the SHA-256 hex digest of the file at path."""
    hasher = sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(65_536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    """Copy the bundled front page to the output directory."""
    picture = PICTURE
    if not picture.is_file():
        raise SystemExit("bundled frontpage.jpg is missing")
    if picture.stat().st_size > BYTE_LIMIT:
        raise SystemExit("bundled frontpage.jpg is over the 1 MiB cap")
    with picture.open("rb") as stream:
        if stream.read(2) != JPEG_START:
            raise SystemExit("bundled frontpage.jpg is not a JPEG")
        stream.seek(-2, 2)
        if stream.read(2) != b"\xff\xd9":
            raise SystemExit("bundled frontpage.jpg has no JPEG end marker")
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    makedirs(out_dir, exist_ok=True)
    target = Path(out_dir) / "entry.png"
    copyfile(picture, target)
    if fingerprint(picture) != fingerprint(target):
        raise SystemExit("entry.png does not match bundled frontpage.jpg")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
