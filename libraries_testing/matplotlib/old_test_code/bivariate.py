import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Salary" : [21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'Management', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],
    "Age" : [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
}

df = pd.DataFrame(data)


# plt.scatter(
#     df["Age"],
#     df["Salary"],
#     color = "red",
#     marker = "o",
#     linewidth = 2
# )

# plt.bar(
#     df["Age"],
#     df["Salary"],
#     color = "green"
# )

# plt.grid()
# plt.show()

# -------> Bivariate: Numerical - categorical <---------
hr_sal = df[df["dept"] == "HR"]["Salary"]
it_sal = df[df["dept"] == "IT"]["Salary"]
fin_sal = df[df["dept"] == "Finance"]["Salary"]
# print(hr_sal)

# # Boxplot
# plt.boxplot(
#     [hr_sal, it_sal, fin_sal],
#     labels = ["HR", "IT", "Finance"]
# )
# plt.show()


# pie chart
salary_by_dept = df.groupby("dept")["Salary"].sum()
print(salary_by_dept)
plt.pie(
    salary_by_dept,
    labels = salary_by_dept.index,
    autopct = "%1.2f",
    shadow = 0.2,
    explode = [0.1, 0.1, 0.1, 0.1]
)
plt.show()


# # bar plot
# hr_mean = sum(hr_sal)/len(hr_sal)
# it_mean = sum(it_sal)/len(it_sal)
# fin_mean = sum(fin_sal)/len(fin_sal)
# plt.bar(
#     ["HR", "IT", "Finance"],
#     [hr_mean, it_mean, fin_mean],
#     color = ["green", "black", "red"]
# )
# plt.grid()
# plt.show()


