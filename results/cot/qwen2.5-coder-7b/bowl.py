import cadquery as cq

# Step 1: Create a semicircle with radius 40 mm
semicircle = cq.Semicircle(radius=40)

# Step 2: Revolve the semicircle around its diameter to form a hemisphere
hemisphere = semicircle.revolve()

# Step 3: Shell the hemisphere to create a wall thickness of 3 mm
result = hemisphere.shell(3)

# The final result is stored in the 'result' variable