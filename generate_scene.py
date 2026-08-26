"""
Reads resinprint2.obj, computes its bounding box, and writes scene.xml.
Run this once before training: venv/bin/python generate_scene.py
"""
import numpy as np

OBJ_FILE = "resinprint2.obj"
SCALE = 0.01  # object becomes ~2 m × 1.1 m × 0.65 m in simulation

verts = []
with open(OBJ_FILE) as f:
    for line in f:
        if line.startswith("v "):
            parts = line.split()
            verts.append([float(parts[1]), float(parts[2]), float(parts[3])])

v = np.array(verts)
mn, mx = v.min(axis=0), v.max(axis=0)
center = (mn + mx) / 2
size_m = (mx - mn) * SCALE

half = size_m / 2
start_z = half[2] + 0.01

print(f"Mesh centre (raw units): {center.round(3)}")
print(f"Car size in sim:  {size_m.round(3)} m  (L × W × H)")
print(f"Car starts at z = {start_z:.3f} m")

xml = f"""<mujoco model="car_racing">
  <compiler meshdir="." autolimits="true"/>
  <option timestep="0.005" gravity="0 0 -9.81"/>

  <asset>
    <mesh name="car_mesh" file="{OBJ_FILE}"
          refpos="{center[0]:.4f} {center[1]:.4f} {center[2]:.4f}"
          scale="{SCALE} {SCALE} {SCALE}"/>

    <!-- Grass ground -->
    <texture name="grass_tex" type="2d" builtin="checker"
             width="512" height="512"
             rgb1="0.18 0.42 0.18" rgb2="0.14 0.35 0.14"/>
    <material name="grass_mat" texture="grass_tex" texrepeat="30 30" reflectance="0.05"/>

    <!-- Road materials -->
    <material name="asphalt"    rgba="0.15 0.15 0.15 1"/>
    <material name="kerb_red"   rgba="0.80 0.10 0.10 1"/>
    <material name="kerb_white" rgba="0.95 0.95 0.95 1"/>
    <material name="startline"  rgba="0.95 0.95 0.95 1"/>
  </asset>

  <worldbody>
    <light pos="0 15 20" dir="0 -0.5 -1" diffuse="0.95 0.95 0.90" specular="0.3 0.3 0.3"/>
    <light pos="-15 -5 10" dir="1 0.3 -1" diffuse="0.40 0.40 0.45"/>

    <!-- Grass ground -->
    <geom name="floor" type="plane" size="80 80 0.1"
          material="grass_mat" friction="1.2 0.02 0.002" contype="1" conaffinity="1"/>

    <!-- ================================================================
         ROAD LOOP  (visual only — no collision so car drives on floor)
         Rectangle: X ±20 m, Y 0 to 28 m  Road width 6 m (half=3)
         ================================================================ -->

    <!-- Bottom straight  (car starts here, drives in +X direction) -->
    <geom type="box" pos="0 0 0.004"    size="17 3 0.004" material="asphalt" contype="0" conaffinity="0"/>
    <!-- Top straight -->
    <geom type="box" pos="0 28 0.004"   size="17 3 0.004" material="asphalt" contype="0" conaffinity="0"/>
    <!-- Left side -->
    <geom type="box" pos="-20 14 0.004" size="3 11 0.004" material="asphalt" contype="0" conaffinity="0"/>
    <!-- Right side -->
    <geom type="box" pos="20 14 0.004"  size="3 11 0.004" material="asphalt" contype="0" conaffinity="0"/>
    <!-- Four corners -->
    <geom type="box" pos="-20  0 0.004" size="3 3 0.004"  material="asphalt" contype="0" conaffinity="0"/>
    <geom type="box" pos=" 20  0 0.004" size="3 3 0.004"  material="asphalt" contype="0" conaffinity="0"/>
    <geom type="box" pos="-20 28 0.004" size="3 3 0.004"  material="asphalt" contype="0" conaffinity="0"/>
    <geom type="box" pos=" 20 28 0.004" size="3 3 0.004"  material="asphalt" contype="0" conaffinity="0"/>

    <!-- Kerbs — alternating red / white strips along the edges -->
    <!-- Bottom straight outer edge -->
    <geom type="box" pos="-12 -3.1 0.006" size="2 0.15 0.006" material="kerb_red"   contype="0" conaffinity="0"/>
    <geom type="box" pos=" -8 -3.1 0.006" size="2 0.15 0.006" material="kerb_white" contype="0" conaffinity="0"/>
    <geom type="box" pos=" -4 -3.1 0.006" size="2 0.15 0.006" material="kerb_red"   contype="0" conaffinity="0"/>
    <geom type="box" pos="  0 -3.1 0.006" size="2 0.15 0.006" material="kerb_white" contype="0" conaffinity="0"/>
    <geom type="box" pos="  4 -3.1 0.006" size="2 0.15 0.006" material="kerb_red"   contype="0" conaffinity="0"/>
    <geom type="box" pos="  8 -3.1 0.006" size="2 0.15 0.006" material="kerb_white" contype="0" conaffinity="0"/>
    <geom type="box" pos=" 12 -3.1 0.006" size="2 0.15 0.006" material="kerb_red"   contype="0" conaffinity="0"/>

    <!-- Start / finish line -->
    <geom type="box" pos="0 0 0.007" size="0.25 3 0.001" material="startline" contype="0" conaffinity="0"/>

    <!-- ================================================================
         WAYPOINT MARKERS  (yellow cones — visual only)
         Matching the WAYPOINTS list in racing_env.py
         ================================================================ -->
    <geom type="cylinder" pos=" 17  0  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos=" 20  5  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos=" 20 14  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos=" 20 23  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos=" 17 28  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="  0 28  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="-17 28  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="-20 23  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="-20 14  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="-20  5  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="-17  0  0.4" size="0.4 0.4" rgba="1 0.9 0 0.9" contype="0" conaffinity="0"/>
    <geom type="cylinder" pos="  0  0  0.4" size="0.4 0.4" rgba="1 0.3 0 0.9" contype="0" conaffinity="0"/>

    <!-- ================================================================
         THE CAR
         ================================================================ -->
    <body name="car" pos="0 0 {start_z:.4f}">
      <freejoint name="car_free"/>
      <geom name="car_visual" type="mesh" mesh="car_mesh"
            rgba="1 1 1 1" contype="0" conaffinity="0" density="0"/>
      <geom name="car_col" type="box"
            size="{half[0]:.4f} {half[1]:.4f} {half[2]:.4f}"
            mass="400" friction="0.8 0.01 0.001"
            rgba="0 0 0 0" contype="1" conaffinity="1"/>
    </body>
  </worldbody>
</mujoco>
"""

with open("scene.xml", "w") as f:
    f.write(xml)

print("scene.xml written — ready to train!")
