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

I acknowledge the use of artificial intelligence tools in the development of this project. AI models were used for generating code, refining text, generating visual and audio assets, and brainstorming concepts. All AI-generated content was heavily curated, edited, and directed by the author, who takes full responsibility for the final original work, research, and arguments presented in this submission.
Akten, M.S. (2021). Deep visual instruments: Realtime continuous, meaningful human control over deep neural networks for creative expression. PhD thesis. Goldsmiths, University of London.
Here is the text formatted cleanly as a Markdown list, perfect for dropping directly into your repository's `README.md` or documentation file. As requested, the text itself has not been changed.

### AI Declaration

> I acknowledge the use of artificial intelligence tools in the development of this project. AI models were used for generating code, refining text, generating visual and audio assets, and brainstorming concepts. All AI-generated content was heavily curated, edited, and directed by the author, who takes full responsibility for the final original work, research, and arguments presented in this submission.

### Bibliography

* Akten, M.S. (2021). Deep visual instruments: Realtime continuous, meaningful human control over deep neural networks for creative expression. PhD thesis. Goldsmiths, University of London.
* Al-Sabah, B. I. (n.d.). Bassam Issa Al-Sabah. [online] Available at: [https://bassamissa.xyz/](https://bassamissa.xyz/) and [https://bassamissa.xyz/?page_id=572](https://bassamissa.xyz/?page_id=572).
* Böhler, A. (2017). Immanence: A life… Friedrich Nietzsche 1. Performance Philosophy, 3(3), pp.576-595.
* Chun, W.H.K. (2011). Programmed visions: Software and memory. Cambridge, MA: MIT Press.
* Cohn, J. (2017). What algorithms want: Imagination in the age of computing. Canadian Journal of Film Studies, 26(2), pp.138-140.
* Crawford, K. (2021). The atlas of AI: Power, politics, and the planetary costs of artificial intelligence. New Haven: Yale University Press.
* Crispin, S. (n.d.). Data-Masks. [online] Available at: [https://www.sterlingcrispin.com/data-masks.html](https://www.sterlingcrispin.com/data-masks.html).
* Cunningham, G.W. (1914). Bergson's conception of duration. The Philosophical Review, 23(5), pp.525-539. Available at: [https://doi.org/10.2307/2178586](https://doi.org/10.2307/2178586) [Accessed 21 May 2026].
* de Vries, P. (2020). Algorithmic anxiety in contemporary art: A Kierkegaardian inquiry into the imaginary of possibility. Amsterdam: Institute of Network Cultures.
* Farocki, H. (2003). Eye / Machine III. [video] YouTube. Available at: [https://youtu.be/eRisum_xq_A](https://youtu.be/eRisum_xq_A).
* Farocki, H. (2014). Parallel I-IV. [video] YouTube. Available at: [https://youtu.be/k3tpEFuTvzc](https://youtu.be/k3tpEFuTvzc).
* Feaster, P. (2023). Adventures in Stable Diffusion #4: One Step at a Time. Griffonage. [online] 12 Jul. Available at: [https://griffonagedotcom.wordpress.com/2023/07/12/adventures-in-stable-diffusion-4-one-step-at-a-time/](https://griffonagedotcom.wordpress.com/2023/07/12/adventures-in-stable-diffusion-4-one-step-at-a-time/).
* Feaster, P. (2023). Creating Synesthetic Sound-Pictures with Generative AI. Griffonage. [online] 23 Dec. Available at: [https://griffonagedotcom.wordpress.com/2023/12/23/creating-synesthetic-sound-pictures-with-generative-ai/](https://griffonagedotcom.wordpress.com/2023/12/23/creating-synesthetic-sound-pictures-with-generative-ai/).
* Feral File (n.d.). Ex Nihilo. [online] Available at: [https://feralfile.com/exhibitions/shows/ex-nihilo-a3c?tab=essay](https://feralfile.com/exhibitions/shows/ex-nihilo-a3c?tab=essay).
* Fischer, U. (n.d.). Shucks & Aww. [online] Available at: [https://ursfischer.com/exhibitions/shucks%20%26%20Aww](https://ursfischer.com/exhibitions/shucks%20%26%20Aww).
* Fly, J. (2019). Charlie Chaplin, Tree or Man?. [video] YouTube. Available at: [https://youtu.be/_7zBO6GenkM](https://youtu.be/_7zBO6GenkM).
* Fly, J. (2019). The Rise and Fall of Civilizations, A BigGAN Latent. [video] YouTube. Available at: [https://youtu.be/mG1EItgWoBs](https://youtu.be/mG1EItgWoBs).
* Friend, S. (n.d.). Perverse Affordances. [online] Available at: [https://isthisa.com/perverseaffordances](https://isthisa.com/perverseaffordances).
* Friend, S. (n.d.). What kind of clock is an LLM? Is this an art? [online] Available at: [https://isthisanart.substack.com/p/what-kind-of-clock-is-an-llm](https://isthisanart.substack.com/p/what-kind-of-clock-is-an-llm).
* Galloway, A.R. (2010). The anti-language of new media. Discourse, 32(3), pp.276-284.
* Godard, J.-L. (2018). The Image Book (Le Livre d'image). [Film].
* Goldsmiths, University of London (n.d.). Goldsmiths Textile Collection: Artists and Makers. [online] Available at: [https://www.gold.ac.uk/textile-collection/](https://www.gold.ac.uk/textile-collection/).
* Google Experiments (n.d.). Scribbling Speech. [online] Available at: [https://experiments.withgoogle.com/scribbling-speech](https://experiments.withgoogle.com/scribbling-speech).
* Graw, I. and Lajer-Burcharth, E. (eds.) (2016). Painting beyond Itself: The Medium in the Post-medium Condition. Berlin: Sternberg Press.
* Habit of Philosophy (2018). The world as remainder. [Blog] Medium. Available at: [https://medium.com/@habitofphilosophy/the-world-as-remainder-8a274d7792df](https://medium.com/@habitofphilosophy/the-world-as-remainder-8a274d7792df) [Accessed 21 May 2026].
* Hartmann, N. (n.d.). Nina Hartmann. [online] Available at: [https://www.ninahartmann.com/](https://www.ninahartmann.com/).
* Hui, Y. (2016). On the existence of digital objects. Minneapolis: University of Minnesota Press.
* Klingemann, M. (2016). X Degrees of Separation. [online] Quasimondo. Available at: [https://quasimondo.com/2016/11/05/x-degrees-of-separation-2016/](https://quasimondo.com/2016/11/05/x-degrees-of-separation-2016/) and [https://artsexperiments.withgoogle.com/xdegrees/ogGvLdZg_9FlIQ/1gHp7gNaErg8lA](https://artsexperiments.withgoogle.com/xdegrees/ogGvLdZg_9FlIQ/1gHp7gNaErg8lA).
* Lee, R. (2019). Uncertainties in the algorithmic image. Journal of Science and Technology of the Arts, 11(2), pp.36–40. Available at: [https://doi.org/10.7559/citarj.v11i2.661](https://doi.org/10.7559/citarj.v11i2.661) [Accessed 21 May 2026].
* Loclair, C. M. (n.d.). Narciss. [online] Available at: [https://christianmioloclair.com/narciss](https://christianmioloclair.com/narciss). (Note: ‘Narciss is both an artistic intervention and artificial intelligence whose only purpose is to investigate itself, referencing a synthetic model of self-awareness, a fragment of artificial narcissism and a fictional character in its own autobiographical narrations.’)
* Lulu [@luluixixix] (2019). [Twitter] 4 Nov. Available at: [https://x.com/luluixixix/status/1191414379989876737](https://x.com/luluixixix/status/1191414379989876737).
* Lulu [@luluixixix] (2020). [Twitter] 16 Feb. Available at: [https://x.com/luluixixix/status/1229424170662072322](https://x.com/luluixixix/status/1229424170662072322).
* Manovich, L. (2013). Software takes command. New York: Bloomsbury Academic.
* May-Hobbs, M. (2023). Machine vision and encoded behaviour in Harun Farocki's later work. Film-Philosophy, 27(2), pp.301-325. Available at: [https://doi.org/10.3366/film.2023.0231](https://doi.org/10.3366/film.2023.0231) [Accessed 21 May 2026].
* Mizuochi, M. (2025). Green Diffusion. [online] Available at: [https://mizumasa.net/work32GreenDiffusionEn.html](https://mizumasa.net/work32GreenDiffusionEn.html).
* ML Art (n.d.). Machine Learning Art. [online] Available at: [https://mlart.co/](https://mlart.co/).
* Moren, B. (n.d.). Clonal Colony. [online] Available at: [https://benmoren.com/environments/clonal-colony/](https://benmoren.com/environments/clonal-colony/).
* Moving Image Artists (n.d.). Moving Image Artists. [online] Available at: [https://movingimageartists.co.uk/](https://movingimageartists.co.uk/).
* Müller, J. (2023). The computer: A history from the 17th century to today. Cologne: Taschen.
* Murray, J. H. (2017). Hamlet on the Holodeck: The Future of Narrative in Cyberspace. Updated edn. Cambridge, MA: MIT Press.
* Nature Morte (2018). Gradient Descent. [online] Available at: [https://naturemorte.com/exhibitions/gradientdescent/](https://naturemorte.com/exhibitions/gradientdescent/).
* Negarestani, R. (2018). Intelligence and spirit. Falmouth: Urbanomic.
* Pamuk, O. (2012). The innocence of objects. New York: Abrams.
* Punday, D. (2015). Computing as writing. Minneapolis: University of Minnesota Press.
* Qiu, H. (n.d.). Image to Audio. [online] Available at: [https://image-to-audio.pages.dev/](https://image-to-audio.pages.dev/).
* Reas, C., McWilliams, C. and LUST (2010). Form+Code in design, art, and architecture. New York: Princeton Architectural Press.
* Rodriguez, H. (2018). Theorem 9. [online] Available at: [https://concept-script.com/theorem9/index.html](https://concept-script.com/theorem9/index.html).
* Russell-Cotes Art Gallery & Museum (n.d.). Collections. [online] Available at: [https://russellcotes.com/collections/](https://russellcotes.com/collections/).
* Salavon, J. (n.d.). Jason Salavon Studio. [online] Available at: [http://salavon.com/](http://salavon.com/).
* Saunders, M. (n.d.). Matt Saunders. [online] Marian Goodman Gallery. Available at: [https://www.mariangoodman.com/artists/61-matt-saunders/](https://www.mariangoodman.com/artists/61-matt-saunders/).
* Slizewicz, G. (n.d.). Decors. [online] Available at: [https://guillaumeslizewicz.com/studio/decors/](https://guillaumeslizewicz.com/studio/decors/).
* Steinfeld, K. (n.d.). Kyle Steinfeld. [online] AI Architects. Available at: [https://aiarchitects.org/portfolio/kyle-steinfeld/](https://aiarchitects.org/portfolio/kyle-steinfeld/).
* Thompson, N. (n.d.). Works. [online] Available at: [https://nyethompson.net/works/index.html](https://nyethompson.net/works/index.html).
* Töyrylä, H. (2019). Taming the GAN. [online] Liipetti. Available at: [https://liipetti.net/visual/taming-the-gan/](https://liipetti.net/visual/taming-the-gan/).
* transmediale (n.d.). The finiteness of algorithms. [online] transmediale archive. Available at: [https://archive.transmediale.de/content/the-finiteness-of-algorithms](https://archive.transmediale.de/content/the-finiteness-of-algorithms) [Accessed 21 May 2026].
* VADS (n.d.). Goldsmiths Textile Collection. [online] Available at: [https://vads.ac.uk](https://vads.ac.uk).
* Wasielewski, A. (2023). Computational formalism: Art history and machine learning. Cambridge, MA: MIT Press.
* Weiss, S. (n.d.). The Chair Project: Generating a Classic. [online] Available at: [https://steffen-weiss.design/the-chair-project-generating-a-classic](https://steffen-weiss.design/the-chair-project-generating-a-classic).
* Zylinska, J. (2020). AI art: Machine visions and warped dreams. London: Open Humanities Press.
