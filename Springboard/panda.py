import pandas as pd

values = {'id': [1, 2, 3, 4],'type': ['Phone', 'Phone', 'Printer', 'Printer'], 'name': ['iPhone', 'samsung', 'hp', 'cannon'], 'price': ['5000', '200', '100', '300'], 'quantities': ['10', '20', '30', '40']}

df = pd.DataFrame(values)
print(df)
print(df.dtypes)

df = df.astype({'price':'int', 'quantities':'int'})
print(df)
print(df.dtypes)

print(df.groupby('type')[['price','quantities']].mean())
