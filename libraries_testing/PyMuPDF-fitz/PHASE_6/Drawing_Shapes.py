"""
==============================================================
DRAWING SHAPES IN PDF USING PyMuPDF
==============================================================

This script demonstrates:

1. Draw Rectangle
2. Draw Circle
3. Draw Lines
4. Fill Colors
5. Visualize Text Blocks (Practical Debugging Example)

Author: ANUJ
"""

import fitz  # PyMuPDF

# File Configuration
input_pdf = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/shapes_visualization_output.pdf"



# ------------------------------------------------------------------
# 1. Open PDF Document
# ------------------------------------------------------------------
doc = fitz.open(input_pdf)   # Replace with your file
page = doc[1]                   # First page



# Find Keyword of Co-Ordinate and Draw Shapes
keyword = "configuration"
find_co_ordinate = page.search_for(keyword)


# ------------------------------------------------------------------
# 2. DRAW RECTANGLE
# ------------------------------------------------------------------
"""
Rect(x0, y0, x1, y1)

x0, y0  ->  top-left
x0, y0  ->  top-left
"""
top, left = 150, 150
width, height = 200, 100
# rect = fitz.Rect(top, left, top + width, left + height)
rect = fitz.Rect(find_co_ordinate[0])    # Custom for Keyword

page.draw_rect(
    rect,
    color = (1, 0, 0),
    width = 2
)
print("✅ Rectangle drawn.")



# # ------------------------------------------------------------
# # 3. Draw Filled Rectengle
# # ------------------------------------------------------------
# top, left = 150, 150
# width, height = 200, 100
# # filled_rect = fitz.Rect(top, left, top + width, left + height)
# filled_rect = fitz.Rect(find_co_ordinate[0])    # Custom for Keyword

# page.draw_rect(
#     filled_rect,
#     color = (0, 0, 1),           # Blue border
#     fill = (0, 0.8, 1),          # Light blue fill
#     width = 1,                    # Border thickness
#     fill_opacity = 0.3            # 👈 Transparency: 0.0 (invisible) to 1.0 (opaque)
# )
# print("✅ Filled rectangle drawn.")




# ------------------------------------------------------------
# 4️⃣ DRAW CIRCLE
# ------------------------------------------------------------

for rect in find_co_ordinate:
    x0, y0, x1, y1 = rect  # rect = (x0, y0, x1, y1)
    
    width = x1 - x0
    height = y1 - y0
    
    # Center
    center_x = x0 + width / 2
    center_y = y0 + height / 2
    center_point = fitz.Point(center_x, center_y)

    dx = x1 - center_x
    dy = 0   # Same horizontal line
    distance = ((dx)**2 + (dy)**2)**0.5
    
    # Radius
    radius = distance
    
    # Draw circle
    page.draw_circle(
        center_point,
        radius,
        color=(0, 1, 0),   # Green border
        width=2
    )

print("✅ Circle drawn over all keyword occurrences.")




# # ------------------------------------------------------------
# # 5️⃣ DRAW LINE
# # ------------------------------------------------------------

# # point1 = fitz.Point(50, 350)
# # point2 = fitz.Point(400, 350)

# # Draw Line for Keyword
# for rect in find_co_ordinate:
#     x0, y0, x1, y1 = rect  # rect = (x0, y0, x1, y1)

#     width = x1 - x0
#     height = y1 - y0
    
#     point1 = fitz.Point(x0, y0 + height)
#     point2 = fitz.Point(x1, y1)

#     page.draw_line(
#         point1,
#         point2,
#         color=(0, 0, 0),   # Black line
#         width=3
#     )

# print("✅ Line drawn.")


# ------------------------------------------------------------
# 7️⃣ Save Output
# ------------------------------------------------------------
doc.save(output_path)
doc.close()

print("🎯 Drawing demo completed successfully.")

