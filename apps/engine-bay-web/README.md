# SRG Engine Bay Web

Dedicated 3D engine bay viewer prototype built with Vite, TypeScript, and Three.js.

## Run locally

```bash
npm ci
npm run dev
```

## Production-oriented features in this scaffold

- Manifest-driven GLB loading with graceful procedural fallback parts.
- Orbit/pan/zoom camera controls.
- Part hover, selection, search, metadata, service notes, and documentation links.
- Exploded view, section/cutaway clipping, guided part focus, measurement mode, screenshot export, and saved camera links.
- Performance HUD for FPS, draw calls, triangles, and active part count.
- Responsive layout for desktop, tablet, and mobile review.

## Asset validation

```bash
npm run validate:assets
```

Real production assets should be generated from CAD through an offline optimization pipeline that emits GLB files plus the versioned manifest in `public/assets/<assembly>/manifest.json`.
