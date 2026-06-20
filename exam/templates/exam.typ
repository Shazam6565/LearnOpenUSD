// NCP-OUSD Practice Test — Typst template (rendered by exam/render_typst.py).
// Reads a sibling data.json (written by the renderer) so question text needs no escaping:
// Typst renders string values verbatim, unlike LaTeX.
#let data = json("data.json")
#let meta = data.meta
#let questions = data.questions
#let with-answers = data.with_answers

// NVIDIA palette (matches the LaTeX template)
#let nvgreen = rgb(118, 185, 0)
#let nvdark = rgb(34, 34, 34)
#let codebg = rgb(242, 242, 242)
#let codegreen = rgb(0, 110, 40)
#let tagslate = rgb(90, 90, 90)
#let linkblue = rgb(40, 90, 160)

#set document(title: "NCP-OUSD Practice Test", author: "LearnOpenUSD")
#set text(font: ("Helvetica Neue", "Arial", "DejaVu Sans"), size: 10pt, fill: nvdark)
#set par(justify: false, leading: 0.62em, spacing: 0.85em)
#show link: set text(fill: linkblue)

#let greenbar = block(fill: nvgreen, height: 6pt, width: 100%)
#let footerline = context [
  #set text(size: 8pt, fill: tagslate)
  #h(1fr) NCP: OpenUSD Development — Practice Test #h(0.5em) | #h(0.5em) #counter(page).display()
]

// Cover page carries no footer; content pages do.
#set page(paper: "us-letter", margin: (x: 0.9in, top: 1in, bottom: 1in), footer: none)

// ===================== COVER =====================
#greenbar
#v(2.2cm)
#text(size: 9pt, weight: "bold", fill: nvgreen)[NVIDIA-CERTIFIED PROFESSIONAL]
#v(0.5cm)
#text(size: 34pt, weight: "bold", fill: nvdark)[OpenUSD Development]
#v(0.1cm)
#text(size: 34pt, weight: "bold", fill: nvdark)[Practice Test]
#v(1.0cm)
#text(size: 13pt, fill: tagslate)[
  #meta.count questions #h(0.5em) #sym.bullet #h(0.5em) #meta.minutes minutes #h(0.5em) #sym.bullet #h(0.5em) weighted by official exam domains
]
#v(1.3cm)
#let info-rows = {
  let r = (
    ([*Difficulty*], [#meta.difficulty]),
    ([*Seed*], [#meta.seed (reproducible)]),
  )
  if meta.domain_focus != "" { r.push(([*Focus domain*], [#meta.domain_focus])) }
  r.push(([*Passing target*], [#meta.passing_target]))
  r
}
#table(columns: (4cm, auto), stroke: none, row-gutter: 0.7em, inset: 0pt, ..info-rows.flatten())
#v(1fr)
#text(size: 9pt, fill: tagslate)[
  This practice test mirrors the question style, multi-select format, and domain weighting of the
  official NVIDIA-Certified Professional: OpenUSD Development exam. Questions and answer key are
  generated from a curated bank grounded in the Learn OpenUSD curriculum. Not affiliated with or
  endorsed by NVIDIA; for study use only.
]
#v(0.6cm)
#greenbar

#set page(footer: footerline)
#pagebreak()

// ===================== INSTRUCTIONS =====================
#text(size: 17pt, weight: "bold", fill: nvdark)[Instructions]
#v(0.3cm)
This test contains *#meta.count questions* distributed across the eight exam domains by their official
weighting. Each question is single-choice (choose one) unless it is explicitly marked _(Select two
options.)_ or _(Select three options.)_, in which case you must select exactly that many answers for
credit. Code questions present one or more USDA layers; reason through composition using *LIVERPS*
strength order (Local, Inherits, Variants, rElocates, References, Payloads, Specializes). The *Answer
Key & Explanations* section begins after the final question.
#v(0.3cm)
#text(size: 9.5pt)[*Domain distribution:* #meta.distribution]
#v(0.2cm)
#text(size: 9pt, fill: tagslate)[#meta.official_note]
#pagebreak()

// ===================== QUESTIONS =====================
#for q in questions {
  block(breakable: true, below: 14pt)[
    #text(size: 13pt, weight: "bold", fill: nvdark)[Question #q.index]
    #v(3pt)
    #text(size: 9.5pt)[#text(weight: "bold", fill: nvgreen)[Domain:] #text(weight: "bold")[#q.domain]]#if q.multi_label != "" [ #h(0.5em) #text(size: 9pt, style: "italic", fill: tagslate)[#q.multi_label]]
    #v(5pt)
    #q.stem
    #for s in q.snippets {
      v(5pt)
      text(size: 8.5pt, style: "italic", fill: tagslate)[#s.filename]
      v(2pt)
      block(fill: codebg, inset: 8pt, radius: 2pt, width: 100%, breakable: false)[
        #set text(font: ("Menlo", "DejaVu Sans Mono", "Courier New"), size: 8.5pt, fill: codegreen)
        #raw(s.code, block: true)
      ]
    }
    #v(5pt)
    #enum(
      numbering: n => text(weight: "bold")[#numbering("A.", n)],
      indent: 0.4em,
      body-indent: 0.5em,
      spacing: 4pt,
      ..q.choices
    )
    #if q.source_url != "" {
      v(3pt)
      text(size: 8.5pt, fill: tagslate)[*Source:* #q.source_title — #link(q.source_url)[#q.source_url]]
    }
  ]
}

// ===================== ANSWER KEY =====================
#if with-answers {
  pagebreak()
  text(size: 17pt, weight: "bold", fill: nvdark)[Answer Key & Explanations]
  v(0.3cm)
  let i = 0
  for q in questions {
    i = i + 1
    block(breakable: true, below: 9pt)[
      #text(weight: "bold")[#(str(i) + ". Answer: " + q.answer_str)] #h(0.5em) #text(size: 9pt, fill: tagslate)[\[#q.domain #sym.bullet obj #q.objective\]]
      #linebreak()
      #text(size: 9.5pt)[#q.explanation]
      #if q.source_url != "" {
        linebreak()
        text(size: 8.5pt, fill: tagslate)[*Source:* #q.source_title — #link(q.source_url)[#q.source_url]]
      }
    ]
  }
}
