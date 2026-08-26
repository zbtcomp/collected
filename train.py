"""
Train a PPO agent to drive resinprint2.obj around a flat track.
Usage:  venv/bin/python train.py
"""
import os
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback
from racing_env import CarRacingEnv

if not os.path.exists("scene.xml"):
    raise FileNotFoundError("Run  venv/bin/python generate_scene.py  first.")

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Device: {device}")

env = CarRacingEnv()
check_env(env, warn=True)

os.makedirs("checkpoints", exist_ok=True)

checkpoint_cb = CheckpointCallback(
    save_freq=5_000,
    save_path="checkpoints/",
    name_prefix="ppo_racing",
)

model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.005,
    verbose=1,
    device=device,
)

print("Training for 200 000 steps …")
model.learn(total_timesteps=200_000, callback=checkpoint_cb)
model.save("ppo_racing_final")
print("Saved → ppo_racing_final.zip")
