"""Prepare DGPE-deck-v2.pptx for import into Google Vids.

Google Vids builds each scene's script from the slide's speaker notes. The v2
deck's notes are production annotations ("3:58 CLIP 12-drc-drilldown.mp4 (28s)",
"slow down here", "first cut if trimming"), so importing it as-is makes the
generated voiceover read timecodes and filenames aloud.

This splits every slide's notes into the annotation and the narration, writes a
deck whose notes hold narration only, and saves the stripped annotations to a
CSV so the deck-to-video mapping survives.

Run it on the machine that has the zip (WSL):

    python3 build_dgpe_vids_ready.py
    python3 build_dgpe_vids_ready.py --deck-zip ~/Downloads/deck.zip --dry-run

Then upload the resulting DGPE.pptx to Drive, open it in Slides, and use
File > Convert to video.
"""

import argparse
import csv
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from pptx import Presentation
except ImportError:
    sys.exit("python-pptx is required: pip install python-pptx")

WINDOWS_USER = "sheke"
SEARCH_DIRS = [
    Path(f"/mnt/c/Users/{WINDOWS_USER}/Downloads"),
    Path(f"/mnt/c/Users/{WINDOWS_USER}/OneDrive/Desktop"),
    Path.home() / "Downloads",
    Path.cwd(),
]
DEFAULT_OUT_DIR = Path(f"/mnt/c/Users/{WINDOWS_USER}/OneDrive/Desktop")

# "3:58 · CLIP 12-drc-drilldown.mp4 (28s)" and the looser variants of it that
# show up when the separator or the duration is missing.
ANNOTATION = re.compile(
    r"""^\s*
    (?:(?P<timecode>\d{1,2}:\d{2})\s*[·\-–|]*\s*)?
    (?:CLIP\s*)?
    (?P<clip>[\w\-.]+\.mp4)
    \s*(?:\(\s*(?P<seconds>\d+)\s*s\s*\))?
    \s*$""",
    re.IGNORECASE | re.VERBOSE,
)
BARE_TIMECODE = re.compile(r"^\s*\d{1,2}:\d{2}\s*[·\-–|]?\s*$")

# Editing direction rather than narration. Reading these aloud is as wrong as
# reading the timecodes, but they are prose and cannot be matched as reliably,
# so they are flagged by default and only removed with --strip-direction.
DIRECTION = re.compile(
    r"slow down|speed up|first cut|trim|cut this|payoff to|callback to|hold on"
    r"|linger|b-roll|cursor (?:does ?n[o']t|never)|note:|todo|reshoot|retake",
    re.IGNORECASE,
)


def find_deck_zip(explicit):
    if explicit:
        path = Path(explicit).expanduser()
        if not path.exists():
            sys.exit(f"No such file: {path}")
        return path
    candidates = []
    for directory in SEARCH_DIRS:
        if directory.is_dir():
            candidates.extend(directory.glob("*.zip"))
    for candidate in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True):
        with zipfile.ZipFile(candidate) as archive:
            if any(n.lower().endswith(".pptx") for n in archive.namelist()):
                return candidate
    sys.exit(
        "Could not find a zip containing a .pptx. Pass one with --deck-zip.\n"
        "Looked in: " + ", ".join(str(d) for d in SEARCH_DIRS)
    )


def extract_pptx(zip_path, workdir):
    with zipfile.ZipFile(zip_path) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith(".pptx")]
        if not names:
            sys.exit(f"{zip_path} contains no .pptx")
        if len(names) > 1:
            preferred = [n for n in names if "deck" in n.lower()]
            names = preferred or names
        archive.extract(names[0], workdir)
        return Path(workdir) / names[0]


def split_notes(text, strip_direction=False):
    """Return (narration, annotations, direction) from one slide's notes."""
    narration, annotations, direction = [], [], []
    for line in text.splitlines():
        if not line.strip():
            continue
        if ANNOTATION.match(line) or BARE_TIMECODE.match(line):
            annotations.append(line.strip())
        elif DIRECTION.search(line):
            direction.append(line.strip())
            if not strip_direction:
                narration.append(line.rstrip())
        else:
            narration.append(line.rstrip())
    return "\n".join(narration).strip(), annotations, direction


def parse_annotation(lines):
    timecode = clip = seconds = ""
    for line in lines:
        match = ANNOTATION.match(line)
        if match:
            timecode = match.group("timecode") or timecode
            clip = match.group("clip") or clip
            seconds = match.group("seconds") or seconds
    return timecode, clip, seconds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck-zip", help="zip holding DGPE-deck-v2.pptx")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--name", default="DGPE", help="output basename")
    parser.add_argument("--dry-run", action="store_true", help="report only")
    parser.add_argument(
        "--strip-direction",
        action="store_true",
        help="also remove editing direction, not just timecodes",
    )
    parser.add_argument(
        "--clear-notes",
        action="store_true",
        help="empty every note so Vids writes all scripts from slide content",
    )
    args = parser.parse_args()

    zip_path = find_deck_zip(args.deck_zip)
    print(f"Deck archive: {zip_path}")

    workdir = tempfile.mkdtemp(prefix="dgpe-")
    try:
        pptx_path = extract_pptx(zip_path, workdir)
        print(f"Extracted:    {pptx_path.name}")

        presentation = Presentation(pptx_path)
        rows, empty_slides, flagged_slides = [], [], []

        for index, slide in enumerate(presentation.slides, start=1):
            if not slide.has_notes_slide:
                rows.append((index, "", "", "", "", "", ""))
                empty_slides.append(index)
                continue

            frame = slide.notes_slide.notes_text_frame
            narration, annotations, direction = split_notes(frame.text, args.strip_direction)
            if args.clear_notes:
                narration = ""
            timecode, clip, seconds = parse_annotation(annotations)
            rows.append((
                index,
                timecode,
                clip,
                seconds,
                " / ".join(annotations),
                " / ".join(direction),
                narration,
            ))

            if not narration:
                empty_slides.append(index)
            if direction and not (args.strip_direction or args.clear_notes):
                flagged_slides.append(index)
            if not args.dry_run:
                frame.text = narration

            label = f"{timecode} {clip}".strip() or "(no clip annotation)"
            summary = narration.replace("\n", " ")[:58] or "*** NO NARRATION ***"
            mark = "!" if index in flagged_slides else " "
            print(f" {mark}slide {index:>2}  {label:<34}  {summary}")

        out_dir = Path(args.out_dir).expanduser()
        if not out_dir.is_dir():
            print(f"\n{out_dir} is not a directory; writing beside the zip instead.")
            out_dir = zip_path.parent

        csv_path = out_dir / f"{args.name}-timecode-map.csv"
        pptx_out = out_dir / f"{args.name}.pptx"

        if args.dry_run:
            print(f"\nDry run: would write {pptx_out} and {csv_path}")
            return

        presentation.save(pptx_out)
        with open(csv_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["slide", "timecode", "clip", "seconds", "annotation", "direction", "narration"]
            )
            writer.writerows(rows)

        print(f"\nWrote {pptx_out}")
        print(f"Wrote {csv_path}")
        if flagged_slides:
            print(
                "\nSlides whose notes still read as direction rather than narration: "
                + ", ".join(str(n) for n in flagged_slides)
                + "\nRerun with --strip-direction to drop those lines too, or edit"
                " their scripts in the Vids import preview."
            )
        if empty_slides:
            print(
                "\nSlides with no narration left: "
                + ", ".join(str(n) for n in empty_slides)
                + "\nLeave Gemini's generated script on these rather than replacing"
                " them with speaker notes."
            )
        print(
            "\nNext: upload to Drive, open in Slides, File > Convert to video.\n"
            "Keep 'Include AI voiceover, script, background music and animation'"
            " on, and review each script in the import preview."
        )
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
