import matplotlib.pyplot as plt
import pandas as pd


data = {
    "Salary" : [25000, 30000, 37000, 28000, 39000, 48000, 55000, 52000, 35000, 26000, 27000, 31000, 33000, 29000, 40000, 36000, 34000, 45000, 47000, 50000]
}

df = pd.DataFrame(data)

df["dept"] = ['HR', 'IT', 'Finance', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR'] * 2

print(f"====== df.head()======> \n {df.head()} \n========================  \n")

print(f"====== df.info()======> \n {df.info()} \n========================  \n")

count = df["dept"].value_counts()

# ==============================================
# -----------------> Pie Chart <----------------
# ==============================================

# plt.pie(
#     count,         #  Data from Department Column
#     labels = count.index,   # Add lable of department
#     autopct = "%1.2f",      # Add percentage
#     explode = [0, 0.1, 0.2] # Add Gap between all part
# )
# plt.axis("equal")
# plt.show()




# ==============================================
# -----------------> Countplot <----------------
# ==============================================
plt.bar(
    count.index,
    count,
    color = ["red", "green", "blue"]
)
plt.grid()
plt.show()


