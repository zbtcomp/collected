# three.js — the world for the collected

A real-time environment built to give the collected somewhere to be. Where the simulation teaches the sculpture to *move*, this gives it an atmosphere to move through — a drifting volumetric field that stands in for the latent space the collected is said to live inside.

---

## `collected3.js`

A particle system that turns a single mesh into a volumetric fog/cloud. It is written as a script attached to a three.js `Mesh` and exposes two functions the host scene calls: `init()` (once) and `update(event)` (every frame).

**What it does:**

- Hides the original mesh and clones its material into a soft, transparent, double-sided cloud material.
- Spawns **200** flat 30×30 planes at random positions inside an 80-unit cube, drawn efficiently with a single `InstancedMesh`.
- Each frame, drifts every plane on procedural wind (sine/cosine over time) plus a small per-particle jitter, so the field moves like slow fog rather than a rigid block.
- **Billboarding:** every plane turns to face the camera each frame, so the flat planes always read as soft volume from any angle.
- **Wrapping:** particles that drift past the edge of the cube reappear on the opposite side, keeping the fog endless and seamless.

**Tuning** (constants at the top of the file):

| Constant | Meaning |
|---|---|
| `particleCount` | Number of cloud planes (200) |
| `spread` | Size of the cube the particles live in (80) |
| `localJitter` | Per-frame random wobble (0.08) |
| `driftSpeed` | Base wind speed (0.07) |

---

## Requirements

- A three.js scene (r128-era API; uses `THREE.InstancedMesh`, `THREE.PlaneGeometry`, `THREE.Object3D`).
- The script must be attached to a `Mesh` that already has a **material with a texture** — the cloud look comes from that texture. Without a material the script logs an error and stops.
- A `camera` reachable in scope for the billboarding to work (it degrades gracefully if none is found).

---

## Use

Attach `collected3.js` to a textured mesh in the host three.js project. The particle system adds itself to the same parent as that mesh, so it appears wherever the placeholder mesh sits. Adjust the four constants to make the fog denser, larger, or faster.
