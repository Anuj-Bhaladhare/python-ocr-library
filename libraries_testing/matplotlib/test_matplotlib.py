import matplotlib.pyplot as plt
import pandas as pd

x = [1, 2, 3]    # Define X-axis co-ordinate
y = [4, 5, 6]    # Define Y-axis co-ordinate

plt.plot(x, y, linestyle = "--", color = "red")   # (1, 4)(2, 5)(3, 6)
plt.grid()
plt.show()
