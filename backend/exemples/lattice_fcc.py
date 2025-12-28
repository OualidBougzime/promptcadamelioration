import cadquery as cq
import math

# ===== Parameters (mm) =====
BLOCK_X = 30.0
BLOCK_Y = 30.0
BLOCK_Z = 30.0

A = 15.0             # cell size
R = 1.2              # strut radius
NODE_R = 1.55 * R    # node sphere radius (1.3R-2.0R)
OVERLAP = 0.9 * R    # strut extension at each end (0.5R-1.5R)

OUT = "lattice_fcc_fixed.stl"

EPS = 1e-6
SCALE_KEY = 1_000_000

def inside(p):
    x, y, z = p
    return (-EPS <= x <= BLOCK_X + EPS) and (-EPS <= y <= BLOCK_Y + EPS) and (-EPS <= z <= BLOCK_Z + EPS)

def pkey(p):
    return (int(round(p[0] * SCALE_KEY)), int(round(p[1] * SCALE_KEY)), int(round(p[2] * SCALE_KEY)))

def ekey(p1, p2):
    a = pkey(p1); b = pkey(p2)
    return (a, b) if a <= b else (b, a)

def vsub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vadd(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vmul(a, s):
    return (a[0]*s, a[1]*s, a[2]*s)

def vlen(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def vunit(v):
    L = vlen(v)
    if L < 1e-9:
        return (0.0, 0.0, 0.0)
    return (v[0]/L, v[1]/L, v[2]/L)

def cylinder_between(p1, p2, radius, overlap=0.0):
    v = vsub(p2, p1)
    L = vlen(v)
    if L < 1e-9:
        return None
    u = vunit(v)

    # extend both ends so struts overlap *inside* node spheres
    p1e = vsub(p1, vmul(u, overlap))
    p2e = vadd(p2, vmul(u, overlap))

    v2 = vsub(p2e, p1e)
    L2 = vlen(v2)
    if L2 < 1e-9:
        return None

    return cq.Solid.makeCylinder(radius, L2, cq.Vector(*p1e), cq.Vector(*v2))

def export_edges(edges):
    # collect unique nodes
    nodes = set()
    for (p1, p2) in edges:
        nodes.add(pkey(p1))
        nodes.add(pkey(p2))

    solids = []

    # struts
    for (p1, p2) in edges:
        c = cylinder_between(p1, p2, R, overlap=OVERLAP)
        if c is not None:
            solids.append(c)

    # node spheres (guaranteed connectivity)
    for nk in nodes:
        p = (nk[0]/SCALE_KEY, nk[1]/SCALE_KEY, nk[2]/SCALE_KEY)
        solids.append(cq.Solid.makeSphere(NODE_R, cq.Vector(*p)))

    # Create compound without fusion
    comp = cq.Compound.makeCompound(solids)
    
    cq.exporters.export(comp, OUT)
    print(f"Exported: {OUT}  (struts={len(edges)}, nodes={len(nodes)})")

nx = int(BLOCK_X / A)
ny = int(BLOCK_Y / A)
nz = int(BLOCK_Z / A)

def build_fcc():
    edges = set()
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                ox, oy, oz = i*A, j*A, k*A
                c000=(ox,oy,oz); c100=(ox+A,oy,oz); c010=(ox,oy+A,oz); c110=(ox+A,oy+A,oz)
                c001=(ox,oy,oz+A); c101=(ox+A,oy,oz+A); c011=(ox,oy+A,oz+A); c111=(ox+A,oy+A,oz+A)

                fx0=(ox,oy+A/2,oz+A/2); fx1=(ox+A,oy+A/2,oz+A/2)
                fy0=(ox+A/2,oy,oz+A/2); fy1=(ox+A/2,oy+A,oz+A/2)
                fz0=(ox+A/2,oy+A/2,oz); fz1=(ox+A/2,oy+A/2,oz+A)

                face_map=[
                    (fx0,[c000,c010,c001,c011]),(fx1,[c100,c110,c101,c111]),
                    (fy0,[c000,c100,c001,c101]),(fy1,[c010,c110,c011,c111]),
                    (fz0,[c000,c100,c010,c110]),(fz1,[c001,c101,c011,c111]),
                ]
                for fc, corners in face_map:
                    if not inside(fc):
                        continue
                    for p in corners:
                        if inside(p):
                            edges.add(ekey(fc, p))
    return [((a[0]/SCALE_KEY, a[1]/SCALE_KEY, a[2]/SCALE_KEY),
             (b[0]/SCALE_KEY, b[1]/SCALE_KEY, b[2]/SCALE_KEY)) for a, b in edges]

export_edges(build_fcc())