"""
Procedural Lion (v14) - Standing on 4 legs:
- Normal standing posture (not hunting crouch)
- Horizontal body (same height front and rear)
- Head raised up
- All 4 legs vertical
- V5 face design maintained

Run:
  pip install numpy scikit-image trimesh
  python lion_standing_v14.py

Output:
  lion_standing_v14.stl
"""

import numpy as np
from skimage import measure
import trimesh

OUTPUT = "lion_standing_v14.stl"

# Quality
N = 200

# Bounds
xmin, xmax = -120, 150
ymin, ymax = -85, 85
zmin, zmax = 0, 120

# Balanced ISO
ISO = 0.36

xs = np.linspace(xmin, xmax, N, dtype=np.float32)
ys = np.linspace(ymin, ymax, N, dtype=np.float32)
zs = np.linspace(zmin, zmax, N, dtype=np.float32)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")

def gauss(cx, cy, cz, sx, sy, sz, w=1.0):
    dx = (X - cx) / sx
    dy = (Y - cy) / sy
    dz = (Z - cz) / sz
    return w * np.exp(-(dx*dx + dy*dy + dz*dz))

F = np.zeros_like(X, dtype=np.float32)

# ============================================================
# TORSO - HORIZONTAL (same height front and rear)
# ============================================================
# Front chest (RAISED to same level as rear)
F += gauss( 35,  0, 42, 26, 14, 13, 0.58)  # raised from 28 to 42
# Mid torso
F += gauss(  5,  0, 44, 31, 15, 14, 0.60)  # raised from 32 to 44
# Rear torso (SAME height as front)
F += gauss(-30,  0, 44, 28, 14, 15, 0.58)  # raised from 38 to 44
# Hind
F += gauss(-55,  0, 44, 22, 13, 14, 0.54)  # raised from 40 to 44

# Connections
F += gauss( 20,  0, 43, 21, 13, 12, 0.22)  # raised from 30 to 43
F += gauss(-15,  0, 44, 24, 14, 13, 0.22)  # raised from 35 to 44

# Belly (subtle)
F -= gauss(  5,  0, 30, 46, 19, 10, 0.20)  # raised from 18 to 30

# ============================================================
# NECK - RAISED to connect with higher head
# ============================================================
F += gauss( 55,  0, 48, 15, 10, 12, 0.50)  # raised from 28 to 48
F += gauss( 42,  0, 46, 16, 11, 14, 0.55)  # raised from 30 to 46

# ============================================================
# HEAD - RAISED (standing position)
# Using v5 design, adjusted for higher position
# ============================================================
# Main skull
F += gauss( 66,  0, 58, 16, 12, 14, 1.02)  # raised from 28 to 58
F += gauss( 68,  10, 55, 10,  7, 10, 0.52)  # raised from 25 to 55
F += gauss( 68, -10, 55, 10,  7, 10, 0.52)
F += gauss( 76,  0, 63, 10,  7,  6, 0.22)  # raised from 33 to 63

# Snout
F += gauss( 80,  0, 53, 13,  8.5, 9.0, 0.86)  # raised from 23 to 53
F += gauss( 90,  0, 50,  9,  5.8, 6.5, 0.74)  # raised from 20 to 50
F += gauss( 96,  0, 49,  6.8, 4.6, 5.4, 0.50)  # raised from 19 to 49

# Snout sides
F -= gauss( 90,  8.0, 50, 10,  4.0, 7.0, 0.16)  # raised from 20 to 50
F -= gauss( 90, -8.0, 50, 10,  4.0, 7.0, 0.16)
F -= gauss( 95,  0, 54,  7.0, 4.5, 3.2, 0.18)  # raised from 24 to 54

# Nose
F += gauss( 95,  0, 52.5, 4.8, 3.2, 3.0, 0.26)  # raised from 22.5 to 52.5
F -= gauss( 98,  2.2, 50.8, 2.2, 1.2, 1.2, 0.16)  # raised from 20.8 to 50.8
F -= gauss( 98, -2.2, 50.8, 2.2, 1.2, 1.2, 0.16)

# Lower jaw
F += gauss( 84,  0, 43.5, 14,  7.5, 5.2, 0.54)  # raised from 13.5 to 43.5
F += gauss( 78,  0, 42.5, 15,  9.0, 6.0, 0.30)  # raised from 12.5 to 42.5
F -= gauss( 92,  0, 46.0, 7.0, 2.4, 1.8, 0.22)  # raised from 16.0 to 46.0

# Ears
F += gauss( 68,  11.5, 70, 5.5, 3.8, 6.5, 0.42)  # raised from 40 to 70
F += gauss( 68, -11.5, 70, 5.5, 3.8, 6.5, 0.42)
F += gauss( 66,  12.5, 75, 3.8, 2.8, 4.8, 0.24)  # raised from 45 to 75
F += gauss( 66, -12.5, 75, 3.8, 2.8, 4.8, 0.24)

# Eye sockets
F -= gauss( 82,  8.0, 58, 2.9, 2.0, 2.0, 0.25)  # raised from 28 to 58
F -= gauss( 82, -8.0, 58, 2.9, 2.0, 2.0, 0.25)

# ============================================================
# ALL 4 LEGS - VERTICAL and SAME HEIGHT
# ============================================================

# FRONT LEFT leg
cx, cy, cz_base = 40, 13, 40  # raised from 26 to 40
F += gauss(cx,     cy, cz_base, 9.5, 6.8, 14, 0.54)
F += gauss(cx+2,   cy, cz_base-10, 8.5, 6.2, 11, 0.58)
F += gauss(cx+4,   cy, cz_base-18, 7.8, 6.0, 8, 0.60)
F += gauss(cx+6,   cy, cz_base-24, 7.0, 6.5, 3.5, 0.64)

# FRONT RIGHT leg
cx, cy, cz_base = 40, -13, 40
F += gauss(cx,     cy, cz_base, 9.5, 6.8, 14, 0.54)
F += gauss(cx+2,   cy, cz_base-10, 8.5, 6.2, 11, 0.58)
F += gauss(cx+4,   cy, cz_base-18, 7.8, 6.0, 8, 0.60)
F += gauss(cx+6,   cy, cz_base-24, 7.0, 6.5, 3.5, 0.64)

# REAR LEFT leg (raised to match front)
cx, cy, cz_base = -38, 13, 40  # raised from 30 to 40
F += gauss(cx,     cy, cz_base, 9.5, 6.8, 14, 0.54)
F += gauss(cx+6,   cy, cz_base-10, 8.5, 6.2, 11, 0.58)
F += gauss(cx+11,  cy, cz_base-18, 7.8, 6.0, 8, 0.60)
F += gauss(cx+15,  cy, cz_base-24, 7.0, 6.5, 3.5, 0.64)

# REAR RIGHT leg
cx, cy, cz_base = -38, -13, 40
F += gauss(cx,     cy, cz_base, 9.5, 6.8, 14, 0.54)
F += gauss(cx+6,   cy, cz_base-10, 8.5, 6.2, 11, 0.58)
F += gauss(cx+11,  cy, cz_base-18, 7.8, 6.0, 8, 0.60)
F += gauss(cx+15,  cy, cz_base-24, 7.0, 6.5, 3.5, 0.64)

# Gaps
F -= gauss( 40,  0, 26, 10, 6, 13, 0.16)  # raised from 14 to 26
F -= gauss(-38,  0, 26, 11, 6, 14, 0.16)  # raised from 16 to 26

# ============================================================
# TAIL - Adjusted for standing position
# ============================================================
tail_segments = [
    (-68,  0, 48),   # raised from 42 to 48
    (-82,  0, 52),   # raised from 44 to 52
    (-95,  0, 60),   # raised from 50 to 60
    (-105, 0, 70),   # raised from 59 to 70
    (-110, 0, 80),   # raised from 68 to 80
    (-108, 0, 88),   # raised from 76 to 88
]
tail_sizes = [
    (9.0, 5.8, 5.8),
    (8.5, 5.5, 5.5),
    (8.0, 5.2, 5.2),
    (7.5, 4.9, 4.9),
    (7.0, 4.6, 4.6),
    (6.5, 4.4, 4.4),
]

for (cx, cy, cz), (sx, sy, sz) in zip(tail_segments, tail_sizes):
    F += gauss(cx, cy, cz, sx, sy, sz, 0.36)

F += gauss(-62, 0, 46, 11, 8.2, 8.2, 0.18)  # raised from 40 to 46
F += gauss(-106, 0, 91, 7.2, 6.2, 6.2, 0.33)  # raised from 79 to 91
F += gauss(-102, 0, 89, 5.8, 5.0, 5.0, 0.18)  # raised from 77 to 89

# ============================================================
# MANE - Adjusted for raised head
# ============================================================
rng = np.random.default_rng(808)

# Base volume (raised)
F += gauss( 77,  0, 56, 22, 20, 20, 0.26)  # raised from 32 to 56
F += gauss( 68,  0, 58, 26, 22, 18, 0.23)  # raised from 34 to 58
F += gauss( 87,  0, 54, 18, 18, 16, 0.24)  # raised from 30 to 54

# HIGH ridge
for t in np.linspace(0, 1, 14):
    cx = 90 - 40*t
    cz = 80 - 12*t  # raised from 56 to 80
    F += gauss(cx, 0, cz, 11, 4.8, 6.8, 0.09)

# Upper mass
F += gauss( 82,  0, 70, 18, 16, 14, 0.20)  # raised from 46 to 70
F += gauss( 75,  0, 74, 16, 14, 12, 0.17)  # raised from 50 to 74
F += gauss( 85,  9, 68, 13, 9, 11, 0.15)   # raised from 44 to 68
F += gauss( 85, -9, 68, 13, 9, 11, 0.15)

# Directional strands
strand_base = np.array([84.0, 0.0, 64.0], dtype=np.float32)  # raised from 40 to 64
for _ in range(360):
    xx = -(10.0 + 46.0 * rng.random())
    yy = (36.0 * (2*rng.random() - 1)) * 0.72
    zz_base = -(5.0 + 24.0 * rng.random())
    if rng.random() < 0.32:
        zz = abs(zz_base) * 0.6
    else:
        zz = zz_base
    
    p = strand_base + np.array([xx, yy, zz], dtype=np.float32)
    
    if not (34.0 < p[2] < 94.0):  # adjusted range
        continue
    if p[0] > 100.0:
        continue
    
    side_mult = 1.0 + (0.35 if p[1] > 0 else 0.0)
    
    sx = 15.5 + 6.0 * rng.random()
    sy = 3.5  + 1.2 * rng.random()
    sz = 6.0  + 1.9 * rng.random()
    w  = 0.11 * side_mult
    
    F += gauss(float(p[0]), float(p[1]), float(p[2]), sx, sy, sz, w)

# Chest beard
beard_base = np.array([74.0, 0.0, 52.0], dtype=np.float32)  # raised from 28 to 52
for _ in range(150):
    xx = -(5.0 + 28.0 * rng.random())
    yy = (26.0 * (2*rng.random() - 1)) * 0.52
    zz = -(12.0 + 34.0 * rng.random())
    p = beard_base + np.array([xx, yy, zz], dtype=np.float32)
    
    if not (30.0 < p[2] < 62.0):  # adjusted range
        continue
    if p[0] > 96.0:
        continue
    
    F += gauss(float(p[0]), float(p[1]), float(p[2]), 17.0, 3.9, 8.8, 0.09)

# Side mane
F += gauss( 78,  17, 58, 11, 6.2, 9.5, 0.10)  # raised from 34 to 58
F += gauss( 78, -17, 58, 11, 6.2, 9.5, 0.10)
F += gauss( 70,  19, 60, 13, 6.8, 11, 0.08)   # raised from 36 to 60
F += gauss( 70, -19, 60, 13, 6.8, 11, 0.08)

# Texture layers
for _ in range(85):
    angle = rng.random() * 2 * np.pi
    radius = 17.0 + 11.0 * rng.random()
    px = 80.0 + radius * np.cos(angle)
    py = radius * np.sin(angle) * 0.74
    pz = 66.0 + 7.5 * rng.random()  # raised from 42 to 66
    
    if pz < 52 or pz > 86:  # adjusted range
        continue
    if px > 98.0:
        continue
    
    F += gauss(float(px), float(py), float(pz),
               10.0 + 3.8*rng.random(),
               2.9 + 0.9*rng.random(),
               5.0 + 1.7*rng.random(),
               0.07)

# ============================================================
# EXTRACT MESH
# ============================================================
verts, faces, normals, values = measure.marching_cubes(
    F, level=ISO, spacing=(xs[1]-xs[0], ys[1]-ys[0], zs[1]-zs[0])
)
verts[:, 0] += xmin
verts[:, 1] += ymin
verts[:, 2] += zmin

mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=True)

# Cleanup
try:
    mesh.update_faces(mesh.nondegenerate_faces())
except Exception:
    try:
        mesh.remove_degenerate_faces()
    except Exception:
        pass

try:
    mesh.update_faces(mesh.unique_faces())
except Exception:
    try:
        mesh.remove_duplicate_faces()
    except Exception:
        pass

mesh.remove_unreferenced_vertices()
try:
    mesh.process(validate=True)
except Exception:
    mesh.process()

# Ground
mesh.apply_translation([0, 0, -mesh.bounds[0][2]])

# Largest component
parts = list(mesh.split(only_watertight=False))
if len(parts) > 1:
    def score(m):
        try:
            v = float(m.volume)
            if np.isfinite(v) and v > 0:
                return v
        except Exception:
            pass
        return float(len(m.faces))
    mesh = max(parts, key=score)

mesh.export(OUTPUT)
print(f"Exported: {OUTPUT}")
print(f"Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")