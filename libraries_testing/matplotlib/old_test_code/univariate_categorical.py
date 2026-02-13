import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Salary" : [32000, 55000, 85000, 62000, 35000, 74000, 92000, 37000, 39000, 65000, 64000, 61000, 21000, 31000, 68000, 88000, 63000, 56000, 75000, 25000]
}

df = pd.DataFrame(data)

df["dept"] = ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'Management', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR']

count = df["dept"].value_counts()

# ========= Pai Chart =========
# plt.pie(
#     count, 
#     labels = count.index,
#     autopct = "%1.1f",
#     explode = [0, 0, 0, 0.1]
# )


# ========== Count Plot ==========
plt.bar(
    count.index, 
    count, 
    color = ["green", "black", "red", "yellow"]
)


plt.show()



