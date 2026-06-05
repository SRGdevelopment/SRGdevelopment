export interface EngineBayPart {
  id: string;
  name: string;
  sku: string;
  oem_number: string;
  category: string;
  parent_id?: string | null;
  documentation_url: string;
  torque_spec_nm?: number | null;
  service_notes: string[];
  position: [number, number, number];
  exploded_offset: [number, number, number];
  bounding_radius: number;
}

export interface EngineBayAssetManifest {
  manifest_version: string;
  assembly_id: string;
  revision: string;
  units: 'meter' | 'millimeter' | 'centimeter' | 'inch';
  up_axis: 'Y' | 'Z';
  model_url: string;
  draco_compressed: boolean;
  meshopt_compressed: boolean;
  texture_format: string;
  lods: string[];
  parts: EngineBayPart[];
}

export interface AnnotationPin {
  id: string;
  partId: string;
  note: string;
  severity: 'info' | 'warning' | 'critical';
}
