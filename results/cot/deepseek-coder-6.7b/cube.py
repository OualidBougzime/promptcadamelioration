import cadquery as cq

# Define the dimensions
length = 50  # mm
width = 50   # mm
height = 50  # mm

# Create a workplane, then create the box and cut away any excess material.
result = (cq.Workplane('XY')
          .box(length, width, height)
          .edges("|Z")
          )