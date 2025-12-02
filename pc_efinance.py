import efinance as ef
import pandas as pd
from datetime import datetime

# 黄金期货代码（上海期货交易所）
futures_code = "115.ZCM"  # 示例代码，需根据实际合约调整

# 获取黄金期货基本信息（包含交易所、合约单位等）
futures_info = ef.futures.get_futures_base_info()
print("合约基本信息：")
print(futures_info)

# 获取黄金期货历史持仓量数据（需自行关联仓单数据）
# 示例：获取近30日持仓量变化（需结合交易所日报）
beg_date = (datetime.now() - pd.Timedelta(days=30)).strftime("%Y%m%d")
end_date = datetime.now().strftime("%Y%m%d")

# 获取日K线数据（持仓量字段为 '持仓量'）
kline_data = ef.futures.get_quote_history(
    futures_code,
    beg='20240101',
    end='20240201',
    klt=101  # 日K线
)

# 提取持仓量数据
positions = kline_data[["日期", "成交量"]].copy()
positions["日期"] = pd.to_datetime(positions["日期"])
positions.set_index("日期", inplace=True)

print("近30日成交量变化：")
print(positions.tail())