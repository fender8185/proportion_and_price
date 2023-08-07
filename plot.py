import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
matplotlib.use('TkAgg')


def calculate_correlation(stock_price, shareholder_ratio):
    # 確保兩個輸入都是 pandas Series
    stock_price = pd.Series(stock_price)
    shareholder_ratio = pd.Series(shareholder_ratio)
    
    # 計算兩個變量的相關性
    correlation, _ = pearsonr(stock_price, shareholder_ratio)
    
    return correlation





qry_range="15,001-20,000"

# 讀取 CSV 檔案
df = pd.read_csv('data/2330.csv')

# 將 'date' 轉換為 datetime 格式
df['date'] = pd.to_datetime(df['date'])


# 使用前一筆資料來填充 'close' 欄位中的 NaN 值
# 因為股權表通常在週六，我們要通常要取用的close是前一日（週五）
df = df.sort_values(by='date')
df['close'] = df['close'].fillna(method='ffill')

# 刪除欄位中沒有數據的行(刪掉週一到週五)
df = df[df[qry_range].notna()]



C=(calculate_correlation(df['close'],df[qry_range]))
print(C)
# 建立一個新的圖表
fig, ax1 = plt.subplots()

color = 'tab:red'
# ax1 設定為股價
ax1.set_xlabel('Date')
plt.xticks(rotation=45)
ax1.set_ylabel('Close Price', color=color)
ax1.plot(df['date'], df['close'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # 共享相同的 x 軸
color = 'tab:blue'
# ax2 設定為對應的分級表持有人數
ax2.set_ylabel('Number of Holders ('+qry_range+')', color=color)  
ax2.plot(df['date'], df[qry_range], color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.title("2330 - "+"correlation ="+str(C)[:6])

fig.tight_layout()  # 確保底部不被截斷
plt.savefig(qry_range+'.png')
plt.show()
