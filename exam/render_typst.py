#!/usr/bin/env python3
"""Render an NCP-OUSD practice test to PDF with Typst (no LaTeX required).

A drop-in alternative to generate_quiz.py's pdflatex path: produces the same NVIDIA-styled
layout, with clickable source links, via the `typst` binary (brew install typst). Reuses
generate_quiz.py's question selection / answer-balancing so output is identical in content.

Examples
--------
    uv run python exam/render_typst.py                          # 60-Q weighted sample
    uv run python exam/render_typst.py --count 30 --difficulty hard
    uv run python exam/render_typst.py --from exam/output/quiz-4217.json --seed 4217
    uv run python exam/render_typst.py --domain Composition --count 15 --md
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import generate_quiz as g  # selection, balancing, markdown, guidelines

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "templates" / "exam.typ"
OUTPUT_DIR = HERE / "output"
SMAP_PATH = HERE / "source_map.json"


def plain_snippet(s) -> dict:
    """Coerce a snippet into {filename, code} with NO LaTeX escaping (Typst is verbatim)."""
    if isinstance(s, dict) and "code" in s:
        code = s["code"]
        fn = s.get("filename") or ("example.py" if any(h in code for h in g._PY_HINTS) else "example.usda")
        return {"filename": fn, "code": code}
    code = s if isinstance(s, str) else str(s)
    fn = "example.py" if any(h in code for h in g._PY_HINTS) else "example.usda"
    return {"filename": fn, "code": code}


def question_vm(q: dict, i: int) -> dict:
    """Template view-model for one question — raw strings, Typst handles the rest."""
    ref = q.get("source_ref") or {}
    select_n = q.get("select_n", 1)
    multi_label = ""
    if q["type"] == "multi":
        words = {2: "two", 3: "three", 4: "four"}.get(select_n, str(select_n))
        multi_label = f"(Select {words} options.)"
    return {
        "index": i,
        "domain": q["domain"],
        "objective": q["objective"],
        "multi_label": multi_label,
        "stem": q["stem"],
        "snippets": [plain_snippet(s) for s in (q.get("snippets") or [])],
        "choices": list(q["choices"]),
        "answer_str": ", ".join(q["answer"]),
        "explanation": q["explanation"],
        "source_title": ref.get("title", ""),
        "source_url": ref.get("url", ""),
    }


def distribution_str(questions: list[dict]) -> str:
    from collections import Counter
    c = Counter(q["domain"] for q in questions)
    parts = [f"{d} {c[d]}" for d in g.DOMAIN_WEIGHTS if c.get(d)]
    extra = [f"{d} {c[d]}" for d in c if d not in g.DOMAIN_WEIGHTS]
    return " · ".join(parts + extra)


def build_data(questions: list[dict], args, seed: int) -> dict:
    meta = {
        "count": len(questions),
        "minutes": g.EXAM_MINUTES,
        "difficulty": args.difficulty.capitalize(),
        "seed": seed,
        "domain_focus": args.domain or "",
        "passing_target": "70% or higher",
        "distribution": distribution_str(questions),
        "official_note": (
            f"Real exam: {g.COUNT_MIN}-{g.COUNT_MAX} questions, {g.EXAM_MINUTES} min, "
            f"{g.GUIDELINES.get('level', 'Professional')} level. Weighting follows the official "
            f"NVIDIA blueprint."
        ),
    }
    return {
        "meta": meta,
        "with_answers": not args.no_answers,
        "questions": [question_vm(q, i) for i, q in enumerate(questions, 1)],
    }


def compile_pdf(data: dict, out_pdf: Path) -> None:
    typst = shutil.which("typst")
    if not typst:
        sys.exit("typst not found. Install it: brew install typst")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        shutil.copy(TEMPLATE, td / "exam.typ")
        proc = subprocess.run([typst, "compile", "exam.typ", "out.pdf"],
                              cwd=td, capture_output=True, text=True)
        built = td / "out.pdf"
        if not built.exists():
            sys.exit("typst compile failed:\n" + (proc.stderr or proc.stdout)[-3000:])
        shutil.copy(built, out_pdf)


def resolve_sources(questions: list[dict]) -> list[dict]:
    """Fill missing source_ref from source_map.json; drop questions with no primary source."""
    smap = json.load(open(SMAP_PATH, encoding="utf-8")) if SMAP_PATH.exists() else {}
    for q in questions:
        if not (q.get("source_ref") or {}).get("url") and q.get("source") in smap:
            q["source_ref"] = smap[q["source"]]
    unsourced = [q.get("id", "?") for q in questions if not (q.get("source_ref") or {}).get("url")]
    if unsourced:
        print(f"note: skipping {len(unsourced)} unsourced question(s): "
              f"{', '.join(unsourced[:10])}{'…' if len(unsourced) > 10 else ''}", file=sys.stderr)
    return [q for q in questions if (q.get("source_ref") or {}).get("url")]


def main() -> None:
    p = argparse.ArgumentParser(description="Render an NCP-OUSD practice test to PDF via Typst.")
    p.add_argument("--count", type=int, default=60)
    p.add_argument("--difficulty", choices=["mixed", "medium", "hard"], default="mixed")
    p.add_argument("--domain", default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--no-answers", action="store_true")
    p.add_argument("--md", action="store_true", help="also write a Markdown sidecar")
    p.add_argument("--dump-json", default=None,
                   help="write the exact rendered question set (post-balance) to this JSON path")
    p.add_argument("--out", default=None, help="output PDF path")
    p.add_argument("--from", dest="from_json", default=None,
                   help="render a pre-built ordered quiz JSON (list of question objects)")
    args = p.parse_args()

    if args.from_json:
        src = Path(args.from_json)
        if not src.exists():
            sys.exit(f"--from file not found: {src}")
        questions = json.load(open(src, encoding="utf-8"))
        if not isinstance(questions, list) or not questions:
            sys.exit(f"--from must be a non-empty JSON list: {src}")
        seed = args.seed if args.seed is not None else 0
        questions = resolve_sources(questions)
        questions = g.balance_answers(questions, seed)
        default_pdf = OUTPUT_DIR / f"{src.stem}.pdf"
    else:
        bank = json.load(open(g.BANK_PATH, encoding="utf-8"))
        bank = resolve_sources(bank)
        seed = args.seed if args.seed is not None else random.randint(1000, 999999)
        rng = random.Random(seed)
        questions = g.select_questions(bank, args.count, args.difficulty, args.domain, rng)
        if not questions:
            sys.exit("No questions selected.")
        questions = g.balance_answers(questions, seed)
        default_pdf = OUTPUT_DIR / f"ncp-ousd-practice-test-{seed}.pdf"

    out_pdf = (Path(args.out) if args.out else default_pdf).resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    if args.dump_json:
        dump_path = Path(args.dump_json).resolve()
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(questions, open(dump_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"JSON: {dump_path}")

    data = build_data(questions, args, seed)
    compile_pdf(data, out_pdf)

    from collections import Counter
    dist = Counter(q["domain"] for q in questions)
    print(f"Rendered {len(questions)} questions (seed={seed}, difficulty={args.difficulty}"
          + (f", domain={args.domain}" if args.domain else "") + ")")
    for d in sorted(dist, key=lambda x: -dist[x]):
        print(f"  {dist[d]:3d}  {d}")
    print(f"answer spread (single): {dict(g._single_letter_dist(questions))}")
    print(f"PDF: {out_pdf}")

    if args.md:
        out_md = out_pdf.with_suffix(".md")
        g.write_markdown(questions, out_md, not args.no_answers)
        print(f"MD:  {out_md}")


if __name__ == "__main__":
    main()
