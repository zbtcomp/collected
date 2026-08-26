import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco

# Waypoints around the rectangular track loop (X, Y) in metres.
# The car starts at (0, 0) facing +X, so waypoint 0 is straight ahead.
WAYPOINTS = np.array([
    [ 17,   0],   # end of bottom straight
    [ 20,   5],   # enter right corner
    [ 20,  14],   # mid right side
    [ 20,  23],   # exit right corner
    [ 17,  28],   # enter top straight
    [  0,  28],   # mid top straight
    [-17,  28],   # exit top straight
    [-20,  23],   # enter left corner
    [-20,  14],   # mid left side
    [-20,   5],   # exit left corner
    [-17,   0],   # enter bottom straight
    [  0,   0],   # start / finish
], dtype=np.float32)

WAYPOINT_RADIUS = 6.0   # metres — how close to count as "reached"
WAYPOINT_BONUS  = 15.0  # reward given on each waypoint reached


class CarRacingEnv(gym.Env):
    """
    MuJoCo car-racing env with waypoint-guided rewards.
    The agent drives resinprint2.obj around the rectangular road loop.

    Observation (16):
        pos(3)  quat(4)  linvel(3)  angvel(3)
        + direction-to-next-waypoint(2)  + distance-to-next-waypoint(1)

    Action (2):  [throttle, steer]  in [-1, 1]
    """

    metadata = {"render_modes": ["rgb_array"]}

    def __init__(self, render_mode=None, max_steps=2000):
        super().__init__()
        self.model = mujoco.MjModel.from_xml_path("scene.xml")
        self.data  = mujoco.MjData(self.model)
        self.render_mode = render_mode
        self._max_steps  = max_steps
        self._step_count = 0
        self._renderer   = None

        self._car_id     = self.model.body("car").id
        self._wp_idx     = 0
        self._prev_wp_dist = None

        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(2,), dtype=np.float32
        )
        # pos(3) + quat(4) + linvel(3) + angvel(3) + wp_dir(2) + wp_dist(1) = 16
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(16,), dtype=np.float32
        )

    # ------------------------------------------------------------------
    def _waypoint_obs(self):
        """Returns (unit-vector-to-next-wp [2], distance [1])."""
        pos2d = self.data.qpos[:2]
        to_wp = WAYPOINTS[self._wp_idx] - pos2d
        dist  = float(np.linalg.norm(to_wp))
        direction = (to_wp / dist) if dist > 1e-3 else np.zeros(2, dtype=np.float32)
        return direction.astype(np.float32), np.float32(dist)

    def _get_obs(self):
        pos    = self.data.qpos[:3]
        quat   = self.data.qpos[3:7]
        linvel = self.data.qvel[:3]
        angvel = self.data.qvel[3:6]
        wp_dir, wp_dist = self._waypoint_obs()
        return np.concatenate([pos, quat, linvel, angvel, wp_dir, [wp_dist]],
                              dtype=np.float32)

    def _apply_controls(self, action):
        throttle = float(action[0])
        steer    = float(action[1])
        xmat     = self.data.xmat[self._car_id].reshape(3, 3)

        # Project forward direction onto horizontal plane — prevents tilting from
        # giving the thrust vector an upward component and launching the car.
        fwd = np.array([xmat[0, 0], xmat[1, 0], 0.0])
        norm = np.linalg.norm(fwd)
        if norm > 1e-3:
            fwd /= norm

        # Velocity damping keeps speed bounded without limiting physics
        vel = self.data.qvel[:3]
        drag = -vel * 120.0

        self.data.xfrc_applied[self._car_id] = 0.0
        self.data.xfrc_applied[self._car_id, :3] = fwd * throttle * 7000.0 + drag
        self.data.xfrc_applied[self._car_id, 5]  = steer * 600.0
        # Damp angular velocity to stop spinning
        self.data.xfrc_applied[self._car_id, 3:6] -= self.data.qvel[3:6] * 200.0

    # ------------------------------------------------------------------
    def step(self, action):
        self._apply_controls(action)
        mujoco.mj_step(self.model, self.data)
        self._step_count += 1

        pos    = self.data.qpos[:3]
        vel    = self.data.qvel[:3]
        height = float(pos[2])
        dist   = float(np.linalg.norm(pos[:2]))

        # --- waypoint logic ---
        wp_dir, wp_dist = self._waypoint_obs()
        waypoint_bonus  = 0.0
        if wp_dist < WAYPOINT_RADIUS:
            self._wp_idx   = (self._wp_idx + 1) % len(WAYPOINTS)
            waypoint_bonus = WAYPOINT_BONUS

        # --- reward: speed toward next waypoint + bonus ---
        normal_z = 0.336
        on_ground = height < normal_z + 0.4
        toward_speed = float(np.dot(vel[:2], wp_dir))
        reward = (max(0.0, toward_speed) if on_ground else -2.0) + waypoint_bonus

        terminated = bool(height < -0.5 or dist > 100.0)
        truncated  = self._step_count >= self._max_steps

        return self._get_obs(), reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        self._step_count = 0
        self._wp_idx     = 0
        return self._get_obs(), {}

    def render(self):
        if self.render_mode != "rgb_array":
            return None
        if self._renderer is None:
            self._renderer = mujoco.Renderer(self.model, height=480, width=640)
        self._renderer.update_scene(self.data)
        return self._renderer.render()

    def close(self):
        if self._renderer is not None:
            self._renderer.close()
            self._renderer = None
