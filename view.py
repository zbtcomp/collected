"""
Watch the trained agent drive resinprint2.obj.
Usage:
  venv/bin/mjpython view.py                              # final model
  venv/bin/mjpython view.py checkpoints/ppo_racing_5000_steps.zip
"""
import sys
import time
from stable_baselines3 import PPO
from racing_env import CarRacingEnv
import mujoco
import mujoco.viewer

model_path = sys.argv[1] if len(sys.argv) > 1 else "ppo_racing_final"
print(f"Loading: {model_path}")
model = PPO.load(model_path)
env = CarRacingEnv()
obs, _ = env.reset()

with mujoco.viewer.launch_passive(env.model, env.data) as viewer:
    # Lock camera onto the car body
    viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
    viewer.cam.trackbodyid = env.model.body("car").id
    viewer.cam.distance = 8.0    # metres behind/above
    viewer.cam.elevation = -25   # degrees (negative = looking down slightly)
    viewer.cam.azimuth = 90      # side angle; 0 = behind, 90 = side

    print("Viewer open — close the window to stop.")
    while viewer.is_running():
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        viewer.sync()
        time.sleep(env.model.opt.timestep)
        if terminated or truncated:
            obs, _ = env.reset()
