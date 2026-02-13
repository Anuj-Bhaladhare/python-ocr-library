import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Salary" : [21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'Management', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],
    "Age" : [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
}

df = pd.DataFrame(data)

df["experience"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# print(df.head())

# # Bubble Plot
# plt.scatter(
#     df["Age"],
#     df["Salary"],
#     s = df["experience"] * 20,   # Size of a bubbel
#     color = "skyblue",
#     edgecolors = "black"
# )
# plt.show()



# # 2 numerical and 1 categorical column:
# color_map = {"HR": "yellow", "IT": "blue", "Finance": "orange"}

# colors = df["dept"].map(color_map).fillna("gray")

# plt.scatter(df["Age"], df["Salary"], c=colors, label = df["dept"])
# plt.xlabel("Age")
# plt.ylabel("Salary")
# plt.title("Age vs Salary vs Dept")
# plt.show()


color = {"HR": "yellow", "IT": "blue", "Finance": "orange"}

for dept, color in color.items():
    df_dept = df[df["dept"] == dept]
    plt.scatter(df_dept["Age"], df_dept["Salary"], c = color, label = dept)

plt.legend()
plt.show()
