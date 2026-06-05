from pydantic import BaseModel, Field


class EngineBayPart(BaseModel):
    id: str
    name: str
    sku: str
    oem_number: str
    category: str
    parent_id: str | None = None
    documentation_url: str
    torque_spec_nm: float | None = Field(default=None, ge=0)
    service_notes: list[str] = Field(default_factory=list)
    position: tuple[float, float, float]
    exploded_offset: tuple[float, float, float]
    bounding_radius: float = Field(gt=0)


class EngineBayAssembly(BaseModel):
    id: str
    name: str
    vehicle: str
    revision: str
    model_url: str
    thumbnail_url: str
    compatible_configurations: list[str]
    part_count: int


class EngineBayAssetManifest(BaseModel):
    manifest_version: str
    assembly_id: str
    revision: str
    units: str = Field(pattern="^(meter|millimeter|centimeter|inch)$")
    up_axis: str = Field(pattern="^(Y|Z)$")
    model_url: str
    draco_compressed: bool
    meshopt_compressed: bool
    texture_format: str
    lods: list[str]
    parts: list[EngineBayPart]


class EngineBayAnnotationIn(BaseModel):
    part_id: str
    note: str = Field(min_length=1, max_length=500)
    severity: str = Field(default="info", pattern="^(info|warning|critical)$")
    camera_view: dict[str, float] = Field(default_factory=dict)


class EngineBayAnnotation(EngineBayAnnotationIn):
    id: str
    assembly_id: str


class ServiceStep(BaseModel):
    id: str
    title: str
    description: str
    part_ids: list[str]
    estimated_minutes: int = Field(ge=0)
