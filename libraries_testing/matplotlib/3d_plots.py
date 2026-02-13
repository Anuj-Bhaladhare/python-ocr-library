import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000],
    "dept" : ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
    "Age" : [22, 25, 29, 24, 30, 35, 40, 36, 28, 22, 23, 25, 26, 24, 31, 29, 27, 33, 35, 38],
    "experience" : [1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0, 1.0, 2.0, 4.0, 1.5, 5.0]
}

df = pd.DataFrame(data)

sort_age = df.sort_values("Age")

fig, axs = plt.subplots(1,3, figsize = (15,5))

data2 = {
    'Year': [2020, 2021, 2022, 2023],
    'Sales': [100, 150, 200, 250],
    'Profit': [20, 30, 40, 50],
    'Expenses': [80, 120, 160, 200]
}

df2 = pd.DataFrame(data2)

# plt.plot(df2["Year"], df2["Sales"], label = "Sales")
# plt.plot(df2["Year"], df2["Profit"], label = "Profit")
# plt.plot(df2["Year"], df2["Expenses"], label = "Expenses")

# plt.title("Financial Analysis")
# plt.xlabel("Year")
# plt.ylabel("Amount")
# plt.legend()
# plt.show()




# ===================================================
# -------------------> 3D - Plot <-------------------
# ===================================================
print(df.head())

ax = plt.axes(projection = "3d")

# ax.scatter(
#     df["Age"],
#     df["Salary"],
#     df["experience"]
# )
# ax.set_xlabel("Age")
# ax.set_ylabel("Salary")
# ax.set_zlabel("Experience")
# plt.show()


fig = px.scatter_3d(
    df, 
    x='Age', 
    y='Salary', 
    z='experience', 
    title='3D Scatter Plot'
)
fig.show()





