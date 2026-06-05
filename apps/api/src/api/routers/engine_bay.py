from fastapi import APIRouter, HTTPException

from ...schemas.engine_bay import (
    EngineBayAnnotation,
    EngineBayAnnotationIn,
    EngineBayAssembly,
    EngineBayAssetManifest,
    EngineBayPart,
    ServiceStep,
)
from ...services.engine_bay_service import EngineBayService

router = APIRouter()
service = EngineBayService()


@router.get("/assemblies", response_model=list[EngineBayAssembly])
def list_assemblies():
    return service.list_assemblies()


@router.get("/assemblies/{assembly_id}", response_model=EngineBayAssembly)
def get_assembly(assembly_id: str):
    assembly = service.get_assembly(assembly_id)
    if assembly is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly not found")
    return assembly


@router.get("/assemblies/{assembly_id}/parts", response_model=list[EngineBayPart])
def list_parts(assembly_id: str):
    parts = service.list_parts(assembly_id)
    if parts is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly not found")
    return parts


@router.get("/assemblies/{assembly_id}/asset-manifest", response_model=EngineBayAssetManifest)
def get_asset_manifest(assembly_id: str):
    manifest = service.asset_manifest(assembly_id)
    if manifest is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly not found")
    return manifest


@router.get("/assemblies/{assembly_id}/service-procedures", response_model=list[ServiceStep])
def get_service_procedures(assembly_id: str):
    procedures = service.service_procedures(assembly_id)
    if procedures is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly not found")
    return procedures


@router.get("/assemblies/{assembly_id}/annotations", response_model=list[EngineBayAnnotation])
def list_annotations(assembly_id: str):
    annotations = service.list_annotations(assembly_id)
    if annotations is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly not found")
    return annotations


@router.post("/assemblies/{assembly_id}/annotations", response_model=EngineBayAnnotation, status_code=201)
def create_annotation(assembly_id: str, payload: EngineBayAnnotationIn):
    annotation = service.create_annotation(assembly_id, payload)
    if annotation is None:
        raise HTTPException(status_code=404, detail="Engine bay assembly or part not found")
    return annotation
