import pandas as pd
import glob
from scipy.stats import pearsonr
import numpy
from itertools import combinations
import os

def calculate_correlation(stock_price, shareholder_ratio):
    stock_price = pd.Series(stock_price)
    shareholder_ratio = pd.Series(shareholder_ratio)
    
    # 計算兩個變量的相關性
    correlation, _ = pearsonr(stock_price, shareholder_ratio)
    
    return correlation

# 找到 'data' 資料夾中的所有 CSV 文件
csv_files = glob.glob('data/*.csv')

# 股東比例列的名稱
ratio_columns = ['1-999', '1,000-5,000', '5,001-10,000', '10,001-15,000', '15,001-20,000']

# 用來存儲相關係數的字典
correlations = {}

for i in csv_files:
    # 檢查檔名是否以 "00" 開頭
    filename = os.path.basename(i)
    if filename.startswith('00'):
        continue  # 如果是，則跳過該檔案
    columns_to_fill = ["Trading_Volume", "Trading_money", "close"]
    qry_table=pd.read_csv(i)
    #先將股價相關資訊補上 (ex:週六有股權分散表但沒有相對應的股價 所以我們往回到週五取股價)
    qry_table[columns_to_fill] = qry_table[columns_to_fill].fillna(method='ffill')
    qry_table = qry_table.dropna(subset=ratio_columns)
    qry_table = qry_table.fillna(method='ffill')
    qry_table = qry_table.fillna(method='bfill')

    # 檢查第一筆資料的股東比例總和是否超過 45
    if qry_table[ratio_columns].iloc[0].sum() < 45:
        continue
    print(filename)
    # 對每一個可能的組合計算相關性
    for r in range(1, len(ratio_columns) + 1):  
        for combination in combinations(ratio_columns, r):
            combined_ratio = qry_table[list(combination)].sum(axis=1)
            correlation = calculate_correlation(qry_table['close'], combined_ratio)
            if numpy.isfinite(correlation):
                # 將相關係數加到字典中
                if combination in correlations:
                    correlations[combination].append(correlation)
                else:
                    correlations[combination] = [correlation]


# 計算並打印所有的平均相關係數
correlation_data = []
for combination, correlation_list in correlations.items():
    avg_correlation = sum(correlation_list) / len(correlation_list)
    correlation_data.append({
        'combination': ', '.join(combination),
        'average_correlation': avg_correlation
    })
# 將結果寫入 CSV 檔案
df = pd.DataFrame(correlation_data)
df.to_csv('correlation_results.csv', index=False)