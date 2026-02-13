import matplotlib.pyplot as plt
import pandas as pd

# ==============================================
# ----------> Univariate - Numerical <----------
# ==============================================

data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000]
}

df = pd.DataFrame(data)

# print Five data of "data object"
print(df.head())

# print Length and how much column is available
print(f"print length and column: (length, column) => {df.shape}") 




# ==============================================
# -----------------> Line Plot <----------------
# ==============================================
# plt.plot(df["Salary"], color = "red", linestyle = ":", marker = "o", linewidth = "2" )
# plt.grid()
# plt.show()


# ==============================================
# -----------------> Histogram <----------------
# ==============================================
# plt.hist(df["Salary"], bins = 5, color = "green")
# plt.grid()
# plt.show()


# ==============================================
# ------------------> Box-Plot <----------------
# ==============================================
# plt.boxplot(df["Salary"])
# plt.grid()
# plt.show()

# Adding New Line in Dataframe
df.loc[20] = [0]

# plt.boxplot(df["Salary"])
# plt.grid()
# plt.show()

df.drop(index = 20, inplace = True)

print(df.shape)

