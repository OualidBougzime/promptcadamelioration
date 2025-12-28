import cadquery as cq

# Define parameters
radius = 60    # mm
sweep_angle = 210  # deg

result = (
    cq.Workplane("XY")
     .moveTo(0, -radius)   # start at the bottom left corner of a box around the arc
     .lineTo(0, radius)    # move straight up to the top right corner
     .threePointArc((-radius/2, radius), (0, 0))  # draw an arc from the current point to the middle of the circle
     .close()              # close the path
     .extrude(10)          # extrude it along the Z axis
)