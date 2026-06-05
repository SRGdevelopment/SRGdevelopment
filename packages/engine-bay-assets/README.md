# Engine Bay Assets

Shared asset-pipeline contracts for the 3D engine bay viewer.

## Manifest validation

```bash
python3 packages/engine-bay-assets/scripts/validate_manifest.py apps/engine-bay-web/public/assets/sample-engine-bay/manifest.json
```

The manifest records assembly revision, coordinate units, model URLs, compression flags, LODs, and selectable part metadata. Production CAD conversion should emit this manifest as the handoff between source CAD, optimized GLB assets, and the web/API layers.
