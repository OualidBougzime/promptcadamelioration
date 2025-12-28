import cadquery as cq
from math import sin, pi

# Define profile parameters
base_radius = 30  # mm
mid_height = 60   # mm
top_radius = 35    # mm
length = mid_height + top_radius  # total length is sum of height and radius at the top

# Create a smooth profile using parametric equation for a helix curve
def helix(t):
    r = base_radius + (top_radius - base_radius) * t
    x = r * cos(2*pi*t)
    y = r * sin(2*pi*t)
    z = mid_height * t
    return (x,y,z)

# Create a solid from the profile using CadQuery's `Workplane.parametricCurve()` method
profile = cq.Workplane("XY").parametricCurve(helix)

# Revolve the profile around Z-axis to create vase
result = profile.revolve(cq.Vector(0, 0, 0))