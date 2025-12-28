import cadquery as cq
from math import pi

# Define the dimensions
semi_circle_radius = 40 # in millimeters
wall_thickness = 3 # in millimeters

# Create a semicircle and revolve it around z-axis to form a hemisphere
semi_circle = cq.Workplane().move(-semi_circle_radius, 0).box(2*semi_circle_radius, semi_circle_radius, 1)
hemisphere = semi_circle.revolve()

# Create a shell with the defined wall thickness
result = hemisphere.shell(wall_thickness)