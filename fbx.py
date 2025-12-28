#!/usr/bin/env python3
import math
import cadquery as cq
from pathlib import Path
import subprocess
import tempfile

CFG = {
    "outer_radius": 8.0,
    "length": 40.0,
    "n_peaks": 8,
    "n_rings": 6,
    "amplitude": 3.0,
    "ring_spacing": 6.0,
    "strut_width": 0.6,
    "strut_depth": 0.4,
}

def create_strut_between_points(cfg, p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    
    width = cfg["strut_width"]
    depth = cfg["strut_depth"]
    
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    
    if length < 0.001:
        return None
    
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    cz = (z1 + z2) / 2
    
    angle_z = math.degrees(math.atan2(dy, dx))
    horizontal_dist = math.sqrt(dx*dx + dy*dy)
    angle_y = math.degrees(math.atan2(dz, horizontal_dist))
    
    strut = (cq.Workplane("XY")
            .center(0, 0)
            .rect(length, width)
            .extrude(depth))
    
    strut = (strut
            .rotate((0, 0, 0), (0, 1, 0), -angle_y)
            .rotate((0, 0, 0), (0, 0, 1), angle_z)
            .translate((cx, cy, cz)))
    
    return strut

def get_ring_points(cfg, z_center, phase_shift=0):
    R = cfg["outer_radius"]
    n_peaks = cfg["n_peaks"]
    amplitude = cfg["amplitude"]
    
    peaks = []
    valleys = []
    angle_step = 360.0 / n_peaks
    
    for i in range(n_peaks):
        angle_peak = i * angle_step + phase_shift
        x_peak = R * math.cos(math.radians(angle_peak))
        y_peak = R * math.sin(math.radians(angle_peak))
        z_peak = z_center + amplitude / 2
        peaks.append((x_peak, y_peak, z_peak))
        
        angle_valley = angle_peak + angle_step / 2
        x_valley = R * math.cos(math.radians(angle_valley))
        y_valley = R * math.sin(math.radians(angle_valley))
        z_valley = z_center - amplitude / 2
        valleys.append((x_valley, y_valley, z_valley))
    
    return peaks, valleys

def build_stent_parts(cfg):
    """Retourne une liste de parts individuelles au lieu d'un mesh fusionné"""
    n_rings = cfg["n_rings"]
    ring_spacing = cfg["ring_spacing"]
    n_peaks = cfg["n_peaks"]
    
    total_height = (n_rings - 1) * ring_spacing
    z_start = -total_height / 2
    
    parts = []  # Liste de tuples (nom, solid)
    rings_points = []
    
    for ring_idx in range(n_rings):
        z = z_start + ring_idx * ring_spacing
        phase_shift = 0 if ring_idx % 2 == 0 else (360.0 / n_peaks) / 2
        
        peaks, valleys = get_ring_points(cfg, z, phase_shift)
        rings_points.append((peaks, valleys))
        
        # Struts du ring
        n = len(peaks)
        for i in range(n):
            strut = create_strut_between_points(cfg, peaks[i], valleys[i])
            if strut:
                parts.append((f"ring{ring_idx}_strut{i}_a", strut))
            
            next_peak = peaks[(i + 1) % n]
            strut = create_strut_between_points(cfg, valleys[i], next_peak)
            if strut:
                parts.append((f"ring{ring_idx}_strut{i}_b", strut))
    
    # Bridges entre rings
    for ring_idx in range(len(rings_points) - 1):
        peaks1, valleys1 = rings_points[ring_idx]
        peaks2, valleys2 = rings_points[ring_idx + 1]
        
        for i in range(len(peaks1)):
            if ring_idx % 2 == 0:
                bridge = create_strut_between_points(cfg, peaks1[i], valleys2[i])
            else:
                bridge = create_strut_between_points(cfg, valleys1[i], peaks2[i])
            
            if bridge:
                parts.append((f"bridge{ring_idx}_{i}", bridge))
    
    return parts

# === MAIN ===
print("Generating stent parts...")
parts = build_stent_parts(CFG)
print(f"  → {len(parts)} parts générées")

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
temp_dir = output_dir / "temp_parts"
temp_dir.mkdir(exist_ok=True)

# Export chaque part en STL séparé
print("Exporting individual STLs...")
for name, part in parts:
    cq.exporters.export(part.val(), str(temp_dir / f"{name}.stl"))

# Script Blender pour importer tous les STLs et exporter en FBX
fbx_path = output_dir / "generated_stent.fbx"

blender_script = f'''
import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

temp_dir = r"{temp_dir}"
for filename in os.listdir(temp_dir):
    if filename.endswith(".stl"):
        filepath = os.path.join(temp_dir, filename)
        bpy.ops.wm.stl_import(filepath=filepath)
        # Renommer l'objet importé
        obj = bpy.context.selected_objects[0]
        obj.name = filename[:-4]  # Sans .stl

bpy.ops.export_scene.fbx(filepath=r"{fbx_path}", use_selection=False)
print(f"Exported {{len(bpy.data.objects)}} objects to FBX")
'''

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(blender_script)
    script_path = f.name

print("Converting to FBX via Blender...")
subprocess.run(["blender", "--background", "--python", script_path], check=True)

# Nettoyage
Path(script_path).unlink()
import shutil
shutil.rmtree(temp_dir)

print(f"✓ FBX exporté : {fbx_path}")
print(f"  → {len(parts)} objets séparés dans le fichier")