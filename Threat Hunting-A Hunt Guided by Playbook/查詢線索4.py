import pandas as pd
from pandas.io import json

# 從 JSON 文件讀取數據
df = json.read_json(path_or_buf='C:\\Users\\JohnsonSun\\empire_mimikatz_logonpasswords_2020-08-07103224.json', lines=True)

# 篩選 Image Load 相關資料
imageLoadDf = (
    df[['@timestamp', 'ProcessGuid', 'Image', 'ImageLoaded']]
    [
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
    .groupby(['ProcessGuid', 'Image'])['ImageLoaded'].count().sort_values(ascending=False)
    .to_frame()
)

# 篩選 Process Access 相關資料
processAccessDf = (
    df[['@timestamp', 'Hostname', 'SourceImage', 'TargetImage', 'GrantedAccess', 'SourceProcessGUID']]
    [
        (df['Channel'] == 'Microsoft-Windows-Sysmon/Operational') &
        (df['EventID'] == 10) &
        (df['TargetImage'].str.contains('.*lsass.exe', regex=True)) &
        (df['CallTrace'].str.contains('.*UNKNOWN*', regex=True))
    ]
)

# 合併兩個 DataFrame
merged_df = pd.merge(
    imageLoadDf, processAccessDf,
    left_on='ProcessGuid', right_on='SourceProcessGUID', 
    how='inner'
)

# 顯示合併後的結果
print(merged_df)