# Pipeline Development — Exam Weight 14%

> Domain 7 of the NVIDIA NCP-OUSD exam blueprint. Extracted from the official
> *NVIDIA-Certified Professional: OpenUSD Development Exam Study Guide* v1.1.0 (OCT25).

High-level tasks that are important for a well-rounded OpenUSD developer or architect, including
designing the pipeline, asset management, versioning, diagraming, documenting, UI/UX, writing a
USD exporter hook to transform data into your pipeline's preferred structure, managing build
configurations, or flattening and removing proprietary dependencies from an asset.

## Exam Objectives

- **7.1** Convert OpenUSD assets to common 3D formats (such as glTF), and ensure fidelity.
- **7.2** Document asset structure guidelines.
- **7.3** Explain trade-offs between USDC and USDA formats (performance, readability, archival, etc.).
- **7.4** Implement "round-trip" pipelines between a DCC and USD.
- **7.5** Integrate custom resolvers to manage asset paths dynamically.
- **7.6** Represent custom metadata.
- **7.7** Validate asset paths are formatted correctly.
- **7.8** Write or extend a USD importer in a DCC.

## NVIDIA Courses and Suggested Readings

### Course Reference
- [Learn OpenUSD: Setting the Stage](https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html)
- [Learn OpenUSD: Scene Description Blueprints](https://docs.nvidia.com/learn-openusd/latest/scene-description-blueprints/index.html)
- [Learn OpenUSD: Composition Basics](https://docs.nvidia.com/learn-openusd/latest/composition-basics/index.html)
- [Learn OpenUSD: Beyond the Basics](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/index.html)
- [Learn OpenUSD: Creating Composition Arcs](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/index.html)
- [Learn OpenUSD: Asset Structure Principles and Content Aggregation](https://docs.nvidia.com/learn-openusd/latest/asset-structure/index.html)

### Tutorials
- [Authoring Variants](https://openusd.org/release/tut_authoring_variants.html)

### Glossary
- [Subcomponent](https://openusd.org/release/glossary.html#usdglossary-subcomponent)
- [Crate File Format](https://openusd.org/release/glossary.html#crate-file-format)
- [TimeCode](https://openusd.org/release/glossary.html#usdglossary-timecode)
- [Flatten](https://openusd.org/release/glossary.html#flatten)
- [Edit Target](https://openusd.org/release/glossary.html#edittarget)

### Technical References
- [USD FAQ - I Have Some Layers I Want to Combine: Should I Use SubLayers or References?](https://openusd.org/release/usdfaq.html#i-have-some-layers-i-want-to-combine-should-i-use-sublayers-or-references)
- [Principles of Scalable Asset Structure in OpenUSD](https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html)
- [ASWF Asset Structure Guidelines](https://github.com/usd-wg/assets/blob/main/docs/asset-structure-guidelines.md)

### API Docs
- [UsdStage::Flatten()](https://openusd.org/release/api/class_usd_stage.html#ae3271778fa2ceeb82fbd51296610820a)
- [Edit Target - Detailed Description](https://openusd.org/release/api/class_usd_edit_target.html#details)
- [UsdStage::Traverse()](https://openusd.org/release/api/class_usd_stage.html#adba675b55f41cc1b305bed414fc4f178)
- [UsdPhysics: USD Physics Schema](https://openusd.org/release/api/usd_physics_page_front.html)
- [Encoding Stage Linear Units](https://openusd.org/release/api/group___usd_geom_linear_units__group.html)
- [Encoding Stage UpAxis](https://openusd.org/release/api/group___usd_geom_up_axis__group.html)
- [SdfChangeBlock](https://openusd.org/release/api/class_sdf_change_block.html)
- [UsdNotice](https://openusd.org/release/api/class_usd_notice.html)
- [UsdGeom: USD Geometry Schema - Applying Timesampled Velocities to Geometry](https://openusd.org/release/api/usd_geom_page_front.html#UsdGeom_VelocityInterpolation)
