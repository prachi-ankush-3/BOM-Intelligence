import pandas as pd
import re
import ezdxf

# STEP 1: READ BOM

file_path = "Plate_Components_BOM.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Plate BOM",
    header=3
)

# Select Part No. 10
part_10 = df[df["P.NO."] == 10].iloc[0]

# BOM PARAMETERS

part_no = int(part_10["P.NO."])
description = str(part_10["Part Description"])
material = str(part_10["Specification"])
quantity = int(part_10["P.QTY"])
item_code = str(part_10["Remark/Purchase Item Code"])

size_text = str(part_10["Size"])

# Extract dimensions from:
# 1185 x 3060 x 3 THK

numbers = re.findall(
    r"\d+(?:\.\d+)?",
    size_text
)

width = float(numbers[0])
length = float(numbers[1])
thickness = float(numbers[2])


print("==========================================")
print("PART 10 BOM INFORMATION")
print("==========================================")

print("Part No.    :", part_no)
print("Description :", description)
print("Material    :", material)
print("Quantity    :", quantity)
print("Width       :", width, "mm")
print("Length      :", length, "mm")
print("Thickness   :", thickness, "mm")
print("Item Code   :", item_code)


# ============================================================
# STEP 2: ALL ENGINEERING PARAMETERS
# ============================================================

L = length
W = width
THK = thickness

# ------------------------------------------------------------
# PART OUTLINE PARAMETERS
# ------------------------------------------------------------

STEP_HEIGHT = 125
STEP_LENGTH = 219


# ------------------------------------------------------------
# HOLE PARAMETERS
# ------------------------------------------------------------

HOLE_DIAMETER = 14
HOLE_RADIUS = HOLE_DIAMETER / 2
HOLE_COUNT = 46


# ------------------------------------------------------------
# HORIZONTAL HOLE SPACING
# Taken from engineering drawing
#
# 250 | 147 | 150 | 150 | 150 | 150 | 150 | 150 |
# 233 | 233 |
# 150 | 150 | 150 | 150 | 150 | 150 | 147 | 250
# ------------------------------------------------------------

HORIZONTAL_SPACING = [
    250,
    147,
    150,
    150,
    150,
    150,
    150,
    150,
    233,
    233,
    150,
    150,
    150,
    150,
    150,
    150,
    147,
    250
]


# ------------------------------------------------------------
# VERTICAL HOLE SPACING
#
# Top edge → top hole       = 144
# Row 1 → Row 2             = 225
# Row 2 → Row 3             = 225
# Row 3 → Row 4             = 225
# Row 4 → bottom row        = 215
# Bottom row → bottom edge  = 151
# ------------------------------------------------------------

TOP_OFFSET = 144
ROW_SPACING_1 = 225
ROW_SPACING_2 = 225
ROW_SPACING_3 = 225
ROW_SPACING_4 = 215
BOTTOM_OFFSET = 151


# ------------------------------------------------------------
# MIDDLE HOLE COLUMNS
# ------------------------------------------------------------

MIDDLE_X_INDEXES = [
    0,
    7,
    9,
    16
]


# ============================================================
# STEP 3: CALCULATE HOLE X POSITIONS
# ============================================================

row_x = []

x = 0

# We don't use the final 250 here because it is
# the distance from the last hole to the right edge.

for spacing in HORIZONTAL_SPACING[:-1]:

    x += spacing
    row_x.append(x)


# ============================================================
# STEP 4: CALCULATE HOLE Y POSITIONS
# ============================================================

top_y = W - TOP_OFFSET

row_y = [
    top_y,
    top_y - ROW_SPACING_1,
    top_y - ROW_SPACING_1 - ROW_SPACING_2,
    top_y - ROW_SPACING_1 - ROW_SPACING_2 - ROW_SPACING_3,
    BOTTOM_OFFSET
]


# ============================================================
# STEP 5: CREATE HOLE POSITIONS
# ============================================================

hole_positions = []


# ------------------------------------------------------------
# TOP ROW
# 17 holes
# ------------------------------------------------------------

for x in row_x:

    hole_positions.append(
        (x, row_y[0])
    )


# ------------------------------------------------------------
# BOTTOM ROW
# 17 holes
# ------------------------------------------------------------

for x in row_x:

    hole_positions.append(
        (x, row_y[4])
    )


# ------------------------------------------------------------
# MIDDLE ROWS
# 4 holes × 3 rows = 12 holes
# ------------------------------------------------------------

middle_x = [
    row_x[index]
    for index in MIDDLE_X_INDEXES
]

for y in row_y[1:4]:

    for x in middle_x:

        hole_positions.append(
            (x, y)
        )


print("\n==========================================")
print("HOLE INFORMATION")
print("==========================================")

print("Hole diameter :", HOLE_DIAMETER, "mm")
print("Required holes:", HOLE_COUNT)
print("Generated holes:", len(hole_positions))


if len(hole_positions) != HOLE_COUNT:

    raise ValueError(
        f"Hole count mismatch! "
        f"Expected {HOLE_COUNT}, "
        f"but generated {len(hole_positions)}"
    )

print("Hole count verified successfully.")


# ============================================================
# STEP 6: CREATE DXF
# ============================================================

doc = ezdxf.new("R2018")

msp = doc.modelspace()
# ============================================================
# DRAWING LAYERS
# ============================================================

doc.layers.add("OUTLINE")
doc.layers.add("HOLES")
doc.layers.add("DIMENSIONS")
doc.layers.add("TEXT")
doc.layers.add("CALLOUT")

# ============================================================
# STEP 7: DRAW PART OUTLINE
# ============================================================

# NOTE: the real drawing (PART NO. - 10) only has the step notch on the
# BOTTOM-LEFT corner. The bottom-right corner is a plain square corner
# (no mirrored step) — confirmed against the source PDF.
msp.add_lwpolyline(
    [
        (0, STEP_HEIGHT),

        (STEP_LENGTH, STEP_HEIGHT),

        (STEP_LENGTH, 0),

        (L, 0),

        (L, W),

        (0, W),

        (0, STEP_HEIGHT)
    ],
    close=True
)


# ============================================================
# STEP 8: DRAW HOLES
# ============================================================

for x, y in hole_positions:

    msp.add_circle(
        center=(x, y),
        radius=HOLE_RADIUS
    )


# ============================================================
# STEP 9: TEXT HELPER
# ============================================================

def add_text(text, position, height=35, rotation=0):

    msp.add_text(
        text,
        dxfattribs={
            "height": height,
            "rotation": rotation
        }
    ).set_placement(position)


# ============================================================
# STEP 10: DRAWING HEADER
# ============================================================

add_text(
    f"{HOLE_COUNT} x DIA{HOLE_DIAMETER} HOLES - M12",
    (100, W + 430),
    40
)

add_text(
    f"SIZE: {L:.0f} x {W:.0f} x {THK:.0f} THK",
    (100, W + 360),
    40
)

add_text(
    f"MATERIAL: {material}",
    (100, W + 290),
    40
)

add_text(
    f"PART NO. {part_no}",
    (100, W + 220),
    40
)


# ============================================================
# STEP 11: OVERALL LENGTH - 3060
# ============================================================

dim_y = W + 170

# Main dimension line
msp.add_line(
    (0, dim_y),
    (L, dim_y)
)

# Extension lines
msp.add_line(
    (0, W),
    (0, dim_y)
)

msp.add_line(
    (L, W),
    (L, dim_y)
)

# Arrows
arrow = 20

msp.add_line(
    (0, dim_y),
    (arrow, dim_y + 8)
)

msp.add_line(
    (0, dim_y),
    (arrow, dim_y - 8)
)

msp.add_line(
    (L, dim_y),
    (L - arrow, dim_y + 8)
)

msp.add_line(
    (L, dim_y),
    (L - arrow, dim_y - 8)
)

add_text(
    f"{L:.0f}",
    (L / 2 - 40, dim_y + 20),
    40
)


# ============================================================
# STEP 12: HORIZONTAL HOLE SPACING
# ============================================================

chain_y = W + 70

# Extension lines
for x in row_x:

    msp.add_line(
        (x, W),
        (x, chain_y)
    )

msp.add_line(
    (0, W),
    (0, chain_y)
)

msp.add_line(
    (L, W),
    (L, chain_y)
)


# Dimension points
points = [0] + row_x + [L]

arrow_size = 12

for i in range(len(points) - 1):

    x1 = points[i]
    x2 = points[i + 1]

    # Dimension line
    msp.add_line(
        (x1, chain_y),
        (x2, chain_y)
    )

    # Left arrow
    msp.add_line(
        (x1, chain_y),
        (x1 + arrow_size, chain_y + 5)
    )

    msp.add_line(
        (x1, chain_y),
        (x1 + arrow_size, chain_y - 5)
    )

    # Right arrow
    msp.add_line(
        (x2, chain_y),
        (x2 - arrow_size, chain_y + 5)
    )

    msp.add_line(
        (x2, chain_y),
        (x2 - arrow_size, chain_y - 5)
    )

    # Dimension value
    spacing = HORIZONTAL_SPACING[i]

    add_text(
        str(spacing),
        ((x1 + x2) / 2 - 15, chain_y + 15),
        28
    )


# ============================================================
# STEP 13: OVERALL WIDTH - 1185
# ============================================================

dim_x = L + 180

msp.add_line(
    (dim_x, 0),
    (dim_x, W)
)

msp.add_line(
    (L, 0),
    (dim_x, 0)
)

msp.add_line(
    (L, W),
    (dim_x, W)
)

# Arrows
msp.add_line(
    (dim_x, 0),
    (dim_x - 8, 20)
)

msp.add_line(
    (dim_x, 0),
    (dim_x + 8, 20)
)

msp.add_line(
    (dim_x, W),
    (dim_x - 8, W - 20)
)

msp.add_line(
    (dim_x, W),
    (dim_x + 8, W - 20)
)

add_text(
    f"{W:.0f}",
    (dim_x + 30, W / 2),
    35,
    90
)


# ============================================================
# STEP 14: RIGHT VERTICAL HOLE DIMENSIONS
# ============================================================

vertical_chain_x = L + 80

vertical_points = [
    W,
    row_y[0],
    row_y[1],
    row_y[2],
    row_y[3],
    row_y[4],
    0
]

vertical_values = [
    TOP_OFFSET,
    ROW_SPACING_1,
    ROW_SPACING_2,
    ROW_SPACING_3,
    ROW_SPACING_4,
    BOTTOM_OFFSET
]

for i in range(len(vertical_values)):

    y1 = vertical_points[i]
    y2 = vertical_points[i + 1]

    # Dimension line
    msp.add_line(
        (vertical_chain_x, y1),
        (vertical_chain_x, y2)
    )

    # Extension lines
    msp.add_line(
        (L, y1),
        (vertical_chain_x, y1)
    )

    msp.add_line(
        (L, y2),
        (vertical_chain_x, y2)
    )

    # Arrows
    msp.add_line(
        (vertical_chain_x, y1),
        (vertical_chain_x - 5, y1 - 12)
    )

    msp.add_line(
        (vertical_chain_x, y1),
        (vertical_chain_x + 5, y1 - 12)
    )

    msp.add_line(
        (vertical_chain_x, y2),
        (vertical_chain_x - 5, y2 + 12)
    )

    msp.add_line(
        (vertical_chain_x, y2),
        (vertical_chain_x + 5, y2 + 12)
    )

    add_text(
        str(vertical_values[i]),
        (vertical_chain_x - 35, (y1 + y2) / 2),
        28,
        90
    )


# ============================================================
# STEP 15: LEFT 1060 DIMENSION
# ============================================================

left_dim_x = -140

msp.add_line(
    (left_dim_x, STEP_HEIGHT),
    (left_dim_x, W)
)

msp.add_line(
    (0, STEP_HEIGHT),
    (left_dim_x, STEP_HEIGHT)
)

msp.add_line(
    (0, W),
    (left_dim_x, W)
)

add_text(
    f"{W - STEP_HEIGHT:.0f}",
    (left_dim_x - 40, (STEP_HEIGHT + W) / 2),
    35,
    90
)


# ============================================================
# STEP 16: LEFT 125 STEP HEIGHT
# ============================================================

left_step_x = -140

msp.add_line(
    (left_step_x, 0),
    (left_step_x, STEP_HEIGHT)
)

msp.add_line(
    (0, 0),
    (left_step_x, 0)
)

msp.add_line(
    (0, STEP_HEIGHT),
    (left_step_x, STEP_HEIGHT)
)

add_text(
    f"{STEP_HEIGHT:.0f}",
    (left_step_x - 35, STEP_HEIGHT / 2),
    30,
    90
)


# ============================================================
# STEP 17: 219 STEP LENGTH
# ============================================================

step_dim_y = -80

msp.add_line(
    (0, step_dim_y),
    (STEP_LENGTH, step_dim_y)
)

msp.add_line(
    (0, 0),
    (0, step_dim_y)
)

msp.add_line(
    (STEP_LENGTH, 0),
    (STEP_LENGTH, step_dim_y)
)

add_text(
    f"{STEP_LENGTH:.0f}",
    (STEP_LENGTH / 2 - 20, step_dim_y - 35),
    30
)


# ============================================================
# STEP 18: MIDDLE HORIZONTAL DIMENSIONS
# ============================================================

middle_dim_y = 720

middle_points = [
    0,
    row_x[0],
    row_x[7],
    row_x[9]
]

middle_values = [
    row_x[0],
    row_x[7] - row_x[0],
    row_x[9] - row_x[7]
]

for i in range(len(middle_values)):

    x1 = middle_points[i]
    x2 = middle_points[i + 1]

    msp.add_line(
        (x1, middle_dim_y),
        (x2, middle_dim_y)
    )

    msp.add_line(
        (x1, middle_dim_y),
        (x1, middle_dim_y + 35)
    )

    msp.add_line(
        (x2, middle_dim_y),
        (x2, middle_dim_y + 35)
    )

    add_text(
        str(middle_values[i]),
        ((x1 + x2) / 2 - 20, middle_dim_y + 20),
        30
    )


# ============================================================
# STEP 19: PART INFORMATION
# ============================================================

title_y = -150

add_text(
    f"PART NO. - {part_no}",
    (L / 2 - 120, title_y),
    55
)

add_text(
    "(QTY. - 1 NO. - AS SHOWN)",
    (L / 2 - 190, title_y - 65),
    35
)

add_text(
    "(QTY. - 1 NO. - AS OPP. HAND)",
    (L / 2 - 220, title_y - 120),
    35
)

add_text(
    "(SCALE 1:2)",
    (L / 2 - 70, title_y - 175),
    35
)


# ============================================================
# STEP 20: HOLE CALLOUT
# ============================================================

# Bottom-row hole at the second inner (middle-column) position —
# matches the leader's start point on the source drawing.
hole_x = row_x[9]
hole_y = row_y[4]

callout_x = hole_x + 100
callout_y = -80

# Leader
msp.add_line(
    (hole_x, hole_y),
    (callout_x, callout_y)
)

msp.add_line(
    (callout_x, callout_y),
    (callout_x + 400, callout_y)
)

add_text(
    f"DIA{HOLE_DIAMETER} HOLE",
    (callout_x + 420, callout_y + 10),
    35
)

add_text(
    "46 NOS. M12",
    (callout_x + 420, callout_y - 45),
    35
)

# F1 erection-mark balloon next to the callout (as shown on the drawing)
balloon_center = (callout_x + 850, callout_y + 15)
msp.add_circle(
    center=balloon_center,
    radius=45
)

add_text(
    "F1",
    (balloon_center[0] - 25, balloon_center[1] - 15),
    35
)


# ============================================================
# STEP 21: SAVE DXF
# ============================================================

output_file = "Part_10_basic.dxf"

doc.saveas(output_file)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n==========================================")
print("DRAWING CREATED")
print("==========================================")

print("File      :", output_file)
print("Part No.  :", part_no)
print("Size      :", L, "x", W, "mm")
print("Thickness :", THK, "mm")
print("Material  :", material)
print("Step      :", STEP_LENGTH, "x", STEP_HEIGHT, "mm")
print("Hole Dia. :", HOLE_DIAMETER, "mm")
print("Holes     :", len(hole_positions))
print("==========================================")