import akshare as ak

# 获取所有场内ETF列表（含行业标签）
# etf_list = ak.fund_etf_category_sina()
# print(etf_list.head())
# etf_list.to_csv("etf_list.csv", index=False)

# 获取某只ETF的历史行情（比如：512480 半导体ETF）
stock_symbol = "000001"
fund_symbol = "512480"
index_symbol = "881279"


# df_fund = ak.fund_etf_hist_sina(symbol=fund_symbol)
# df_fund.to_csv(f"{fund_symbol}_fund.csv", index=False)

# df_stock = ak.stock_zh_a_hist(symbol=stock_symbol, period="daily", start_date="20230101", end_date="20230201")
# df_stock.to_csv(f"{stock_symbol}_stock.csv", index=False)


# 获取中证光伏设备指数（881279）的历史行情
df_index = ak.index_zh_a_hist(symbol=index_symbol, start_date="20250601", end_date="20251101")
print(df_index.head())
df_index.to_csv(f"{index_symbol}_index.csv", index=False)
