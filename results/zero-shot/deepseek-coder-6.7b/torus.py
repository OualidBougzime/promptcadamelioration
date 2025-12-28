import cadquery as cq
from math import pi, sin, cos

# Define parameters
major_radius = 50 # in millimeters
minor_radius = 8 # in millimeters

# Create a torus using CadQuery
result = (cq.Workplane("XY")
          .placeSketch(
              cq.Sketch().addTorus(major_radius, minor_radius)
          )
          .extrude(10) # extrude to create 3D object
         )