import plotly.graph_objects as go
import numpy as np
from PIL import Image
import plotly.express as px
import pandas as pd

# # =========================================================================================
# # ============= Option 1: Show an image as a 3D surface (MOST COMMON & WORKS) =============
# # =========================================================================================
# img = Image.open("image_data/rolled_image.png").convert("L")     # grayscale
# z = np.array(img)

# fig = go.Figure(data = [go.Surface(z = z)])
# fig.update_layout(title = "3D Image as Surface")
# fig.show()

img = Image.open("image_data/rolled_image.png").convert("L")
z = np.array(img)

fig = go.Figure(data=[go.Surface(z=z)])
fig.update_layout(title="3D Image as Surface")

fig.write_html("3d_image_surface.html")




# # =========================================================================================
# # =============== Option 2: Use image as a background (NOT inside 3D space) ===============
# # =========================================================================================
# data = {
#     "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000],
#     "dept" : ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
#     "Age" : [22, 25, 29, 24, 30, 35, 40, 36, 28, 22, 23, 25, 26, 24, 31, 29, 27, 33, 35, 38],
#     "experience" : [1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0]
# }

# df = pd.DataFrame(data)

# fig = px.scatter_3d(df, x="Age", y="Salary", z="experience")

# fig.add_layout_image(
#     dict(
#         source="image_data/rolled_image.png",
#         xref="paper",
#         yref="paper",
#         x=0,
#         y=1,
#         sizex=1,
#         sizey=1,
#         opacity=0.3,
#         layer="below"
#     )
# )

# fig.show()





# =========================================================================================
# ============ Option 3: Fake it — image as a cloud of points (advanced trick) ============
# =========================================================================================








