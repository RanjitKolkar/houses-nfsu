import pandas as pd

# load excel
df = pd.read_excel("state_wise.xlsx")

# state-wise count
statewise = df.groupby("State").size().reset_index(name="Count")

# save to excel
statewise.to_excel("statewise_data.xlsx", index=False)

print(statewise)
