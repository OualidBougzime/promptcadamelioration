"""
Miura-like faceted pattern on a SOLID cylinder (filled, with top & bottom caps) - STL mesh generator.
No command-line arguments needed.

Default output: miura_cylinder_40x100_solid_v7.stl

You can tweak parameters by editing this file (RELIEF, N_COLS, N_ROWS, etc.).
"""

import math

# ---------------- Parameters (mm) ----------------
OUTER_DIAM = 40.0
R0 = OUTER_DIAM / 2.0
H = 100.0

RELIEF = 1.8       # radial displacement amplitude (mm) for folds
N_COLS = 18        # pattern repeats around circumference
N_ROWS = 14        # pattern repeats along height
TWIST  = 0.5       # row staggering (Miura phase shift)

# Mesh resolution (higher = smoother, heavier STL)
SEG_U = N_COLS * 2
SEG_V = N_ROWS * 2

OUTPUT_PATH = "miura_cylinder_40x100_solid_v7.stl"

# ---------------- Miura-like heightfield ----------------
def heightfield(u, v):
    """
    Miura-like piecewise-linear faceting on [0,1]x[0,1]
    u: around circumference
    v: along height
    """
    cu = u * N_COLS
    cv = v * N_ROWS

    # stagger alternate rows
    cu -= (int(math.floor(cv)) % 2) * TWIST

    iu = int(math.floor(cu)) % N_COLS
    iv = int(math.floor(cv))
    fu = cu - math.floor(cu)  # 0..1
    fv = cv - math.floor(cv)  # 0..1

    # mountain/valley alternation
    sgn = 1.0 if ((iu + iv) % 2 == 0) else -1.0

    # faceted "tent" with a diagonal crease (2 triangles per cell)
    if fu + fv < 1.0:
        h = fu + fv
    else:
        h = 2.0 - (fu + fv)

    h = (h - 0.5) * 2.0  # ~[-1, +1]
    return sgn * h

def write_facet(f, v1, v2, v3):
    ux, uy, uz = (v2[i]-v1[i] for i in range(3))
    vx, vy, vz = (v3[i]-v1[i] for i in range(3))
    nx = uy*vz - uz*vy
    ny = uz*vx - ux*vz
    nz = ux*vy - uy*vx
    ln = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
    nx/=ln; ny/=ln; nz/=ln
    f.write(f"  facet normal {nx} {ny} {nz}\n")
    f.write("    outer loop\n")
    f.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
    f.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
    f.write(f"      vertex {v3[0]} {v3[1]} {v3[2]}\n")
    f.write("    endloop\n")
    f.write("  endfacet\n")

# ---------------- Build outer surface vertices ----------------
outer = []
for j in range(SEG_V + 1):
    v = j / SEG_V
    z = H * v
    row = []
    for i in range(SEG_U + 1):
        u = i / SEG_U
        theta = 2.0 * math.pi * u
        h = heightfield(u, v) * RELIEF
        r = R0 + h
        row.append((r * math.cos(theta), r * math.sin(theta), z))
    outer.append(row)

# Center points for caps
c_bottom = (0.0, 0.0, 0.0)
c_top    = (0.0, 0.0, H)

with open(OUTPUT_PATH, "w") as f:
    f.write("solid miura_solid_cylinder\n")

    # Side surface
    for j in range(SEG_V):
        for i in range(SEG_U):
            v00 = outer[j][i]
            v01 = outer[j][i+1]
            v10 = outer[j+1][i]
            v11 = outer[j+1][i+1]
            write_facet(f, v00, v10, v11)
            write_facet(f, v00, v11, v01)

    # Bottom cap (z=0), oriented downward (-Z)
    j = 0
    for i in range(SEG_U):
        v0 = outer[j][i]
        v1 = outer[j][i+1]
        # triangle fan: (v1, v0, center) gives normals ~ -Z
        write_facet(f, v1, v0, c_bottom)

    # Top cap (z=H), oriented upward (+Z)
    j = SEG_V
    for i in range(SEG_U):
        v0 = outer[j][i]
        v1 = outer[j][i+1]
        # triangle fan: (v0, v1, center) gives normals ~ +Z
        write_facet(f, v0, v1, c_top)

    f.write("endsolid miura_solid_cylinder\n")

print(f"Exported: {OUTPUT_PATH}")
