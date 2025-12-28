# Generated code that failed:
import cadquery as cq
from pathlib import Path

# Import STL mesh
result = cq.importers.importStl("assets/lion.stl")

# Scale to standard size
result = result.scale((1.0, 1.0, 1.0))

# Position the lion in the desired location
result = result.translate((0, 0, 0))

# Export
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "generated_lion.stl"
cq.exporters.export(result, str(output_path))
print(f" STL exported to: {output_path}")