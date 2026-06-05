# 3D Engine Bay Production Roadmap

This repo now includes a dedicated `apps/engine-bay-web` prototype and `/engine-bay` API surface. The current implementation is intentionally asset-ready: it can load a versioned manifest, attempts to fetch a GLB, and falls back to procedural part proxies until optimized CAD exports are available.

## Implemented foundation

- Three.js viewer with OrbitControls for pan/zoom/orbit.
- Manifest-driven glTF/GLB loading hook with graceful fallback parts.
- Part search by name, SKU, OEM number, or category.
- Click and hover selection with metadata panel.
- Exploded view toggle using per-part offsets.
- Section/cutaway toggle using renderer clipping planes.
- Measurement mode for approximate center-to-center distances.
- Guided “Where is this part?” camera focus mode.
- Screenshot export and copyable saved camera views.
- Performance HUD for FPS, draw calls, triangles, and active part count.
- Responsive desktop/mobile layout.
- Backend API contracts for assemblies, parts, asset manifests, procedures, and annotations.
- Dependency-free manifest validation script for CI.

## Next production milestones

1. Replace procedural fallback parts with real CAD-derived `glb` assets that preserve stable part IDs in node names or `userData`.
2. Add an offline CAD optimization job for mesh decimation, LOD generation, Draco/Meshopt geometry compression, and KTX2/Basis texture compression.
3. Store manifests and assets in versioned object storage and serve them through signed URLs or a CDN.
4. Move sample API data to SQLAlchemy models/repositories with audit logs for part, annotation, and procedure changes.
5. Add visual regression snapshots for canonical camera views and performance budgets for draw calls, triangles, bundle size, and Lighthouse scores.
6. Add role-based access controls for internal engineering, service technicians, and customer-facing documentation views.
