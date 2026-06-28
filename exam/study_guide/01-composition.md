# Composition — Exam Weight 23%

> Domain 1 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

Authoring, design with, or debugging composition arcs. A developer needs to know all of the
composition arcs, how they work, and when and when it is appropriate to use each. The developer
needs to be able to debug complex LIVRPS scenarios.

## Exam Objectives

- **1.1** Change the strength of an opinion.
- **1.2** Choose an appropriate instancing style for data at different scales.
- **1.3** Compare between referencing, payloads, and sublayers, and identify their use cases.
- **1.4** Create a scene with multiple elements referencing the same animation at different time-offset.
- **1.5** Design potential scene layering strategies to facilitate multi-user workflows.
- **1.6** Explain LIVERPS in simple terms.
- **1.7** Identify situations where variants are/are not appropriate for structuring assets.
- **1.8** Identify why opinions from one layer do not take effect in a composed stage.
- **1.9** Prepare an internal asset to be delivered to external parties.
- **1.10** Remove properties from instanced component prims in an assembly stage.
- **1.11** Split a monolithic asset to model multiple collaborative workstreams.

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Creating Composition Arcs](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/index.html)

### Tutorials
- [Referencing Layers](https://openusd.org/release/tut_referencing_layers.html)
- [Authoring Variants](https://openusd.org/release/tut_authoring_variants.html)

### Glossary
- [LIVERPS](https://openusd.org/release/glossary.html#liverps-strength-ordering)
- [Sublayers](https://openusd.org/release/glossary.html#usdglossary-sublayers)
- [Variant Set](https://openusd.org/release/glossary.html#usdglossary-variantset)
- [Reference](https://openusd.org/release/glossary.html#usdglossary-references)
- [Payload](https://openusd.org/release/glossary.html#usdglossary-payload)
- [Timesample](https://openusd.org/release/glossary.html#usdglossary-timesample)
- [Value Clips](https://openusd.org/release/glossary.html#usdglossary-valueclips)
- [Layer Offset](https://openusd.org/release/glossary.html#layer-offset)
- [Edit Target](https://openusd.org/release/glossary.html#edittarget)
- [Change Processing](https://openusd.org/release/glossary.html#change-processing)
- [Flatten](https://openusd.org/release/glossary.html#flatten)

### API Docs
- [Scenegraph Instancing](https://openusd.org/release/api/_usd__page__scenegraph_instancing.html)
- [Basic Datatypes for Scene Description Provided by Sdf](https://openusd.org/release/api/_usd__page__datatypes.html)
- [Edit Target - Detailed Description](https://openusd.org/release/api/class_usd_edit_target.html#details)
- [UsdStage::Flatten()](https://openusd.org/release/api/class_usd_stage.html#ae3271778fa2ceeb82fbd51296610820a)
- [UsdReference - Expressing References Without Prim Paths](https://openusd.org/release/api/class_usd_references.html#Usd_DefaultPrim_References)

### Additional Resources
- [USD Composition - SIGGRAPH 2019](https://openusd.org/files/Siggraph2019_USD%20Composition.pdf)
- [USD Book - Default Prim](https://remedy-entertainment.github.io/USDBook/terminology/default_prim.html)
- [OpenUSD Code Samples - Add a Payload](https://docs.omniverse.nvidia.com/dev-guide/latest/programmer_ref/usd/references-payloads/add-payload.html)

---

> **Spelling note:** the official guide writes the strength-ordering mnemonic both ways — "LIVRPS"
> in the domain description above and "LIVERPS" in objective 1.6 and the glossary link. Both refer
> to the same concept (Local, Inherits, Variants, References, Payloads, Specializes).
