from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.WebGl.display import display
import cadquery as cq

# Create a box with dimensions 50 mm x 50 mm x 50 mm
box = BRepPrimAPI_MakeBox(12.7, 12.7, 12.7).Shape()
result = cq.Workplane("XY").placeObj(cq.Shapes.convertBrepToCompound(box))

# Display the result in a web-based viewer (optional)
show_object(result)