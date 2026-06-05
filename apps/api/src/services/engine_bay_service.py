from ..schemas.engine_bay import (
    EngineBayAnnotation,
    EngineBayAnnotationIn,
    EngineBayAssembly,
    EngineBayAssetManifest,
    EngineBayPart,
    ServiceStep,
)


class EngineBayService:
    """In-memory engine-bay catalog and manifest service.

    This is a production-facing API contract scaffold. Replace the sample data with
    database-backed repositories, object storage manifests, and audit logging before
    exposing real customer assets.
    """

    def __init__(self) -> None:
        self._parts = [
            EngineBayPart(
                id="intake_manifold",
                name="Intake Manifold",
                sku="SRG-INT-001",
                oem_number="OEM-INT-7842",
                category="air-intake",
                documentation_url="/docs/engine-bay/intake-manifold",
                torque_spec_nm=24,
                service_notes=[
                    "Inspect gasket before reinstalling",
                    "Tighten bolts in a cross pattern",
                ],
                position=(0.0, 1.2, 0.0),
                exploded_offset=(0.0, 0.7, 0.0),
                bounding_radius=0.45,
            ),
            EngineBayPart(
                id="turbocharger",
                name="Turbocharger Assembly",
                sku="SRG-TBO-220",
                oem_number="OEM-TBO-4210",
                category="forced-induction",
                documentation_url="/docs/engine-bay/turbocharger",
                torque_spec_nm=38,
                service_notes=[
                    "Allow engine to cool before service",
                    "Prime oil feed before first start",
                ],
                position=(-0.75, 0.55, 0.25),
                exploded_offset=(-0.55, 0.25, 0.35),
                bounding_radius=0.32,
            ),
            EngineBayPart(
                id="coolant_reservoir",
                name="Coolant Reservoir",
                sku="SRG-CLR-018",
                oem_number="OEM-CLR-9011",
                category="cooling",
                documentation_url="/docs/engine-bay/coolant-reservoir",
                torque_spec_nm=8,
                service_notes=["Verify coolant is below max fill line when cold"],
                position=(0.85, 0.65, -0.35),
                exploded_offset=(0.45, 0.25, -0.35),
                bounding_radius=0.24,
            ),
            EngineBayPart(
                id="battery",
                name="Battery",
                sku="SRG-BAT-012",
                oem_number="OEM-BAT-5300",
                category="electrical",
                documentation_url="/docs/engine-bay/battery",
                torque_spec_nm=6,
                service_notes=[
                    "Disconnect negative terminal first",
                    "Use memory saver when required",
                ],
                position=(0.95, 0.35, 0.45),
                exploded_offset=(0.6, 0.15, 0.45),
                bounding_radius=0.28,
            ),
        ]
        self._assemblies = [
            EngineBayAssembly(
                id="srg-demo-engine-bay",
                name="SRG Demo Engine Bay",
                vehicle="SRG GT Development Mule",
                revision="2026.06.0",
                model_url="/assets/sample-engine-bay/engine-bay.glb",
                thumbnail_url="/assets/sample-engine-bay/thumbnail.webp",
                compatible_configurations=["2.0T", "2.0T Track Pack"],
                part_count=len(self._parts),
            )
        ]
        self._annotations: list[EngineBayAnnotation] = []

    def list_assemblies(self) -> list[EngineBayAssembly]:
        return self._assemblies

    def get_assembly(self, assembly_id: str) -> EngineBayAssembly | None:
        return next((assembly for assembly in self._assemblies if assembly.id == assembly_id), None)

    def list_parts(self, assembly_id: str) -> list[EngineBayPart] | None:
        if self.get_assembly(assembly_id) is None:
            return None
        return self._parts

    def asset_manifest(self, assembly_id: str) -> EngineBayAssetManifest | None:
        assembly = self.get_assembly(assembly_id)
        if assembly is None:
            return None
        return EngineBayAssetManifest(
            manifest_version="1.0.0",
            assembly_id=assembly.id,
            revision=assembly.revision,
            units="meter",
            up_axis="Y",
            model_url=assembly.model_url,
            draco_compressed=True,
            meshopt_compressed=True,
            texture_format="ktx2",
            lods=[
                "/assets/sample-engine-bay/engine-bay-lod0.glb",
                "/assets/sample-engine-bay/engine-bay-lod1.glb",
            ],
            parts=self._parts,
        )

    def service_procedures(self, assembly_id: str) -> list[ServiceStep] | None:
        if self.get_assembly(assembly_id) is None:
            return None
        return [
            ServiceStep(
                id="locate-intake",
                title="Locate intake manifold",
                description="Use guided mode to highlight the intake manifold and nearby fasteners.",
                part_ids=["intake_manifold"],
                estimated_minutes=2,
            ),
            ServiceStep(
                id="inspect-turbo-oil-feed",
                title="Inspect turbo oil feed",
                description="Highlight turbocharger service points and verify no visible seepage is present.",
                part_ids=["turbocharger"],
                estimated_minutes=5,
            ),
        ]

    def list_annotations(self, assembly_id: str) -> list[EngineBayAnnotation] | None:
        if self.get_assembly(assembly_id) is None:
            return None
        return [annotation for annotation in self._annotations if annotation.assembly_id == assembly_id]

    def create_annotation(self, assembly_id: str, payload: EngineBayAnnotationIn) -> EngineBayAnnotation | None:
        part_ids = {part.id for part in self._parts}
        if self.get_assembly(assembly_id) is None or payload.part_id not in part_ids:
            return None
        annotation = EngineBayAnnotation(
            id=f"ann_{len(self._annotations) + 1:04d}",
            assembly_id=assembly_id,
            **payload.dict(),
        )
        self._annotations.append(annotation)
        return annotation
