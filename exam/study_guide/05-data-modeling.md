# Data Modeling — Exam Weight 13%

> Domain 5 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

Require understanding of USD and Sdf data structures and data types, including prims, properties
(attributes/relationships), primvars, valueTypes (float, token, matrix4d, etc.), timeSamples, and
built-in USD schemas.

## Exam Objectives

- **5.1** Add a primvar to a mesh.
- **5.2** Choose the appropriate value types to store attribute data.
- **5.3** Represent custom metadata.
- **5.4** Retrieve properties of a prim.
- **5.5** Understand what causes unexpected visual results.
- **5.6** Update the extent attribute of a mesh after having updated its points.

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Setting the Stage](https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html)
- [Learn OpenUSD: Scene Description Blueprints](https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/index.html)
- [Learn OpenUSD: Beyond the Basics](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/index.html)

### Tutorials
- [Transformations, Time-Sampled Animation, and Layer Offsets](https://openusd.org/release/tut_xforms.html)
- [Generating New Schema Classes](https://openusd.org/release/tut_generating_new_schema.html)

### User Guides
- [Rendering User Guide - Working With Primvars](https://openusd.org/release/user_guides/render_user_guide.html#working-with-primvars)

### Glossary
- [TimeCode](https://openusd.org/release/glossary.html#usdglossary-timecode)
- [Layer Offset](https://openusd.org/release/glossary.html#layer-offset)
- [List Editing](https://openusd.org/release/glossary.html#list-editing)
- [Primvar](https://openusd.org/release/glossary.html#usdglossary-primvar)

### Technical References
- [USD Proposals - Spline Animation in USD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/spline-animation#spline-animation-in-usd)
- [Maximizing USD Performance](https://openusd.org/release/maxperf.html)

### API Docs
- [Basic Datatypes for Scene Description Provided by Sdf](https://openusd.org/release/api/_usd__page__datatypes.html)
- [Encoding Stage Linear Units](https://openusd.org/release/api/group___usd_geom_linear_units__group.html)
- [UsdAttribute - Attribute Interpolation](https://openusd.org/release/api/class_usd_attribute.html#Usd_AttributeInterpolation)
- [UsdGeomPrimvar - Detailed Description](https://openusd.org/release/api/class_usd_geom_primvar.html#details)
- [UsdGeomPrimvar - Interpolation of Geometric Primitive Variables](https://openusd.org/release/api/class_usd_geom_primvar.html#Usd_InterpolationVals)
- [Sdf: Scene Description Foundations - Types](https://openusd.org/release/api/sdf_page_front.html#sdf_metadata_types)
- [Creating New Schema Classes With usdGenSchema](https://openusd.org/release/api/_usd__page__generating_schemas.html)
- [UsdGeomBoundable](https://openusd.org/release/api/class_usd_geom_boundable.html)
- [UsdGeomXformable](https://openusd.org/release/api/class_usd_geom_xformable.html)
- [UsdGeomXformCache](https://openusd.org/release/api/class_usd_geom_xform_cache.html)
- [UsdStage::SetInterpolationType()](https://openusd.org/release/api/class_usd_stage.html#ad29a9aaba12c36407936a21abf514ea4)
