import pandas as pd
from pandas.io import json

# 從 JSON 文件讀取數據
df = json.read_json(path_or_buf='C:\\Users\\JohnsonSun\\empire_mimikatz_logonpasswords_2020-08-07103224.json', lines=True)

# 打印整個 DataFrame（可選）
#print(df)

# 進行篩選操作
filtered_df = df[
    (df['Channel'].str.lower() == 'security') &
    ((df['EventID'] == 4663) | (df['EventID'] == 4656)) &
    (df['ObjectName'].str.contains('.*lsass.exe', regex=True)) &
    (~df['SubjectUserName'].str.endswith('.*$', na=False))
]

# 選擇特定的欄位並取出前幾行
result = filtered_df[['@timestamp', 'Hostname', 'SubjectUserName', 'ProcessName', 'ObjectName', 'AccessMask', 'EventID']].head()

# 顯示篩選後的結果
print(result)