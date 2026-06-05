import './styles.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import type { EngineBayAssetManifest, EngineBayPart } from './types';

const MANIFEST_URL = '/assets/sample-engine-bay/manifest.json';
const app = document.querySelector<HTMLDivElement>('#app');

if (!app) {
  throw new Error('App root not found');
}

app.innerHTML = `
  <main class="shell">
    <aside class="panel">
      <h1>Engine Bay</h1>
      <p class="meta">Search parts, select components, toggle exploded view, take measurements, and save/share camera views.</p>
      <input id="part-search" type="search" placeholder="Search name, SKU, OEM…" aria-label="Search parts" />
      <div id="part-list" class="part-list"></div>
    </aside>
    <section class="viewer-wrap" aria-label="3D engine bay viewer">
      <div id="loading" class="loading">Loading manifest…</div>
      <div id="fallback" class="fallback" hidden>GLB unavailable; showing procedural fallback parts.</div>
      <div id="hud" class="hud">HUD pending…</div>
      <div id="toolbar" class="toolbar">
        <button id="explode" type="button" aria-pressed="false">Exploded view</button>
        <button id="section" type="button" aria-pressed="false">Section cut</button>
        <button id="measure" type="button" aria-pressed="false">Measure</button>
        <button id="guided" type="button" aria-pressed="false">Where is this part?</button>
        <button id="screenshot" type="button">Screenshot</button>
        <button id="save-view" type="button">Save view</button>
      </div>
    </section>
    <aside id="details" class="panel right"><h2>No part selected</h2><p class="meta">Click a part or choose one from the list.</p></aside>
  </main>
`;

const viewerWrap = document.querySelector<HTMLElement>('.viewer-wrap')!;
const loading = document.querySelector<HTMLElement>('#loading')!;
const fallback = document.querySelector<HTMLElement>('#fallback')!;
const hud = document.querySelector<HTMLElement>('#hud')!;
const partList = document.querySelector<HTMLElement>('#part-list')!;
const details = document.querySelector<HTMLElement>('#details')!;
const search = document.querySelector<HTMLInputElement>('#part-search')!;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x071018);
const camera = new THREE.PerspectiveCamera(55, 1, 0.05, 100);
camera.position.set(2.4, 1.8, 3.2);
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.localClippingEnabled = true;
viewerWrap.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 0.55, 0);

scene.add(new THREE.HemisphereLight(0xc9e6ff, 0x111827, 1.8));
const keyLight = new THREE.DirectionalLight(0xffffff, 2.4);
keyLight.position.set(3, 4, 3);
keyLight.castShadow = true;
scene.add(keyLight);

const floor = new THREE.Mesh(
  new THREE.CircleGeometry(2.2, 80),
  new THREE.MeshStandardMaterial({ color: 0x0d1a28, roughness: 0.85, metalness: 0.05 }),
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const partMeshes = new Map<string, THREE.Mesh>();
const basePositions = new Map<string, THREE.Vector3>();
const sectionPlane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0.15);
let manifest: EngineBayAssetManifest;
let selectedPart: EngineBayPart | null = null;
let hoveredMesh: THREE.Mesh | null = null;
let exploded = false;
let sectionEnabled = false;
let measurementEnabled = false;
let guidedEnabled = false;
let lastTime = performance.now();
let frames = 0;
let fps = 0;

function resize() {
  const { clientWidth, clientHeight } = viewerWrap;
  camera.aspect = clientWidth / clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(clientWidth, clientHeight, false);
}

function partColor(part: EngineBayPart) {
  const palette: Record<string, number> = {
    'air-intake': 0x4db8ff,
    'forced-induction': 0xff9f43,
    cooling: 0x41d6a6,
    electrical: 0xffd166,
  };
  return palette[part.category] ?? 0x98a7b8;
}

function buildFallbackPart(part: EngineBayPart) {
  const geometry = part.category === 'electrical'
    ? new THREE.BoxGeometry(part.bounding_radius * 1.7, part.bounding_radius, part.bounding_radius * 1.2)
    : new THREE.SphereGeometry(part.bounding_radius, 32, 20);
  const material = new THREE.MeshStandardMaterial({ color: partColor(part), roughness: 0.48, metalness: 0.18 });
  material.clippingPlanes = [];
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = part.id;
  mesh.userData.partId = part.id;
  mesh.position.fromArray(part.position);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);
  partMeshes.set(part.id, mesh);
  basePositions.set(part.id, mesh.position.clone());
}

function renderPartList(parts: EngineBayPart[]) {
  const needle = search.value.trim().toLowerCase();
  const filtered = parts.filter((part) =>
    [part.name, part.sku, part.oem_number, part.category].some((v) => v.toLowerCase().includes(needle)),
  );
  const nodes = filtered.map((part) => {
    const btn = document.createElement('button');
    btn.className = `part-card${selectedPart?.id === part.id ? ' active' : ''}`;
    btn.dataset.partId = part.id;
    btn.type = 'button';
    const strong = document.createElement('strong');
    strong.textContent = part.name;
    const meta = document.createElement('span');
    meta.className = 'meta';
    meta.textContent = `${part.sku} · ${part.oem_number}`;
    meta.append(document.createElement('br'), part.category);
    btn.append(strong, meta);
    return btn;
  });
  partList.replaceChildren(...nodes);
}

function renderDetails(part: EngineBayPart | null) {
  if (!part) {
    const h2 = document.createElement('h2');
    h2.textContent = 'No part selected';
    const p = document.createElement('p');
    p.className = 'meta';
    p.textContent = 'Click a part or choose one from the list.';
    details.replaceChildren(h2, p);
    return;
  }

  const h2 = document.createElement('h2');
  h2.textContent = part.name;

  const metaP = document.createElement('p');
  metaP.className = 'meta';
  metaP.textContent = `SKU: ${part.sku}`;
  metaP.append(document.createElement('br'), `OEM: ${part.oem_number}`, document.createElement('br'), `Category: ${part.category}`);

  const serviceH3 = document.createElement('h3');
  serviceH3.textContent = 'Service data';

  const torqueP = document.createElement('p');
  torqueP.textContent = `Torque: ${part.torque_spec_nm ?? 'N/A'} Nm`;

  const notesList = document.createElement('ul');
  notesList.className = 'notes';
  for (const note of part.service_notes) {
    const li = document.createElement('li');
    li.textContent = note;
    notesList.append(li);
  }

  const docP = document.createElement('p');
  const link = document.createElement('a');
  const rawUrl = part.documentation_url;
  link.href = /^https?:\/\//i.test(rawUrl) || rawUrl.startsWith('/') ? rawUrl : '#';
  link.textContent = 'Open documentation';
  docP.append(link);

  const annotH3 = document.createElement('h3');
  annotH3.textContent = 'Annotations';

  const annotP = document.createElement('p');
  annotP.className = 'meta';
  annotP.textContent = 'Damage/issue annotation hooks are wired at the API contract level.';

  details.replaceChildren(h2, metaP, serviceH3, torqueP, notesList, docP, annotH3, annotP);
}

function selectPart(partId: string | null) {
  if (!manifest) return;
  selectedPart = manifest.parts.find((part) => part.id === partId) ?? null;
  for (const [id, mesh] of partMeshes) {
    const material = mesh.material as THREE.MeshStandardMaterial;
    material.emissive.set(id === selectedPart?.id ? 0x155cff : 0x000000);
    material.emissiveIntensity = id === selectedPart?.id ? 0.5 : 0;
  }
  if (selectedPart && guidedEnabled) {
    const target = basePositions.get(selectedPart.id);
    if (target) {
      controls.target.copy(target);
      camera.position.copy(target.clone().add(new THREE.Vector3(1.1, 0.75, 1.2)));
    }
  }
  renderPartList(manifest.parts);
  renderDetails(selectedPart);
}

function updateExplodedState() {
  if (!manifest) return;
  for (const part of manifest.parts) {
    const mesh = partMeshes.get(part.id);
    const base = basePositions.get(part.id);
    if (!mesh || !base) continue;
    const offset = new THREE.Vector3(...part.exploded_offset).multiplyScalar(exploded ? 1 : 0);
    mesh.position.lerp(base.clone().add(offset), 0.18);
  }
}

function updateSectionState() {
  for (const mesh of partMeshes.values()) {
    const material = mesh.material as THREE.MeshStandardMaterial;
    material.clippingPlanes = sectionEnabled ? [sectionPlane] : [];
    material.needsUpdate = true;
  }
}

async function loadManifest() {
  const response = await fetch(MANIFEST_URL);
  if (!response.ok) throw new Error(`Manifest failed: ${response.status}`);
  manifest = await response.json() as EngineBayAssetManifest;
  loading.textContent = 'Loading model…';

  const loader = new GLTFLoader();
  if (manifest.draco_compressed) {
    const draco = new DRACOLoader();
    draco.setDecoderPath('/draco/');
    loader.setDRACOLoader(draco);
  }
  if (manifest.meshopt_compressed) {
    loader.setMeshoptDecoder(
      // @types/three does not yet expose MeshoptDecoder; suppress the mismatch.
      MeshoptDecoder as Parameters<typeof loader.setMeshoptDecoder>[0],
    );
  }

  try {
    const gltf = await loader.loadAsync(manifest.model_url);
    scene.add(gltf.scene);
    // Map any GLB nodes that carry a partId in userData to the selection layer
    gltf.scene.traverse((node) => {
      if (node instanceof THREE.Mesh && node.userData.partId) {
        const id = String(node.userData.partId);
        partMeshes.set(id, node);
        basePositions.set(id, node.position.clone());
      }
    });
  } catch {
    fallback.hidden = false;
    manifest.parts.forEach(buildFallbackPart);
  }

  renderPartList(manifest.parts);
  loading.hidden = true;
}

renderer.domElement.addEventListener('pointermove', (event) => {
  const bounds = renderer.domElement.getBoundingClientRect();
  pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
  pointer.y = -(((event.clientY - bounds.top) / bounds.height) * 2 - 1);
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObjects([...partMeshes.values()])[0]?.object as THREE.Mesh | undefined;
  if (hoveredMesh && hoveredMesh !== hit && hoveredMesh.userData.partId !== selectedPart?.id) {
    (hoveredMesh.material as THREE.MeshStandardMaterial).emissive.set(0x000000);
  }
  hoveredMesh = hit ?? null;
  if (hoveredMesh && hoveredMesh.userData.partId !== selectedPart?.id) {
    const material = hoveredMesh.material as THREE.MeshStandardMaterial;
    material.emissive.set(0x41d6ff);
    material.emissiveIntensity = 0.35;
  }
});

renderer.domElement.addEventListener('click', () => {
  if (measurementEnabled && selectedPart && hoveredMesh?.userData.partId) {
    const a = basePositions.get(selectedPart.id);
    const b = basePositions.get(hoveredMesh.userData.partId);
    if (a && b) alert(`Approximate center-to-center distance: ${a.distanceTo(b).toFixed(2)} ${manifest.units}`);
    return;
  }
  selectPart(hoveredMesh?.userData.partId ?? null);
});

partList.addEventListener('click', (event) => {
  const card = (event.target as HTMLElement).closest<HTMLElement>('[data-part-id]');
  if (card) selectPart(card.dataset.partId ?? null);
});
search.addEventListener('input', () => renderPartList(manifest?.parts ?? []));

function bindToggle(id: string, handler: (pressed: boolean) => void) {
  document.querySelector<HTMLButtonElement>(`#${id}`)!.addEventListener('click', (event) => {
    const button = event.currentTarget as HTMLButtonElement;
    const pressed = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(pressed));
    handler(pressed);
  });
}

bindToggle('explode', (pressed) => { exploded = pressed; });
bindToggle('section', (pressed) => { sectionEnabled = pressed; updateSectionState(); });
bindToggle('measure', (pressed) => { measurementEnabled = pressed; });
bindToggle('guided', (pressed) => { guidedEnabled = pressed; if (selectedPart) selectPart(selectedPart.id); });

document.querySelector<HTMLButtonElement>('#screenshot')!.addEventListener('click', () => {
  const link = document.createElement('a');
  link.download = `engine-bay-${Date.now()}.png`;
  link.href = renderer.domElement.toDataURL('image/png');
  link.click();
});

document.querySelector<HTMLButtonElement>('#save-view')!.addEventListener('click', async () => {
  const view = {
    camera: camera.position.toArray(),
    target: controls.target.toArray(),
    selectedPart: selectedPart?.id ?? null,
  };
  await navigator.clipboard?.writeText(`${location.origin}${location.pathname}#view=${encodeURIComponent(JSON.stringify(view))}`);
  alert('Shareable camera view copied to clipboard.');
});

function animate() {
  requestAnimationFrame(animate);
  updateExplodedState();
  controls.update();
  renderer.render(scene, camera);
  frames += 1;
  const now = performance.now();
  if (now - lastTime > 1000) {
    fps = Math.round((frames * 1000) / (now - lastTime));
    frames = 0;
    lastTime = now;
    const info = renderer.info.render;
    hud.textContent = `FPS ${fps} · calls ${info.calls} · tris ${info.triangles} · parts ${partMeshes.size}`;
  }
}

function restoreHashView() {
  const hash = location.hash;
  if (!hash.startsWith('#view=')) return;
  try {
    const raw = decodeURIComponent(hash.slice(6));
    if (raw.length > 2048) return; // guard against oversized payloads
    const view = JSON.parse(raw) as {
      camera?: number[];
      target?: number[];
      selectedPart?: string | null;
    };
    if (Array.isArray(view.camera) && view.camera.length === 3) {
      camera.position.set(view.camera[0], view.camera[1], view.camera[2]);
    }
    if (Array.isArray(view.target) && view.target.length === 3) {
      controls.target.set(view.target[0], view.target[1], view.target[2]);
    }
    if (typeof view.selectedPart === 'string') {
      selectPart(view.selectedPart);
    }
  } catch {
    // Ignore malformed hash
  }
}

window.addEventListener('resize', resize);
resize();
void loadManifest()
  .then(() => { restoreHashView(); })
  .catch((error) => {
    loading.textContent = `Unable to load engine bay: ${error instanceof Error ? error.message : 'unknown error'}`;
  });
animate();
