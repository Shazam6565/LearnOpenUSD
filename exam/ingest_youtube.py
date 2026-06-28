#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["youtube-transcript-api>=1.1"]
# ///
"""Ingest YouTube video transcripts as grounding sources for /generate-quiz.

This adapts the transcript->markdown logic from microsoft/markitdown's YouTube
converter (MIT) into the shape the quiz pipeline already expects: a plain-text
corpus file the author/verifier sub-agents can grep, plus a source_map.json entry
so generated questions can cite the video.

For each video it:
  1. fetches the transcript via youtube-transcript-api (markitdown's approach),
  2. fetches the title via YouTube's keyless oEmbed endpoint,
  3. writes the transcript to exam/_verification/pages/<key> (the grounding corpus),
  4. adds/updates an entry in exam/source_map.json: <key> -> {title, url}.

After ingesting, run /generate-quiz unchanged; it will ground new questions in
these transcripts alongside the existing NVIDIA docs sources (additive).

Usage (run from repo root, LearnOpenUSD/):
  uv run python exam/ingest_youtube.py https://www.youtube.com/watch?v=VIDEO_ID [more URLs...]
  uv run python exam/ingest_youtube.py VIDEO_ID --lang en          # bare id also works
  uv run python exam/ingest_youtube.py URL --list                  # just list available transcripts
  uv run python exam/ingest_youtube.py URL --dry-run               # don't write anything
  # API blocked? paste a transcript you exported yourself:
  uv run python exam/ingest_youtube.py URL --from-file transcript.txt --title "My Title"

Notes:
  - youtube-transcript-api scrapes YouTube and is frequently rate-limited / IP-blocked
    (especially from cloud IPs) and only works on videos that actually have captions.
    On a hard block, use --from-file to ingest a manually exported transcript.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
SMAP = HERE / "source_map.json"
PAGES = HERE / "_verification" / "pages"
KEY_PREFIX = "yt"
RETRIES = 3
RETRY_WAIT = 2.0
UA = "Mozilla/5.0 (compatible; quiz-openusd ingest_youtube/1.0)"


# ---------------------------------------------------------------- url / id parsing
def extract_video_id(s: str) -> str | None:
    """Accept a watch URL, youtu.be/embed/shorts URL, or a bare 11-char video id."""
    s = s.strip()
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", s):
        return s
    try:
        u = urlparse(s if "//" in s else "https://" + s)
    except ValueError:
        return None
    host = (u.hostname or "").lower().removeprefix("www.")
    if host == "youtu.be":
        vid = u.path.lstrip("/").split("/")[0]
        return vid if re.fullmatch(r"[0-9A-Za-z_-]{11}", vid) else None
    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        q = parse_qs(u.query)
        if "v" in q and re.fullmatch(r"[0-9A-Za-z_-]{11}", q["v"][0]):
            return q["v"][0]
        m = re.match(r"/(?:embed|shorts|v|live)/([0-9A-Za-z_-]{11})", u.path)
        if m:
            return m.group(1)
    return None


def watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def scrape_playlist_video_ids(url: str) -> list[str]:
    """Best-effort: pull ordered, de-duplicated video ids out of a public playlist page.

    No API key and no extra deps, but fragile (depends on YouTube's page markup). If it
    returns nothing, pass the individual video URLs instead.
    """
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print(f"  ! could not fetch playlist page: {e}", file=sys.stderr)
        return []
    seen, out = set(), []
    for m in re.finditer(r'"videoId":"([0-9A-Za-z_-]{11})"', html):
        vid = m.group(1)
        if vid not in seen:
            seen.add(vid)
            out.append(vid)
    return out


# ---------------------------------------------------------------- metadata (oembed)
def fetch_title(video_id: str) -> str:
    """Keyless title lookup via YouTube oEmbed; falls back to a generic label."""
    url = f"https://www.youtube.com/oembed?url={watch_url(video_id)}&format=json"
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=20) as resp:
            data = json.load(resp)
        title = (data.get("title") or "").strip()
        author = (data.get("author_name") or "").strip()
        if title:
            return f"{title} — {author}" if author else title
    except Exception as e:  # noqa: BLE001
        print(f"  ! oEmbed title lookup failed ({e}); using generic title", file=sys.stderr)
    return f"YouTube Video {video_id}"


# ---------------------------------------------------------------- transcript fetch
def _segments_text(segments) -> str:
    """Join transcript snippets (objects in API >=1.x, dicts in legacy) into prose."""
    parts = []
    for s in segments:
        t = getattr(s, "text", None)
        if t is None and isinstance(s, dict):
            t = s.get("text", "")
        t = (t or "").replace("\n", " ").strip()
        if t:
            parts.append(t)
    return " ".join(parts)


def fetch_transcript(video_id: str, languages: list[str]) -> tuple[str, list[str]]:
    """Return (transcript_text, languages_available). Tries the 1.x instance API first,
    then the legacy static API, with markitdown-style retries on transient errors."""
    from youtube_transcript_api import YouTubeTranscriptApi

    last_err: Exception | None = None
    for attempt in range(RETRIES):
        try:
            if hasattr(YouTubeTranscriptApi, "fetch"):  # >= 1.x instance API
                api = YouTubeTranscriptApi()
                avail = []
                try:
                    avail = [f"{t.language_code}{'(auto)' if t.is_generated else ''}"
                             for t in api.list(video_id)]
                except Exception:  # noqa: BLE001 -- listing is best-effort only
                    pass
                fetched = api.fetch(video_id, languages=languages) if languages else api.fetch(video_id)
                return _segments_text(fetched), avail
            # legacy 0.6.x static API
            avail = []
            try:
                avail = [f"{t.language_code}{'(auto)' if t.is_generated else ''}"
                         for t in YouTubeTranscriptApi.list_transcripts(video_id)]
            except Exception:  # noqa: BLE001
                pass
            segs = YouTubeTranscriptApi.get_transcript(video_id, languages=languages or ["en"])
            return _segments_text(segs), avail
        except Exception as e:  # noqa: BLE001
            last_err = e
            name = type(e).__name__
            # Don't burn retries on definitive "no transcript here" errors.
            if name in ("TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable",
                        "NotTranslatable", "NoTranscriptAvailable"):
                break
            if attempt < RETRIES - 1:
                print(f"  … transcript fetch failed ({name}); retrying in {RETRY_WAIT}s", file=sys.stderr)
                time.sleep(RETRY_WAIT)
    raise RuntimeError(f"could not fetch transcript for {video_id}: "
                       f"{type(last_err).__name__}: {last_err}") from last_err


def list_only(video_id: str) -> int:
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        api = YouTubeTranscriptApi()
        tl = api.list(video_id) if hasattr(api, "list") else YouTubeTranscriptApi.list_transcripts(video_id)
        print(f"{video_id}: available transcripts:")
        for t in tl:
            kind = "auto-generated" if t.is_generated else "manual"
            print(f"  - {t.language_code:8} {kind:14} {t.language}")
        return 0
    except Exception as e:  # noqa: BLE001
        print(f"{video_id}: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------- corpus + source map
def corpus_body(title: str, url: str, transcript: str) -> str:
    """Plain-text corpus file (light header the grep-based authoring step can read)."""
    return (f"# {title}\n\n"
            f"Source: {url}\n"
            f"Type: YouTube video transcript\n\n"
            f"## Transcript\n\n{transcript}\n")


def ingest(video_id: str, *, languages: list[str], dry_run: bool,
           transcript_override: str | None, title_override: str | None) -> dict | None:
    url = watch_url(video_id)
    key = f"{KEY_PREFIX}__{video_id}.txt"

    if transcript_override is not None:
        transcript, avail = transcript_override, ["(provided via --from-file)"]
    else:
        transcript, avail = fetch_transcript(video_id, languages)
    if not transcript.strip():
        print(f"  ! empty transcript for {video_id}; skipping", file=sys.stderr)
        return None

    title = title_override or fetch_title(video_id)
    body = corpus_body(title, url, transcript)
    words = len(transcript.split())
    print(f"  ok  {key}  ({words} words; transcripts: {', '.join(avail) or 'n/a'})")

    if dry_run:
        print(f"  [dry-run] would write {PAGES / key} and source_map['{key}']")
        return {"key": key, "title": title, "url": url, "words": words}

    PAGES.mkdir(parents=True, exist_ok=True)
    (PAGES / key).write_text(body, encoding="utf-8")
    return {"key": key, "title": title, "url": url, "words": words}


def update_source_map(entries: list[dict]) -> None:
    smap = json.loads(SMAP.read_text(encoding="utf-8")) if SMAP.exists() else {}
    for e in entries:
        smap[e["key"]] = {"title": e["title"], "url": e["url"]}
    SMAP.write_text(json.dumps(smap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- cli
def main() -> int:
    p = argparse.ArgumentParser(description="Ingest YouTube transcripts as /generate-quiz sources.")
    p.add_argument("inputs", nargs="+", help="video URL(s), youtu.be/embed/shorts URL(s), bare video id(s), or a playlist URL")
    p.add_argument("--lang", default="en",
                   help="preferred transcript language codes, comma-separated (default: en). "
                        "First available wins; the library will fall back to generated captions.")
    p.add_argument("--playlist", action="store_true",
                   help="treat each input as a playlist URL and scrape its video ids (best-effort)")
    p.add_argument("--list", action="store_true", help="only list available transcripts; write nothing")
    p.add_argument("--dry-run", action="store_true", help="fetch + report but do not write files")
    p.add_argument("--from-file", default=None,
                   help="ingest a pasted/exported transcript from this text file instead of "
                        "calling the API (use when YouTube blocks the request). Single input only.")
    p.add_argument("--title", default=None, help="override the video title (recommended with --from-file)")
    a = p.parse_args()

    languages = [s.strip() for s in a.lang.split(",") if s.strip()]

    # Resolve inputs -> ordered, de-duplicated list of video ids.
    video_ids: list[str] = []
    for item in a.inputs:
        if a.playlist:
            ids = scrape_playlist_video_ids(item)
            if not ids:
                print(f"no video ids scraped from playlist: {item}", file=sys.stderr)
            video_ids += ids
            continue
        vid = extract_video_id(item)
        if not vid:
            print(f"could not parse a video id from: {item!r}", file=sys.stderr)
            continue
        video_ids.append(vid)
    # de-dup, preserve order
    video_ids = list(dict.fromkeys(video_ids))
    if not video_ids:
        print("no valid video ids to process.", file=sys.stderr)
        return 2

    if a.from_file is not None and len(video_ids) != 1:
        print("--from-file works with exactly one video input.", file=sys.stderr)
        return 2

    if a.list:
        rc = 0
        for vid in video_ids:
            rc |= list_only(vid)
        return rc

    override = None
    if a.from_file is not None:
        override = Path(a.from_file).read_text(encoding="utf-8").strip()

    entries, failures = [], 0
    for vid in video_ids:
        print(f"- {vid}")
        try:
            e = ingest(vid, languages=languages, dry_run=a.dry_run,
                       transcript_override=override, title_override=a.title)
            if e:
                entries.append(e)
            else:
                failures += 1
        except Exception as ex:  # noqa: BLE001
            failures += 1
            print(f"  FAIL {vid}: {ex}", file=sys.stderr)

    if entries and not a.dry_run:
        update_source_map(entries)
        print(f"\nupdated {SMAP.name}: +{len(entries)} source(s)")
        print("corpus written under:", PAGES)
        print("source keys:", ", ".join(e["key"] for e in entries))
        print("\nNext: run /generate-quiz — it will ground new questions in these transcripts too.")
    elif a.dry_run:
        print(f"\n[dry-run] {len(entries)} source(s) would be added; nothing written.")

    if failures:
        print(f"\n{failures} input(s) failed.", file=sys.stderr)
    return 1 if failures and not entries else 0


if __name__ == "__main__":
    raise SystemExit(main())
