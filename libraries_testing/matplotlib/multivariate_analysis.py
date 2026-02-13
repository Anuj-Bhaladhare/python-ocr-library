import matplotlib.pyplot as plt
import pandas as pd


data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
    "Age" : [22, 25, 29, 24, 30, 35, 40, 36, 28, 22, 23, 25, 26, 24, 31, 29, 27, 33, 35, 38]
}

df = pd.DataFrame(data)

# Multivariate Analysis: 3 numerical columns
print(df.head())

# =====================================
# ===========> Bubble Plot <===========
# =====================================
# plt.scatter(
#     df["Age"], 
#     df["Salary"], 
#     s = df["experience"]*50, 
#     color = "skyblue", 
#     edgecolors = "black"
# )
# plt.title("Age vs Salary vs Experience")
# plt.xlabel("Age")
# plt.ylabel("Salary")
# plt.show()




# =====================================
# 2 numerical and 1 categorical column:
# =====================================
# plt.scatter(
#     df["Age"], 
#     df["Salary"], 
#     c = df["dept"].map(
#         {
#             "HR": "yellow", 
#             "IT":"blue", 
#             "Finance": "orange"
#         }
#     )
# )
# plt.xlabel("Age")
# plt.ylabel("Salary")
# plt.title("Age vs Salary vs Dept")
# plt.legend()
# plt.show()


color = {"HR": "yellow", "IT":"blue", "Finance": "orange"}

for dept, color in color.items():
    df_dept = df[df["dept"] == dept]
    plt.scatter(df_dept["Age"], df_dept["Salary"], c = color, label = dept)

plt.legend()
