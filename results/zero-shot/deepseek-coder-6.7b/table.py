from OCP.gp import gp_Trsf2d, gp_Vec, gp_Pnt2d
import cadquery as cq

# Define dimensions
table_width = 200  # mm
table_length = 100  # mm
table_height = 15  # mm
leg_diameter = 12  # mm
leg_height = 120  # mm
inset = 15  # mm

# Create a rectangular top
table = cq.Workplane("XY").box(table_width, table_length, table_height)

# Add four cylindrical legs
legs = (cq.Workplane("XY")
         .moveTo(-table_width/2 + leg_diameter/2 + inset, -table_length/2 + leg_diameter/2 + inset)
         .circle(leg_diameter/2)
         .extrude(leg_height)
         )

# Union all parts
result = table.union(legs).val()