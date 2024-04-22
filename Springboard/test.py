# In the given dataframe 
# 1. Add a columns that calculates the percentage for Math & science subjects for all students
# 2. Find students who have a Math percentage over 80
import pandas as pd

df = pd.DataFrame({
  "Students":["A","B"," C"],
  "Math": ["25", "100", "90"],
  "Science": [50, 85, 75],
  "English": [67,56, 95]
})
df = df.astype({'Math': 'int'})
print(df['Math'].sum())
df['Percentage_math']=df['Math']/df['Math'].sum()

df['Percentage_scin']=df['Science']/df['Science'].sum()
print(df)
print(df[df['Percentage_math']>0.8]['Students'])


#df.astype({'col1': 'int32'})