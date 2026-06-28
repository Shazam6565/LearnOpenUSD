#!/usr/bin/env python3
"""Render a 'wrong & unsure' remediation review to a Typst PDF in the quiz style.

Reads the enriched review questions (exam/output/_review_wu_<seed>.json) plus per-note
concept files (exam/output/_concepts_*.json) and produces a NVIDIA-styled PDF that, for
each question, marks the correct answer + the student's pick, explains why, and teaches
the underlying concept grounded in the source video notes.
"""
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile, glob
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "templates" / "review.typ"
OUT = HERE / "output"
LETTERS = "ABCDE"


def multi_label(q) -> str:
    if q.get("type") == "multi":
        words = {2: "two", 3: "three", 4: "four"}.get(q.get("select_n", 1), str(q.get("select_n")))
        return f"(Select {words} options.)"
    return ""


def main():
    seed = sys.argv[1] if len(sys.argv) > 1 else "7002"
    items_raw = json.load(open(OUT / f"_review_wu_{seed}.json", encoding="utf-8"))
    concepts = {}
    for f in glob.glob(str(OUT / "_concepts_*.json")):
        concepts.update(json.load(open(f, encoding="utf-8")))

    items = []
    for q in sorted(items_raw, key=lambda x: x["index"]):
        ans = set(q["answer"])
        yours = set(q.get("your_answer") or [])
        choices = []
        for j, text in enumerate(q["choices"]):
            L = LETTERS[j]
            choices.append({"letter": L, "text": text,
                            "correct": L in ans, "yours": L in yours and L not in ans})
        ref = q.get("source_ref") or {}
        items.append({
            "index": q["index"], "domain": q["domain"], "multi_label": multi_label(q),
            "stem": q["stem"], "snippets": q.get("snippets") or [],
            "choices": choices,
            "answer_str": ", ".join(q["answer"]),
            "your_str": ", ".join(q["your_answer"]) if q.get("your_answer") else "(left blank)",
            "explanation": q["explanation"],
            "concept": concepts.get(str(q["index"]), "(concept not available)"),
            "source_title": ref.get("title", ""), "source_url": ref.get("url", ""),
        })

    weak = "Pipeline Development & Debugging and Troubleshooting"
    data = {
        "meta": {"count": len(items), "student": "Shaurya", "quiz": f"Practice Test {seed}",
                 "weak": weak},
        "items": items,
    }

    typst = shutil.which("typst")
    if not typst:
        sys.exit("typst not found. Install: brew install typst")
    out_pdf = OUT / f"quiz-{seed}-wrong-unsure-review.pdf"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        shutil.copy(TEMPLATE, td / "review.typ")
        proc = subprocess.run([typst, "compile", "review.typ", "out.pdf"],
                              cwd=td, capture_output=True, text=True)
        if not (td / "out.pdf").exists():
            sys.exit("typst compile failed:\n" + (proc.stderr or proc.stdout)[-3000:])
        shutil.copy(td / "out.pdf", out_pdf)
    print(f"rendered {len(items)} questions -> {out_pdf}")


if __name__ == "__main__":
    main()
