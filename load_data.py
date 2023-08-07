from FinMind.data import DataLoader
import pandas as pd
import os
import time
user_id = os.environ.get("FINMIND_USER", "")
password = os.environ.get("FINMIND_PASSWORD", "")

def save_stock_data(stock_id, start_date, end_date):
    # 定義參數字典
    params = {
        'stock_id': stock_id,
        'start_date': start_date,
        'end_date': end_date
    }

    # 載入股票資料
    dl = DataLoader()

    #沒有可以不要輸入
    dl.login(user_id, password)

    # 持有人資料
    df_holding = dl.taiwan_stock_holding_shares_per(**params)

    # 篩選出 '1-999'、'1,000-5,000' 和 '5,001-10,000' 這三類的數據
    df_holding = df_holding[
        (df_holding['HoldingSharesLevel'] == '1-999')  |
        (df_holding['HoldingSharesLevel'] == '1,000-5,000')  |
        (df_holding['HoldingSharesLevel'] == '5,001-10,000') |
        (df_holding['HoldingSharesLevel'] == '10,001-15,000')|
        (df_holding['HoldingSharesLevel'] == '15,001-20,000')
    ]

    # 使用 pivot 將 'HoldingSharesLevel' 的五個類別變成五個不同的欄位
    df_holding = df_holding.pivot(index='date', columns='HoldingSharesLevel', values='percent').reset_index()

    # 股價資料
    df_price = dl.taiwan_stock_daily(**params)

    # 選擇 'Trading_Volume'、'Trading_Volume' 和 'Trading_Volume' 這三個欄位
    df_price = df_price[['date', 'Trading_Volume', 'Trading_money', 'close']]

    # 將持股數據與股價數據合併
    df = df_holding.merge(df_price, on='date', how='outer')

    # 用前一筆資料來填充 NaN
    #df = df.sort_values(by='date')
    #df = df.fillna(method='ffill')

    # 將 date 轉換為 datetime 格式並進行排序
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # 將 DataFrame 存儲為 CSV 文件
    df.to_csv(f'data/{stock_id}.csv', index=False)



#要取的股票名稱放在name.txt
file_path = "name.txt"
name_list = []
start_date = '2022-01-01'
end_date = '2023-07-25'
# 開啟文件並逐行讀取名稱
with open(file_path, "r") as file:
    for line in file:
        name_list.append(line.strip())

for i in name_list:
    try:
        print(i)
        save_stock_data(i, start_date, end_date)
        time.sleep(5)
    except:
        pass
