import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Salary" : [32000, 55000, 85000, 62000, 35000, 74000, 92000, 37000, 39000, 65000, 64000, 61000, 21000, 31000, 68000, 88000, 63000, 56000, 75000, 25000]
}

plt.hist(
    data["Salary"],
    bins = 5, 
    color = "green"
)

plt.show()

