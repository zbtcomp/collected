# TouchDesigner — custom visuals for the moving image

The `.toe` files are the TouchDesigner networks used to build the visuals for the moving-image work — slit-scans, matrix effects, and the compositing of AI-generated stills and video into the final sequences. These are binary TouchDesigner project files and must be opened in TouchDesigner; they are not human-readable in a text editor.

> **Note:** `.toe` files store the project as a compressed binary. Open them in TouchDesigner to inspect or edit the networks. Version numbers in filenames (e.g. `_35`, `_7`, `_2`) are iteration counters, not part numbers.

---

## Files

| File | Role |
|---|---|
| `collected_7.toe` | Main network for **the collected** — compositing the sculpture/character into its scenes |
| `collection_summer.toe` | Collection sequence — arranging generated artworks together |
| `CFP-video-and-slitscans_35.toe` | Video processing and **slit-scan** treatments (time-smeared frames) |
| `matrixboxtd.toe` | **Matrix / grid** effect network |
| `xrf_2.toe` | Effect / processing network |

*(Roles are described from the project notes; open each in TouchDesigner for the exact operator graph.)*

---

## Requirements

- **TouchDesigner** (099 / 2022+ recommended). The free non-commercial licence is sufficient for these networks.
- Any external media the networks reference — generated stills, the WGAN cemetery video, and other source clips — needs to sit where the `MovieFileIn` operators expect them. If a file path is missing on open, TouchDesigner will flag the operator; re-point it to your local copy of the media.

---

## Opening

1. Launch TouchDesigner.
2. **File → Open** and choose the `.toe` you want, or double-click the file.
3. If any source media shows as missing, select the relevant `MovieFileIn` (or similar) operator and update its file parameter to your local path.

---

## How this fits the project

These networks are the last step before the video: generated images and the WGAN cemetery footage are processed here into the moving image described in the project's *Dreaming in Collections* document. Slit-scans stretch single moments across time; the matrix and effect networks build the latent-space atmosphere the collected moves through. The sound for the video was made separately, by converting a still from the green generated video into audio.
