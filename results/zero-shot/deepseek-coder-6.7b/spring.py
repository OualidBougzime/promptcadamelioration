from math import pi, sin, cos
import cadquery as cq

# Parameters
radius = 1.5  # mm
major_radius = 20  # mm
pitch = 8  # mm
total_height = 80  # mm

# Create a helix profile
helix = []
for i in range(int((total_height/pitch) * 360)):
    theta = (i / ((total_height/pitch)/360)) * pi/180.0 # convert to radians
    x = major_radius*cos(theta) + radius*sin(theta)*2
    y = major_radius*sin(theta) - radius*cos(theta)*2
    helix.append((x,y,0))

# Create a CQ object and sweep along the helix profile
result = cq.Workplane("XY").polyline(helix).close().extrude(1)