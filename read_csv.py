import pandas as pd 

income_file = pd.read_csv('106_165-9.csv')
# columns: 縣市 鄉鎮市區   村里  納稅單位   綜合所得總額   平均數  中位數  第一分位數  第三分位數      標準差    變異係數
print(income_file.head())
income_file = income_file.rename(columns={income_file.columns[0]: '縣市'})
print(income_file.groupby(['縣市', '鄉鎮市區']).sum())