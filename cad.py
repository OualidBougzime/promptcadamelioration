import cadquery as cq
# Step 1: Define heatsink parameters
plate_width = 40
plate_height = 40
plate_thickness = 3
tube_outer = 42
tube_length = 10
fin_length = 22
fin_angle = 20
# Step 2: Create base plate
base_plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)
# Step 3: Add mounting holes
mount_positions = [(-16, -16), (16, -16), (-16, 16), (16, 16)]
for x, y in mount_positions:
    hole = cq.Workplane("XY").center(x, y).circle(1.65).extrude(plate_thickness*2)
    base_plate = base_plate.cut(hole)
# Step 4: Add central tube
tube = cq.Workplane("XY").workplane(offset=plate_thickness).rect(tube_outer, tube_outer*0.8).extrude(tube_length)
result = base_plate.union(tube)
# Step 5: Add cooling fins
for side in [-1, 1]:
    fin = cq.Workplane("XY").workplane(offset=plate_thickness+tube_length).rect(fin_length, 4).extrude(8)
    fin = fin.translate((side*15, 0, 0))
    fin = fin.rotate((0, 0, plate_thickness+tube_length), (1, 0, 0), side*fin_angle)
    result = result.union(fin)
cq.exporters.export(result, "cpu_heatsink_cot.stl")