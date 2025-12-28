import cadquery as cq

top_width = 200
top_length = 100
top_height = 15

leg_diameter = 12
leg_height = 120
leg_inset = 15

result = (
    cq.Workplane("XY")
    .rect(top_width, top_length, forConstruction=True)
    .extrude(top_height)
    .faces(">Z")
    .workplane()
    .moveAxes(cq.Vector(leg_inset, leg_inset, 0))
    .circle(leg_diameter / 2)
    .extrude(leg_height)
    .faces("<Z")
    .chamfer(1)
    .workplane()
    .moveAxes(cq.Vector(-leg_inset, leg_inset, 0))
    .circle(leg_diameter / 2)
    .extrude(leg_height)
    .faces("<Z")
    .chamfer(1)
    .workplane()
    .moveAxes(cq.Vector(leg_inset, -leg_inset, 0))
    .circle(leg_diameter / 2)
    .extrude(leg_height)
    .faces("<Z")
    .chamfer(1)
    .workplane()
    .moveAxes(cq.Vector(-leg_inset, -leg_inset, 0))
    .circle(leg_diameter / 2)
    .extrude(leg_height)
    .faces("<Z")
    .chamfer(1)
    .union()
    .subtract(cq.Workplane("XY").rect(top_width, top_length).extrude(top_height))
)