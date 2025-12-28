import cadquery as cq

# Define profile parameters
base_radius = 30
mid_height = 60
top_radius = 35
length = mid_height + top_radius  # Length of the vase is sum of mid and top radii

# Create a smooth profile using Workplane.circle() method with radius as argument
profile = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(length)
)

# Revolve the profile about Z-axis to create vase shape
result = (
    profile
    .revolve(cq.Vector(0, 0, length/2))
)