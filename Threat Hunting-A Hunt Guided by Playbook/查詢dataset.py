import pandas as pd
from pandas.io import json

df = json.read_json(path_or_buf='C:\\Users\\JohnsonSun\\empire_mimikatz_logonpasswords_2020-08-07103224.json', lines=True)
print(df)