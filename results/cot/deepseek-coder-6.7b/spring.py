from OCP.gp import gp_Trsf, gp_Ax2d
import cadquery as cq

# Define the key dimensions and parameters
spring_radius = 1.5  # mm
helix_major_radius = 20  # mm
helix_pitch = 8  # mm
total_height = 80  # mm

# Create a circle for the spring
spring = cq.Workplane("XY").circle(spring_radius)

# Extrude to create the helical spring along z-axis
helical_spring = spring.extrude(total_height)

# Define the helix as a translation of a circle
helix = (cq.Workplane("XY")
          .circle(helix_major_radius)
          .translate((0, -40, 0)))

# Rotate the helix by pitch around y-axis to create sweeping pattern
sweep = helical_spring.workplane().add(helix).rotate((0, 1, 0), (0, helix_pitch))

result = sweep.combine()