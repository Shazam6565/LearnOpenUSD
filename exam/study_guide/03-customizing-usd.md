# Customizing USD — Exam Weight 6%

> Domain 3 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

Understand USD plugin development to extend USD's functionality, including the creation of custom
schemas, file format plugins, custom model kinds, and variant fallback selections.

## Exam Objectives

- **3.1** Build a USD plug-in against a given version of USD.
- **3.2** Build USD from scratch with custom dependencies.
- **3.3** Create custom model kinds when appropriate.
- **3.4** Create custom schemas for proprietary data models.
- **3.5** Integrate a custom resolver to manage asset paths dynamically.
- **3.6** Use USD schemas to support nonstandard attributes/structures during import/export.
- **3.7** Write a SceneIndex plug-in to generate renderable geometry directly as Hydra prims.
- **3.8** Write an AssetResolver that generates in-memory renderable primitives.

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Understanding Model Kinds](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/model-kinds.html)

### Tutorials
- [Generating New Schema Classes](https://openusd.org/release/tut_generating_new_schema.html)

### Glossary
- [Model Hierarchy](https://openusd.org/release/glossary.html#usdglossary-modelhierarchy)

### Whitepapers and Blogs
- [What Are OpenUSD Schemas?](https://aousd.org/blog/explainer-series-for-developers-what-are-openusd-schemas/)

### Videos
- [Universal Scene Description (OpenUSD): Custom Schemas](https://www.youtube.com/watch?v=-iCUjNk2aiA)
- [USD in Production](https://dl.acm.org/doi/10.1145/3587423.3595531)

### Technical Reference
- [USD FAQ - Isn't USD Just Another File Format?](https://dl.acm.org/doi/10.1145/3587423.3595531)

### API Docs
- [Creating a File Format Plug-in](https://openusd.org/release/api/_sdf__page__file_format_plugin.html)
- [Creating New Schema Classes With usdGenSchema](https://openusd.org/release/api/_usd__page__generating_schemas.html)
- [Kind: Extensible Categorization](https://openusd.org/release/api/kind_page_front.html)
- [PlugRegistry - Registering Plug-ins](https://openusd.org/release/api/class_plug_registry.html#plug_RegisteringPlugins)
- [Ar: Asset Resolution](https://openusd.org/release/api/ar_page_front.html)

---

> **Source-link note:** in the official PDF, the "USD FAQ - Isn't USD Just Another File Format?"
> entry links to the same ACM DOI as "USD in Production" (`dl.acm.org/doi/10.1145/3587423.3595531`)
> — an apparent copy-paste in NVIDIA's document. The link is reproduced here as published; the
> canonical USD FAQ lives at <https://openusd.org/release/usdfaq.html>.
