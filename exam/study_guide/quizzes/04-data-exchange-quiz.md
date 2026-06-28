# Data Exchange — Practice Quiz

> Domain 4 of the NVIDIA NCP-OUSD exam blueprint (Exam Weight 15%).
> Questions are written in the style of the official *NVIDIA-Certified Professional: OpenUSD
> Development Exam Study Guide* sample questions, and are grounded in the sources listed under
> "NVIDIA Courses and Suggested Readings" in [`04-data-exchange.md`](../04-data-exchange.md).
> Each question cites its source in the [Rationale & Sources](#rationale--sources) section.

This set covers conceptual and scenario/code-driven items across the eight Data Exchange
objectives: format conversion and trade-offs, packaging, validation, conceptual data mapping,
handling nonstandard data, and writing importers/exporters. Single-choice unless a question says
"Select two/three options."

---

## Question 1
**Domain:** Data Exchange

**Question:** A teammate renames a binary Crate file from `model.usdc` to `model.usd`. When USD opens `model.usd`, how does it determine the file's format?

**Answer Choices:**

- **A.** The `.usd` extension always denotes binary Crate, so it is read as Crate.
- **B.** USD reads the file's header/content to detect whether it is text or Crate; a `.usd` file may be either.
- **C.** It is determined solely by the `USD_DEFAULT_FILE_FORMAT` environment variable.
- **D.** It always defaults to ASCII (`usda`) unless `--usdFormat` is passed.

## Question 2
**Domain:** Data Exchange

**Question:** Your pipeline stores large geometry caches that are opened thousands of times per render but rarely hand-edited. Which layer format is the recommended default, and why?

**Answer Choices:**

- **A.** USDA (text), because text layers load faster than binary.
- **B.** USDC (binary Crate), because it opens faster and consumes substantially less memory while held open.
- **C.** USDA, because only text layers support references and variants.
- **D.** USDC, because text layers cannot store geometry.

## Question 3
**Domain:** Data Exchange

**Question:** You need to convert an ASCII layer `Sphere.usda` into the binary Crate format. Which `usdcat` invocation does this?

**Answer Choices:**

- **A.** `usdcat Sphere.usda`
- **B.** `usdcat -o Sphere.usdc Sphere.usda`
- **C.** `usdcat --flatten Sphere.usda`
- **D.** `usdcat -o Sphere.usda Sphere.usdc`

## Question 4
**Domain:** Data Exchange

**Question:** When is the `--usdFormat usda|usdc` flag to `usdcat` actually necessary?

**Answer Choices:**

- **A.** Whenever you convert between any two formats with `usdcat`.
- **B.** Only when the output filename uses the ambiguous `.usd` extension, since text vs. Crate cannot be inferred from it.
- **C.** Only when flattening composition arcs with `--flatten`.
- **D.** Never — `usdcat` always infers the output format from the input file.

## Question 5
**Domain:** Data Exchange

**Question:** Which of the following statements about the `.usdz` package format are correct? (Select two options.)

**Answer Choices:**

- **A.** A `usdz` package is a zero-compression, unencrypted ZIP archive.
- **B.** The data for each file in the package must begin at a multiple of 64 bytes from the start of the package.
- **C.** `usdz` uses gzip compression to minimize on-disk size.
- **D.** `usdz` packages are encrypted and require a key to unpack.

## Question 6
**Domain:** Data Exchange

**Question:** Your team wants a third-party CAD format to remain the single source of truth, while still letting USD stages reference or payload it directly and letting tools like `usdcat` read it. Which data-exchange implementation accomplishes this?

**Answer Choices:**

- **A.** A standalone one-shot converter that writes a `.usdc` copy.
- **B.** An exporter plugin embedded in the CAD application.
- **C.** A USD File Format Plugin.
- **D.** An importer that reads USD into the CAD application.

## Question 7
**Domain:** Data Exchange

**Question:** A converter you wrote outputs a stage from an OBJ file, but `usdchecker` reports that the asset is not properly interchangeable and the stage cannot be referenced. Which stage-level metadata should an exporter author to address this? (Select three options.)

**Answer Choices:**

- **A.** `upAxis`
- **B.** `metersPerUnit`
- **C.** `defaultPrim`
- **D.** `compressionLevel`
- **E.** `faceVertexCounts`

## Question 8
**Domain:** Data Exchange

**Question:** What does running `usdchecker` on an exported asset verify? (Select two options.)

**Answer Choices:**

- **A.** That the asset is compliant and properly interchangeable.
- **B.** That the asset is renderable by Hydra.
- **C.** That the asset is converted to binary Crate for faster loading.
- **D.** That the asset and its dependencies are packaged into a `usdz`.

## Question 9
**Domain:** Data Exchange

**Question:** What is the primary purpose of authoring a *conceptual data mapping* document before implementing an importer or exporter?

**Answer Choices:**

- **A.** To compress the source data for archival.
- **B.** To plan how source concepts map to USD, quantify feature coverage, and identify gaps that may justify proposing new USD schemas.
- **C.** To define the binary layout of the `.usdc` Crate file.
- **D.** To register the converter as a USD plugin via `plugInfo.json`.

## Question 10
**Domain:** Data Exchange

**Question:** During import, you read a `UsdAttribute` whose full name is `foo:bar:baz`. What does `attr.GetNamespace()` return?

**Answer Choices:**

- **A.** `"baz"`
- **B.** `"foo:bar"`
- **C.** `"foo"`
- **D.** `"foo:bar:baz"`

## Question 11
**Domain:** Data Exchange

**Question:** A source format groups several related fields into a compound "record" for which USD has no native equivalent. What is the conventional way to represent this grouping in USD?

**Answer Choices:**

- **A.** Create a custom C++ struct value type and register it with USD.
- **B.** Store the fields as namespace-prefixed attributes on the prim (e.g., `myData:foo`, `myData:bar`).
- **C.** Encode the entire record as a single JSON string attribute.
- **D.** Add each field as separate stage metadata.

## Question 12
**Domain:** Data Exchange

**Question:** In the Extract phase of an ETL-style data-exchange pipeline, NVIDIA recommends mapping the source data to USD "as directly as possible." Why? (Select two options.)

**Answer Choices:**

- **A.** It preserves fidelity so the USD resembles the source, making the result easier to understand and debug.
- **B.** It simplifies round-tripping the data back to the original format.
- **C.** It guarantees the smallest possible file size.
- **D.** It is required for the stage to be renderable in Hydra.

## Question 13
**Domain:** Data Exchange

**Question:** Your exporter overwrites a `UsdGeomMesh`'s `points` with new positions, but afterward the asset's bounding box is wrong and `usdchecker` flags a bad extent. What is the cause and the correct fix?

**Answer Choices:**

- **A.** The `extent` updates automatically; the stage just needs to be reloaded.
- **B.** The `extent` attribute is not recomputed automatically when `points` change; recompute it (e.g., `UsdGeomBoundable::ComputeExtentFromPlugins`) and re-author it.
- **C.** Editing `points` requires switching the layer to USDA before the bounds refresh.
- **D.** You must delete and recreate the Mesh prim to refresh its bounds.

---

## Answer Key

1. B
2. B
3. B
4. B
5. A, B
6. C
7. A, B, C
8. A, B
9. B
10. B
11. B
12. A, B
13. B

---

## Rationale & Sources

1. **B.** A `.usd` file can be text or Crate; "When USD opens a `.usd` file, it detects the underlying format and handles the file appropriately" — detection is by content, not extension. *(Converting Between Layer Formats; USD FAQ — "What file format is my USD file?")*
2. **B.** "For files that contain more than a few small definitions or overrides, the binary [`usdc`] format will open faster and consume substantially much less memory while held open." USDC is also the default for the `.usd` extension. *(Maximizing USD Performance)*
3. **B.** `usdcat -o NewSphere.usdc Sphere.usda` writes the output to a file whose extension (`.usdc`) selects the Crate format. `-o`/`--out` sets the output file; bare `usdcat` prints to stdout; `--flatten` composes the stage rather than just converting format. *(Converting Between Layer Formats; USD Toolset — usdcat)*
4. **B.** The extension normally determines the format, so `--usdFormat` is only required to disambiguate the format when writing to the ambiguous `.usd` extension. *(Converting Between Layer Formats; USD FAQ)*
5. **A, B.** "A usdz package is a zero compression, unencrypted zip archive," and "the data for each file [must] begin at a multiple of 64 bytes from the beginning of the package" (enabling zero-copy / mmap access). It is therefore neither gzip-compressed nor encrypted. *(USDZ File Format Specification)*
6. **C.** A File Format Plugin lets a USD stage reference/payload/sublayer a source format directly so the source file "can remain the source of truth," and is usable with tools like `usdcat`. Converters/importers/exporters all produce a translated copy instead. *(Learn OpenUSD: Developing Data Exchange Pipelines — "What Is Data Exchange?")*
7. **A, B, C.** Exporters are "strongly encouraged to always set the upAxis for every USD file they create." In the course's validation exercise, `usdchecker` flagged missing `upAxis`, `metersPerUnit`, and `defaultPrim`; a `defaultPrim` is also required before the stage can be referenced. `compressionLevel` is not USD metadata, and `faceVertexCounts` is a per-mesh geometry attribute, not stage metadata. *(Encoding Stage UpAxis; Learn OpenUSD — Asset Validation)*
8. **A, B.** `usdchecker` validates a stage or USDZ package against rules to give assurance the asset is "properly interchangeable and renderable by Hydra." Converting to Crate is `usdcat`'s job; packaging into `usdz` is `usdzip`'s. *(USD Toolset — usdchecker; Learn OpenUSD — Asset Validation)*
9. **B.** A conceptual data mapping document "helps developers reason about data translation choices when mapping between OpenUSD and another data format" — it quantifies feature support, identifies mapping gaps that may justify new USD schemas, and serves as software-design documentation. *(Conceptual Data Mapping)*
10. **B.** `GetNamespace()` returns "this property's complete namespace prefix" with no trailing delimiter — `"foo:bar"`. (`GetBaseName()` would return `"baz"`; `GetName()` the full `"foo:bar:baz"`.) The namespace delimiter is `:`. *(UsdProperty::GetNamespace())*
11. **B.** USD has no native struct/record type, so namespace-prefixed attributes (using the `:` separator) are the convention for grouping related properties together on a prim. *(Learn OpenUSD — Data Exchange; UsdProperty namespacing)*
12. **A, B.** The Extract phase maps source data "as directly as possible" to maintain fidelity — the USD should "look like it did in the source format" to ease understanding/debugging — and this direct mapping is what simplifies round-tripping back to the original format. *(Learn OpenUSD — What Is Data Extraction? / Data Transformation)*
13. **B.** `extent` is local-space bounds cached on `UsdGeomBoundable` and is **not** auto-recomputed when geometry changes; after editing `points` you must recompute it (`ComputeExtentFromPlugins` / `ComputeExtent`) and re-author it, or bounds go stale. *(UsdGeomBoundable — ComputeExtentFromPlugins() / GetExtentAttr())*

---

*Generated from live-fetched source content (PyMuPDF-extracted links → WebFetch). 13 questions; 4 multi-select.*
