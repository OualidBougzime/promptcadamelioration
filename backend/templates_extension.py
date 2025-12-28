#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
templates_extension.py — Extension des templates pour les nouveaux types de lattice
Ajoute: lattice_bcc, lattice_fcc, lattice_diamond, lattice_octet
"""

import logging
from typing import Dict, Any

log = logging.getLogger("cadamx.templates")


class LatticeTemplates:
    """Templates pour les nouveaux types de lattice"""
    
    @staticmethod
    def generate_lattice_bcc(analysis: Dict[str, Any]) -> str:
        """Template pour BCC (Body-Centered Cubic) lattice"""
        params = analysis.get('parameters', {})
        
        block_x = params.get('block_x', 30.0)
        block_y = params.get('block_y', 30.0)
        block_z = params.get('block_z', 30.0)
        cell_size = params.get('cell_size', 15.0)
        strut_radius = params.get('strut_radius', 1.2)
        node_radius = params.get('node_radius', 1.86)
        overlap = params.get('overlap', 1.08)
        
        code = f"""#!/usr/bin/env python3
import cadquery as cq
import math

# ===== Parameters (mm) =====
BLOCK_X = {block_x}
BLOCK_Y = {block_y}
BLOCK_Z = {block_z}

A = {cell_size}             # cell size
R = {strut_radius}              # strut radius
NODE_R = {node_radius}    # node sphere radius
OVERLAP = {overlap}    # strut extension at each end

OUT = "generated_lattice_bcc.stl"

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
    print(f"Exported: {{OUT}}  (struts={{len(edges)}}, nodes={{len(nodes)}})")

nx = int(BLOCK_X / A)
ny = int(BLOCK_Y / A)
nz = int(BLOCK_Z / A)

def build_bcc():
    edges = set()
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                ox, oy, oz = i*A, j*A, k*A
                c = (ox + A/2, oy + A/2, oz + A/2)
                if not inside(c): 
                    continue
                corners = [
                    (ox, oy, oz), (ox+A, oy, oz), (ox, oy+A, oz), (ox+A, oy+A, oz),
                    (ox, oy, oz+A), (ox+A, oy, oz+A), (ox, oy+A, oz+A), (ox+A, oy+A, oz+A)
                ]
                for p in corners:
                    if inside(p):
                        edges.add(ekey(p, c))
    return [((a[0]/SCALE_KEY, a[1]/SCALE_KEY, a[2]/SCALE_KEY),
             (b[0]/SCALE_KEY, b[1]/SCALE_KEY, b[2]/SCALE_KEY)) for a, b in edges]

export_edges(build_bcc())
print(f"✅ BCC lattice generated: {{nx}}×{{ny}}×{{nz}} cells")
"""
        return code
    
    @staticmethod
    def generate_lattice_fcc(analysis: Dict[str, Any]) -> str:
        """Template pour FCC (Face-Centered Cubic) lattice"""
        params = analysis.get('parameters', {})
        
        block_x = params.get('block_x', 30.0)
        block_y = params.get('block_y', 30.0)
        block_z = params.get('block_z', 30.0)
        cell_size = params.get('cell_size', 15.0)
        strut_radius = params.get('strut_radius', 1.2)
        node_radius = params.get('node_radius', 1.86)
        overlap = params.get('overlap', 1.08)
        
        code = f"""#!/usr/bin/env python3
import cadquery as cq
import math

# ===== Parameters (mm) =====
BLOCK_X = {block_x}
BLOCK_Y = {block_y}
BLOCK_Z = {block_z}

A = {cell_size}             # cell size
R = {strut_radius}              # strut radius
NODE_R = {node_radius}    # node sphere radius
OVERLAP = {overlap}    # strut extension at each end

OUT = "generated_lattice_fcc.stl"

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
    print(f"Exported: {{OUT}}  (struts={{len(edges)}}, nodes={{len(nodes)}})")

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
print(f"✅ FCC lattice generated: {{nx}}×{{ny}}×{{nz}} cells")
"""
        return code
    
    @staticmethod
    def generate_lattice_diamond(analysis: Dict[str, Any]) -> str:
        """Template pour Diamond lattice"""
        params = analysis.get('parameters', {})
        
        block_x = params.get('block_x', 30.0)
        block_y = params.get('block_y', 30.0)
        block_z = params.get('block_z', 30.0)
        cell_size = params.get('cell_size', 15.0)
        strut_radius = params.get('strut_radius', 1.2)
        node_radius = params.get('node_radius', 1.86)
        overlap = params.get('overlap', 1.08)
        
        code = f"""#!/usr/bin/env python3
import cadquery as cq
import math

# ===== Parameters (mm) =====
BLOCK_X = {block_x}
BLOCK_Y = {block_y}
BLOCK_Z = {block_z}

A = {cell_size}             # cell size
R = {strut_radius}              # strut radius
NODE_R = {node_radius}    # node sphere radius
OVERLAP = {overlap}    # strut extension at each end

OUT = "generated_lattice_diamond.stl"

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
    print(f"Exported: {{OUT}}  (struts={{len(edges)}}, nodes={{len(nodes)}})")

nx = int(BLOCK_X / A)
ny = int(BLOCK_Y / A)
nz = int(BLOCK_Z / A)

def build_diamond():
    basis_fcc=[(0.0,0.0,0.0),(0.0,0.5,0.5),(0.5,0.0,0.5),(0.5,0.5,0.0)]
    nn=[(0.25,0.25,0.25),(0.25,-0.25,-0.25),(-0.25,0.25,-0.25),(-0.25,-0.25,0.25)]

    pts=[]
    for i in range(nx+1):
        for j in range(ny+1):
            for k in range(nz+1):
                ox, oy, oz = i*A, j*A, k*A
                for bx, by, bz in basis_fcc:
                    p=(ox+bx*A, oy+by*A, oz+bz*A)
                    if inside(p):
                        pts.append(p)

    edges = set()
    for p in pts:
        px, py, pz = p
        for dx, dy, dz in nn:
            q=(px+dx*A, py+dy*A, pz+dz*A)
            if inside(q):
                edges.add(ekey(p, q))
    
    return [((a[0]/SCALE_KEY, a[1]/SCALE_KEY, a[2]/SCALE_KEY),
             (b[0]/SCALE_KEY, b[1]/SCALE_KEY, b[2]/SCALE_KEY)) for a, b in edges]

export_edges(build_diamond())
print(f"✅ Diamond lattice generated")
"""
        return code
    
    @staticmethod
    def generate_lattice_octet(analysis: Dict[str, Any]) -> str:
        """Template pour Octet truss lattice"""
        params = analysis.get('parameters', {})
        
        block_x = params.get('block_x', 30.0)
        block_y = params.get('block_y', 30.0)
        block_z = params.get('block_z', 30.0)
        cell_size = params.get('cell_size', 15.0)
        strut_radius = params.get('strut_radius', 1.2)
        node_radius = params.get('node_radius', 1.86)
        overlap = params.get('overlap', 1.08)
        
        code = f"""#!/usr/bin/env python3
import cadquery as cq
import math

# ===== Parameters (mm) =====
BLOCK_X = {block_x}
BLOCK_Y = {block_y}
BLOCK_Z = {block_z}

A = {cell_size}             # cell size
R = {strut_radius}              # strut radius
NODE_R = {node_radius}    # node sphere radius
OVERLAP = {overlap}    # strut extension at each end

OUT = "generated_lattice_octet.stl"

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
    print(f"Exported: {{OUT}}  (struts={{len(edges)}}, nodes={{len(nodes)}})")

nx = int(BLOCK_X / A)
ny = int(BLOCK_Y / A)
nz = int(BLOCK_Z / A)

def build_octet():
    edges = set()
    
    # FCC part: connect face centers to corners
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
    
    # BCC part: connect cell center to face centers
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                ox, oy, oz = i*A, j*A, k*A
                c  = (ox + A/2, oy + A/2, oz + A/2)
                if not inside(c):
                    continue
                fcs=[
                    (ox,oy+A/2,oz+A/2),(ox+A,oy+A/2,oz+A/2),
                    (ox+A/2,oy,oz+A/2),(ox+A/2,oy+A,oz+A/2),
                    (ox+A/2,oy+A/2,oz),(ox+A/2,oy+A/2,oz+A),
                ]
                for fc in fcs:
                    if inside(fc):
                        edges.add(ekey(fc, c))
    
    return [((a[0]/SCALE_KEY, a[1]/SCALE_KEY, a[2]/SCALE_KEY),
             (b[0]/SCALE_KEY, b[1]/SCALE_KEY, b[2]/SCALE_KEY)) for a, b in edges]

export_edges(build_octet())
print(f"✅ Octet truss lattice generated: {{nx}}×{{ny}}×{{nz}} cells")
"""
        return code
