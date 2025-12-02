import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import time

# 1) 获取数据
symbol = ["600519.SS"]  # 示例：贵州茅台
start, end = "2019-01-01", "2021-01-01"
# data = yf.download(symbol, start=start, end=end)
data = {}
for ticker in symbol:
    try:
        data[ticker] = yf.download(ticker, period="1mo")
        print(f"成功获取 {ticker}")
        time.sleep(10)  # 每次请求间隔10秒
    except Exception as e:
        print(f"{ticker} 下载失败: {str(e)}")

close = data['Close'].copy()

# 2) 策略参数与信号（双均线交叉）
short_win, long_win = 20, 50
data['SMA_S'] = close.rolling(short_win).mean()
data['SMA_L'] = close.rolling(long_win).mean()
data['signal'] = 0
data.loc[data['SMA_S'] > data['SMA_L'], 'signal'] = 1
data.loc[data['SMA_S'] < data['SMA_L'], 'signal'] = -1

# 3) 回测参数
init_cap = 1_000_000
pos_size = 0.10          # 单标的最大资金使用比例
commission = 0.001       # 单边佣金率
slippage = 0.0005        # 单边滑点

# 4) 向量化回测（避免未来信息：shift(1)）
data['ret'] = close.pct_change()
data['pos'] = data['signal'].shift(1)  # T日信号，T+1日开盘执行
data['turnover'] = data['pos'].abs().rolling(2).sum().fillna(0)  # 近两日换手

# 5) 成本与成交价（简化：按开盘价成交 + 滑点）
data['exec_price'] = close * (1 + data['pos'].shift(1) * slippage)
trade = data['pos'].diff().abs()
gross_pnl = (data['ret'] * data['pos']).fillna(0)

# 6) 现金与净值（多空均计费；若仅做多可简化）
data['fees'] = (trade * close * commission).fillna(0)
data['cash'] = init_cap \
               - (data['pos'].shift(1) * data['exec_price'] * commission).fillna(0).cumsum() \
               - (trade * data['exec_price'] * commission).fillna(0).cumsum()
data['hold_val'] = (data['pos'].shift(1) * close).fillna(0).cumsum()
data['total'] = data['cash'] + data['hold_val']

# 7) 绩效指标
ann_ret = data['total'].pct_change().mean() * 252
ann_vol = data['total'].pct_change().std() * np.sqrt(252)
sharpe = ann_ret / ann_vol
peak = data['total'].cummax()
mdd = (peak - data['total']).max()

print(f"年化收益: {ann_ret:.2%} | 波动率: {ann_vol:.2%} | 夏普: {sharpe:.2f} | 最大回撤: {mdd:.2%}")

# 8) 可视化
(data['total'] / data['total'].iloc[0]).plot(figsize=(12,6), title="策略净值 vs 买入持有", grid=True)
((data['Close']/data['Close'].iloc[0]) * init_cap / data['Close'].iloc[0]).plot(label="买入持有")
plt.legend(); plt.ylabel("净值"); plt.xlabel("日期")