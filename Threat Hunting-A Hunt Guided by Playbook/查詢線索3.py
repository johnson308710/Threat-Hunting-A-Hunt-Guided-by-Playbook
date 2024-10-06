import pandas as pd
from pandas.io import json

# 從 JSON 文件讀取數據
df = json.read_json(path_or_buf='C:\\Users\\JohnsonSun\\empire_mimikatz_logonpasswords_2020-08-07103224.json', lines=True)

# 篩選條件
filtered_df = df[
    (df['Channel'] == 'Microsoft-Windows-Sysmon/Operational') &
    (df['EventID'] == 7) &
    (
        (df['ImageLoaded'].str.contains('.*samlib.dll', regex=True)) |
        (df['ImageLoaded'].str.contains('.*vaultcli.dll', regex=True)) |
        (df['ImageLoaded'].str.contains('.*hid.dll', regex=True)) |
        (df['ImageLoaded'].str.contains('.*winscard.dll', regex=True)) |
        (df['ImageLoaded'].str.contains('.*cryptdll.dll', regex=True))
    ) &
    (df['@timestamp'].between('2020-06-00 00:00:00.000', '2020-08-20 00:00:00.000'))
]

# 分組統計並排序
grouped_df = filtered_df.groupby(['ProcessGuid', 'Image'])['ImageLoaded'].count().sort_values(ascending=False)

# 轉換為 DataFrame 格式
result_df = grouped_df.to_frame()

# 顯示結果
print(result_df)