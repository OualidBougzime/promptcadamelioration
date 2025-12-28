import bpy
from pathlib import Path

stl_path = Path(r"C:\Users\obougzim\PromptCAD\output\generated_stent.stl")
fbx_path = Path(r"C:\Users\obougzim\PromptCAD\output\generated_stent.fbx")

print("Blender STL path:", stl_path)
print("Blender FBX path:", fbx_path)

# Nettoyer la scène
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Importer le STL
bpy.ops.import_mesh.stl(filepath=str(stl_path))

# Tout sélectionner
bpy.ops.object.select_all(action='SELECT')

# Exporter en FBX
bpy.ops.export_scene.fbx(
    filepath=str(fbx_path),
    use_selection=True
)

print("Blender export done.")
