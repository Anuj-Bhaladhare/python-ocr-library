import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Salary" : [21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'Management', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],
    "Age" : [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
}

df = pd.DataFrame(data)

df["experience"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Object Oriented API
fig, axs = plt.subplots(1, 3, figsize = (10, 5))

# Line Plot
axs[0].plot(sort_age["Age"], df["Salary"], o )
