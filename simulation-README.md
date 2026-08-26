# Simulation — teaching the collected to move

This is the **release** stage of *The Collected*: the resin-printed sculpture stops being an object and becomes an agent. The 3D print (`resinprint2.obj`) is loaded into a MuJoCo physics world as a car, and a PPO reinforcement-learning agent learns to drive it around a track.

Conceptually: the sculpture, generated from a model trained on the collection, is placed inside a *second* model — a world model — and taught to act. An artwork from an AI collection given a body and something to do.

---

## Files

| File | Purpose |
|---|---|
| `generate_scene.py` | Reads `resinprint2.obj`, computes its bounding box, writes `scene.xml` |
| `racing_env.py` | The MuJoCo Gymnasium environment — physics, observations, reward |
| `train.py` | Trains a PPO agent, saves checkpoints every 5,000 steps |
| `view.py` | Opens a live 3D viewer running the trained policy |

`scene.xml` is generated, not hand-written — it is not committed and appears after the first step below.

---

## Requirements

- Python 3.10+
- `resinprint2.obj` in this folder (the mesh of the collected)
- Packages:

```bash
pip install mujoco gymnasium stable-baselines3 torch numpy
```

On Apple Silicon, training uses the `mps` device automatically; otherwise it falls back to CPU. The live viewer must be run with `mjpython` (ships with the `mujoco` package) rather than plain `python`.

---

## How to run

**1. Build the scene from the mesh** (run once, whenever the OBJ changes):

```bash
python generate_scene.py
```

This scales the mesh to roughly 2 m long, works out where the object rests on the ground, and writes `scene.xml` — a grass field with a rectangular road loop, kerbs, a start/finish line, and yellow waypoint cones.

**2. Train:**

```bash
python train.py
```

Trains a PPO agent for 200,000 steps. Checkpoints land in `checkpoints/` every 5,000 steps; the final model is saved as `ppo_racing_final.zip`.

**3. Watch it drive:**

```bash
mjpython view.py                                    # final model
mjpython view.py checkpoints/ppo_racing_5000_steps.zip   # a specific checkpoint
```

The camera locks onto the sculpture and follows it around the loop. Close the window to stop.

---

## How the environment works (`racing_env.py`)

**Observation (16 values):** position (3), orientation quaternion (4), linear velocity (3), angular velocity (3), unit direction to the next waypoint (2), distance to the next waypoint (1).

**Action (2 values):** `[throttle, steer]`, each in `[-1, 1]`.

**Track:** twelve waypoints form a rectangular loop. The agent is rewarded for speed *toward* the next waypoint and given a bonus of 15 each time it reaches one (within 6 m). Leaving the ground is penalised; falling through the floor or driving more than 100 m out ends the episode. Each episode is capped at 2,000 steps.

**Physics notes:** the collected is driven by applying forces rather than wheels — throttle pushes along the object's forward axis (flattened to the horizontal so tilting can't launch it), steering applies torque about the vertical axis, and both linear and angular velocity are damped so it stays controllable. The visible mesh has no collision; a hidden box carries the collision and mass.

---

## Tuning

Training hyperparameters live at the top of `train.py` (learning rate, steps, batch size, discount, entropy). Reward shaping and waypoint spacing live at the top of `racing_env.py` (`WAYPOINTS`, `WAYPOINT_RADIUS`, `WAYPOINT_BONUS`).
