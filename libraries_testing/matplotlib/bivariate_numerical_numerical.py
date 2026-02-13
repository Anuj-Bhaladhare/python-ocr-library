import matplotlib.pyplot as plt
import pandas as pd


data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
    "Age" : [22, 25, 29, 24, 30, 35, 40, 36, 28, 22, 23, 25, 26, 24, 31, 29, 27, 33, 35, 38]
}

df = pd.DataFrame(data)

# print(df.head())


# ==============================================
# ---------------> Scatter Plot <---------------
# ==============================================
# plt.scatter(
#     df["Age"],
#     df["Salary"],
#     color = "orange"
# )
# plt.show()

sort_age = df.sort_values("Age")


# ==============================================
# -----------------> Line Plot <----------------
# ==============================================
# plt.plot(
#     sort_age["Age"],
#     df["Salary"],
#     color = "red",
#     marker = "o",
#     linewidth = "2"
# )
# plt.grid()
# plt.show()


# ==============================================
# -----------------> Bar Chart <----------------
# ==============================================
# plt.bar(
#     sort_age["Age"],
#     df["Salary"],
#     color = "green"
# )
# plt.grid()
# plt.show()








# ========================================================
# ========>> Bivariate: Numerical - categorical <<========
# ========================================================
hr_sal = df[df["dept"] == "HR"]["Salary"]    # get Salary of HR
print(hr_sal)

it_sal = df[df["dept"] == "IT"]["Salary"]    # get Salary of IT
print(it_sal)

fin_sal = df[df["dept"] == "Finance"]["Salary"]    # get Salary of Finance
print(fin_sal)

# # Box Plot
# plt.boxplot(
#     [hr_sal, it_sal, fin_sal],
#     labels = ["Hr", "IT", "Finance"] 
# )
# plt.grid()
# plt.show()



# Pie Chart:
salary_by_dept = df.groupby("dept")["Salary"].sum()
print(salary_by_dept)
plt.pie(
    salary_by_dept, 
    labels = salary_by_dept.index, 
    autopct = "%1.2f", 
    shadow = True, 
    explode = [0.1, 0, 0.1]
)
plt.axis("equal")
plt.show()
