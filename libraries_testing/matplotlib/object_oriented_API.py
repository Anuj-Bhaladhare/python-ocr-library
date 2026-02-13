import matplotlib.pyplot as plt
import pandas as pd


data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
    "Age" : [22, 25, 29, 24, 30, 35, 40, 36, 28, 22, 23, 25, 26, 24, 31, 29, 27, 33, 35, 38]
}

df = pd.DataFrame(data)

sort_age = df.sort_values("Age")

fig, axs = plt.subplots(1,3, figsize = (15,5))

# Line plot

axs[0].plot(
    sort_age["Age"],
    df["Salary"],
    color = "red",
    marker = "o",
    linewidth = "2",
    markersize = 2
)
axs[0].grid()
axs[0].set_title("Line Plot")
axs[0].set_xlabel("Age")
axs[0].set_ylabel("Salary")

# Histogram

axs[1].hist(
    df["Salary"], 
    bins = 5, 
    color = "skyblue"
)
axs[1].grid()
axs[1].set_title("Histogram")
axs[1].set_xlabel("Salary")
axs[1].set_ylabel("Frequency")

# Boxplot:

axs[2].boxplot(df["Salary"])
axs[2].grid()
axs[2].set_title("Boxplot")
axs[2].set_xlabel("Salary")

plt.show()



