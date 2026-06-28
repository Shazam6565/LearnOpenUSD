# Debugging and Troubleshooting — Exam Weight 11%

> Domain 6 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

Introspecting USD stages for the purpose of fixing unexpected or undesired composition results,
identifying bad authored data, or optimizing load and render times.

## Exam Objectives

- **6.1** Identify when using SdfChangeBlocks can alleviate performance bottlenecks.
- **6.2** Identify why opinions from one layer do not take effect in a composed stage.
- **6.3** Resolve issues related to asset management.
- **6.4** Understand what causes unexpected visual results.
- **6.5** Work with diagnostics for debugging and profiling (TfDebug, diagnostic delegates, Trace, TfMallocTag, ...).

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Creating Composition Arcs](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/index.html)

### Tutorials
- [Inspecting and Authoring Properties](https://openusd.org/release/tut_inspect_and_author_props.html)
- [Traversing a Stage](https://openusd.org/release/tut_traversing_stage.html)

### Glossary
- [LIVERPS](https://openusd.org/release/glossary.html#liverps-strength-ordering)
- [Reference](https://openusd.org/release/glossary.html#usdglossary-references)
- [Visibility](https://openusd.org/release/glossary.html#usdglossary-visibility)
- [IsA Schema](https://openusd.org/release/glossary.html#isa-schema)
- [Inherits](https://openusd.org/release/glossary.html#usdglossary-inherits)

### Technical References
- [Maximizing USD Performance](https://openusd.org/release/maxperf.html)
- [USD Toolset - usdcat](https://openusd.org/release/toolset.html#usdcat)
- [USD FAQ - What's the Difference Between an "Over" and a "Typeless Def"?](https://openusd.org/release/usdfaq.html#what-s-the-difference-between-an-over-and-a-typeless-def)
- [usdview LayerStack tab](https://docs.omniverse.nvidia.com/usd/latest/usdview/panel_composition.html#layer-stack)

### API Docs
- [UsdPrim](https://openusd.org/release/api/class_usd_prim.html)
- [UsdReference - Expressing References Without Prim Paths](https://openusd.org/release/api/class_usd_references.html#Usd_DefaultPrim_References)
- [UsdGeomModelAPI - Draw Modes](https://openusd.org/release/api/class_usd_geom_model_a_p_i.html#UsdGeomModelAPI_drawMode)
- [UsdProperty::GetPropertyStack()](https://openusd.org/release/api/class_usd_property.html#a2159d3d651cd66e4fb1c724be90ed5e0)
- [UsdUtilsCoalescingDiagnosticDelegate](https://openusd.org/release/api/class_usd_utils_coalescing_diagnostic_delegate.html)
- [TfDiagnosticMgr::Delegate](https://openusd.org/release/api/class_tf_diagnostic_mgr_1_1_delegate.html)
- [UsdStage::Open() - pathResolverContext](https://openusd.org/release/api/class_usd_stage.html#ad3e185c150ee38ae13fb76115863d108)
- [UsdStage - Variant Management](https://openusd.org/release/api/class_usd_stage.html#Usd_variantManagement)
- [UsdStage - Working Set Management](https://openusd.org/release/api/class_usd_stage.html#Usd_workingSetManagement)
- [UsdStage::MuteLayer()](https://openusd.org/release/api/class_usd_stage.html#a8af4162fe11cc6a5f21a39e770d397c2)
- [UsdReferences - Reasons Why Adding a Reference May Fail...](https://openusd.org/release/api/class_usd_references.html#Usd_Failing_References)
- [Pcp: PrimCache Population (Composition) - Errors](https://openusd.org/release/api/pcp_page_front.html#pcp_Errors)
