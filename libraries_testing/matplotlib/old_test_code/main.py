import matplotlib.pyplot as plt
import pandas as pd

# x = [1, 2, 3]
# y = [4, 5, 6]

# plt.plot(x, y)    # (1, 4)(2, 5)(3, 6) 
# plt.grid()
# plt.show()

# ===================================================
#  ------------------- Pyplot API -------------------
# ===================================================

# Univariate  -  Nuerical

data = {
    "Salary" : [32000, 55000, 85000, 62000, 35000, 74000, 92000, 37000, 39000, 65000, 64000, 61000, 21000, 31000, 68000, 88000, 63000, 56000, 75000, 25000]
} 
df = pd.DataFrame(data)

# # First 5 record of dataframe 
# print(df.head())

# Plot the Salary Data
plt.plot(
    df["Salary"],
    color = "red",
    marker = "o",
    linestyle = "--",
    linewidth = "2"
)

plt.grid()    # Add Grid Boxes in Chart 
plt.show()    # Show the charts

