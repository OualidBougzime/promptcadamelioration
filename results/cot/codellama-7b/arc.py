import cadquery as cq

def create_arc(radius, sweep_angle):
    center = cq.Vector3D(0, 0, 0)
    circle = cq.Workplane().circle(center, radius)
    arc = circle.sweep(sweep_angle)
    return arc

result = create_arc(60, 210)