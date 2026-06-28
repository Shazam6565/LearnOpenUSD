// NCP-OUSD "Wrong & Unsure" Review — Typst template (rendered by exam/render_review.py).
// Reads a sibling data.json. Strings render verbatim (no escaping needed).
#let data = json("data.json")
#let meta = data.meta
#let items = data.items

// NVIDIA palette (matches exam.typ)
#let nvgreen = rgb(118, 185, 0)
#let nvdark = rgb(34, 34, 34)
#let codebg = rgb(242, 242, 242)
#let codegreen = rgb(0, 110, 40)
#let tagslate = rgb(90, 90, 90)
#let linkblue = rgb(40, 90, 160)
#let okgreen = rgb(0, 140, 55)
#let wrongred = rgb(200, 50, 45)
#let boxbg = rgb(247, 250, 242)
#let conceptbg = rgb(244, 247, 251)

#set document(title: "NCP-OUSD Wrong & Unsure Review", author: "LearnOpenUSD")
#set text(font: ("Helvetica Neue", "Arial", "DejaVu Sans"), size: 10pt, fill: nvdark)
#set par(justify: false, leading: 0.62em, spacing: 0.85em)
#show link: set text(fill: linkblue)

#let greenbar = block(fill: nvgreen, height: 6pt, width: 100%)
#let footerline = context [
  #set text(size: 8pt, fill: tagslate)
  #h(1fr) NCP: OpenUSD Development — Wrong & Unsure Review #h(0.5em) | #h(0.5em) #counter(page).display()
]

#set page(paper: "us-letter", margin: (x: 0.9in, top: 1in, bottom: 1in), footer: none)

// ===================== COVER =====================
#greenbar
#v(2.2cm)
#text(size: 9pt, weight: "bold", fill: nvgreen)[NVIDIA-CERTIFIED PROFESSIONAL · TARGETED REVIEW]
#v(0.5cm)
#text(size: 34pt, weight: "bold", fill: nvdark)[OpenUSD Development]
#v(0.1cm)
#text(size: 30pt, weight: "bold", fill: nvdark)[Wrong & Unsure Review]
#v(1.0cm)
#text(size: 13pt, fill: tagslate)[
  #meta.count questions you got wrong AND flagged unsure #h(0.4em) #sym.bullet #h(0.4em) with concepts from the source videos
]
#v(1.3cm)
#table(columns: (4cm, auto), stroke: none, row-gutter: 0.7em, inset: 0pt,
  [*Student*], [#meta.student],
  [*Quiz*], [#meta.quiz],
  [*Selection*], [Questions answered incorrectly that were also flagged "unsure"],
  [*Weak domains*], [#meta.weak],
)
#v(1fr)
#text(size: 9pt, fill: tagslate)[
  Each entry shows the question, marks the correct answer (green check) and your selected answer
  (red cross), explains why, and then teaches the underlying concept grounded in the Learn OpenUSD
  source material. Study the Concept blocks — they are the "why," not just the "what."
]
#v(0.6cm)
#greenbar

#set page(footer: footerline)
#pagebreak()

// ===================== ITEMS =====================
#for q in items {
  block(breakable: true, below: 16pt)[
    #text(size: 13pt, weight: "bold", fill: nvdark)[Question #q.index]
    #h(0.6em) #text(size: 9pt, weight: "bold", fill: nvgreen)[#q.domain]#if q.multi_label != "" [ #h(0.4em) #text(size: 9pt, style: "italic", fill: tagslate)[#q.multi_label]]
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
    #v(6pt)
    // choices with markers
    #for c in q.choices {
      let mark = if c.correct { text(fill: okgreen, weight: "bold")[#sym.checkmark] }
                 else if c.yours { text(fill: wrongred, weight: "bold")[#sym.crossmark] }
                 else { text(fill: tagslate)[#sym.bullet] }
      let label = if c.correct { text(fill: okgreen, weight: "bold")[#c.letter.] }
                  else if c.yours { text(fill: wrongred, weight: "bold")[#c.letter.] }
                  else { text(weight: "bold")[#c.letter.] }
      block(below: 3pt)[#box(width: 1.1em)[#mark] #label #h(0.2em) #c.text]
    }
    #v(7pt)
    // verdict line
    #block(fill: boxbg, inset: 9pt, radius: 3pt, width: 100%)[
      #text(fill: okgreen, weight: "bold")[Correct: #q.answer_str]
      #h(1.2em) #text(fill: wrongred)[Your answer: #q.your_str]
      #v(4pt)
      #text(size: 9.5pt)[#text(weight: "bold")[Why: ] #q.explanation]
    ]
    #v(5pt)
    #block(fill: conceptbg, inset: 9pt, radius: 3pt, width: 100%)[
      #text(size: 9pt, weight: "bold", fill: linkblue)[Concept — from the source]
      #v(3pt)
      #text(size: 9.5pt)[#q.concept]
    ]
    #if q.source_url != "" {
      v(3pt)
      text(size: 8.5pt, fill: tagslate)[*Source:* #q.source_title — #link(q.source_url)[#q.source_url]]
    }
  ]
  line(length: 100%, stroke: 0.4pt + rgb(220,220,220))
}
