# The Collected

*Trained with art collections and a cemetery dataset, this project questions the change of forms, time and condition of mediums. Looking at AI as an intermediary to create computational and algorithmic narratives, the work deals with ‘what does it mean to be made of?’.*

This repository holds the code for **The Collected** — a project that trains models on museum and personal archives, fuses two of them into a single model, and gives the resulting output a body, a world, and eventually the ability to move. The physical work (3D prints, heatpress and UV prints, the installation) lives offline; what is versioned here is the machine-learning, simulation, and real-time code behind it.

---

## Concept

Art happens in different forms. I am interested in changing forms. Cemeteries are museums that contain humans as datasets. Merging art collections — many containing figures that are dead — is a way of learning stories, techniques, fictions, historical and social elements. The project asks: how would an AI collection look, and what does it tell us? What medium is a human being? What medium is time? What does it mean to be made of?

The central sculpture, **the collected**, is a clear resin 3D print made from a model trained on sculpture pictures of the collection. Across the work it stops being an object and becomes a character: a sculpture from an AI collection, living in the latent space. The moving image work explores the computational narrative and theory in this context.

---

## The three archives

| Archive | Source | Training | Becomes |
|---|---|---|---|
| One | Goldsmiths Textile Collection (1,400 images) | DreamBooth LoRA | Texture — yarn, thread, weave |
| Two | Russell-Cotes Collection (36 photographs) | IP-Adapter conditioning | Structure — rooms, sculptures |
| Three | My own cemetery photographs | WGAN | Movement — the video |

Archives one and two are **fused**: an InstructPix2Pix model is trained on paired data and the LoRA weights are merged into it, so neither collection is imitating the other any more — one model can no longer tell them apart. Archive three stays **separate** and drives the moving image.

---

## What is in this repository

The code falls into three groups.

### 1. Simulation — teaching the sculpture to move (`/simulation`)

A MuJoCo + PPO reinforcement-learning setup that trains the resin print (`resinprint2.obj`) to drive itself around a track. This is the "release" stage: the sculpture becomes an agent.

| File | Purpose |
|---|---|
| `generate_scene.py` | Reads the OBJ, computes its bounding box, writes `scene.xml` |
| `racing_env.py` | The MuJoCo Gymnasium environment (physics + reward) |
| `train.py` | Trains a PPO agent, saves checkpoints every 5k steps |
| `view.py` | Opens a live 3D viewer with the trained policy |

See [`simulation/README.md`](simulation/README.md) for how to run it.

### 2. Real-time environment — the world for the collected (`/three-js`)

A three.js scene that gives the collected somewhere to be. `collected3.js` builds a volumetric fog/cloud field of 200 camera-facing planes drifting on procedural wind — the atmosphere the sculpture inhabits in the latent-space sequences.

See [`three-js/README.md`](three-js/README.md).

### 3. Custom visuals — TouchDesigner (`/touchdesigner`)

The `.toe` networks used for the moving-image visuals: slit-scans, matrix effects, and the compositing of generated stills into the video. These are binary TouchDesigner project files.

See [`touchdesigner/README.md`](touchdesigner/README.md).

---

## Pipeline overview

```
                Goldsmiths LoRA ─┐
                                 ├─► InstructPix2Pix ─► merged model ─► images
   Russell-Cotes (IP-Adapter) ──┘                                        │
                                                                         ▼
                                                     mesh ─► resin print (the collected)
                                                                         │
                                          ┌──────────────────────────────┤
                                          ▼                              ▼
                          MuJoCo world model (simulation/)   three.js world (three-js/)
                                          │                              │
                                          └──────────► video ◄───────────┘
                                                        ▲
   cemetery photographs ─► WGAN ─────────────────────── ┘
                                                (moving-image/ — TouchDesigner)
```

---

## Tools

Stable Diffusion 1.5, U-Net, DreamBooth LoRA, IP-Adapter, InstructPix2Pix, WGAN, ComfyUI, Python, PyCharm, MuJoCo, Gymnasium, Stable-Baselines3, three.js, TouchDesigner. Models were trained and merged locally, WGAN is trained in MATLAB, generative AI is used in Huggingface, ElevenLabs, Gemini.

---

## Reference

Zylinska, J., 2020. *AI Art: Machine Visions and Warped Dreams*. London: Open Humanities Press.

---


