import pandas as pd

data = ['김','이','박']
series_data = pd.Series(data,name='data',dtype="string")
series_data.to_json("a.json",index=True)