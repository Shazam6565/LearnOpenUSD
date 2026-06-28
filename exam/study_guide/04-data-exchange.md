# Data Exchange — Exam Weight 15%

> Domain 4 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

Creating conceptual data mapping documents, custom importers, exports, and scripts for interchange
of data with OpenUSD.

## Exam Objectives

- **4.1** Convert OpenUSD assets to common 3D formats (such as glTF), and ensure fidelity.
- **4.2** Document conceptual mappings between USD and another data model (e.g., materialX).
- **4.3** Explain the trade-offs between USDC and USDA formats (performance, readability, archival, etc.).
- **4.4** Implement a "round-trip" pipeline in a DCC to and from USD.
- **4.5** Use USD schemas to support nonstandard attributes/structures during import/export.
- **4.6** Write a validator for ensuring integrity of an OpenUSD asset exported from a DCC.
- **4.7** Write an exporter or converter to USD.
- **4.8** Write or extend a USD importer in a DCC.

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Developing Data Exchange Pipelines](https://docs.nvidia.com/learn-openusd/latest/data-exchange/index.html)

### Tutorials
- [Traversing a Stage](https://openusd.org/release/tut_traversing_stage.html)
- [Converting Between Layer Formats](https://openusd.org/release/tut_converting_between_layer_formats.html)

### Glossary
- [Over](https://openusd.org/release/glossary.html#usdglossary-over)
- [Stage Traversal](https://openusd.org/release/glossary.html?highlight=traverse#stage-traversal)

### Technical References
- [Conceptual Data Mapping](https://docs.omniverse.nvidia.com/usd/latest/technical_reference/conceptual_data_mapping/index.html)
- [USD Toolset - usdchecker](https://openusd.org/release/toolset.html#usdchecker)
- [USD Toolset - usdcat](https://openusd.org/release/toolset.html#usdcat)
- [USD Toolset - usdzip](https://openusd.org/release/toolset.html#usdzip)
- [USD FAQ - What File Format Is My .usd File?](https://openusd.org/release/usdfaq.html#what-file-format-is-my-usd-file)
- [USDZ File Format Specification](https://openusd.org/release/spec_usdz.html)
- [Maximizing USD Performance](https://openusd.org/release/maxperf.html)

### API Docs
- [Encoding Stage UpAxis](https://openusd.org/release/api/group___usd_geom_up_axis__group.html)
- [Creating New Schema Classes With usdGenSchema](https://openusd.org/release/api/_usd__page__generating_schemas.html)
- [Common Idioms and Examples](https://openusd.org/release/api/_usd__page__common_idioms.html)
- [UsdGeomPoints - Detailed Description](https://openusd.org/release/api/class_usd_geom_points.html#details)
- [UsdProperty::GetNamespace()](https://openusd.org/release/api/class_usd_property.html#a914ef5e6cffe6c3c85f7b1085bea0cf2)
- [UsdGeomModelAPI::GetExtentsHint()](https://openusd.org/release/api/class_usd_geom_model_a_p_i.html#a4aa8b1f29a3097fe08da868bd2b8b259)
- [UsdGeomBoundable::ComputeExtentFromPlugins()](https://openusd.org/release/api/class_usd_geom_boundable.html#a413c9eb5b4e1d8fddd627cf33ed4a106)
- [UsdGeomBoundable::GetExtentAttr()](https://openusd.org/release/api/class_usd_geom_boundable.html#abecc87b5433fec139295a78b439b0531)
