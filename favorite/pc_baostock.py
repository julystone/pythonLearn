import baostock as bs
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Grid

# 初始化Baostock登录
lg = bs.login()
if lg.error_code != '0':
    raise Exception(f"登录失败: {lg.error_msg}")

# 获取股票数据（示例：平安银行 000001）
# stock_code = "000001.SZ"
# start_date = "2024-01-01"
# end_date = "2025-09-15"
# stock_code = "000001.SZ"
stock_name = "新易盛"
bs.query_stock_basic(code_name=stock_name)
stock_code = bs.get_code_name(stock_name)
start_date = "2025-01-01"
end_date = "2025-09-18"


# 查询历史K线数据
rs = bs.query_history_k_data_plus(
    stock_code,
    "date,open,high,low,close,volume",
    start_date=start_date,
    end_date=end_date,
    frequency="d",
    adjustflag="3"  # 3表示不复权
)

# 数据处理
# data_list = []
# while rs.next():
#     data_list.append([
#         rs.get_row_data()[0],  # 日期
#         float(rs.get_row_data()[1]),  # 开盘
#         float(rs.get_row_data()[2]),  # 最高
#         float(rs.get_row_data()[3]),  # 最低
#         float(rs.get_row_data()[4])   # 收盘
#     ])
#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
df = pd.DataFrame(data_list, columns=rs.fields)


# df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close'])
df['date'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m-%d")

# 转换Pyecharts所需数据格式


kline_data = df[['open', 'close', 'low', 'high']].values.tolist()
dates = df['date'].tolist()

# 创建K线图
kline = (
    Kline()
    .add_xaxis(dates)
    .add_yaxis(
        series_name="新易盛",
        y_axis=kline_data,
        itemstyle_opts=opts.ItemStyleOpts(
            color="#ef232a",      # 阳线颜色
            color0="#00a800",     # 阴线颜色
            border_color="#ef232a",
            border_color0="#00a800"
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title=f"{stock_code} K线图"),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            is_scale=True
        ),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value} 元"),
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(opacity=1)
            )
        ),
        datazoom_opts=[opts.DataZoomOpts()],  # 启用缩放工具
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross"
        )
    )
)

# 添加移动平均线（正确实现方式）
ma5 = df['close'].rolling(5).mean().tolist()
ma10 = df['close'].rolling(10).mean().tolist()

# 创建均线图层
line = (
    Line()
    .add_xaxis(dates)
    .add_yaxis(
        series_name="MA5",
        y_axis=ma5,
        linestyle_opts=opts.LineStyleOpts(width=2, color="#5470C6"),
        label_opts=opts.LabelOpts(is_show=False)
    )
)

line2 = (
    Line()
    .add_xaxis(dates)
    .add_yaxis(
        series_name="MA10",
        y_axis=ma10,
        linestyle_opts=opts.LineStyleOpts(width=2, color="#91CC75"),
        label_opts=opts.LabelOpts(is_show=False)
    )
)

# 组合图表
overlap = kline.overlap(line).overlap(line2)

# 渲染图表
overlap.render("pyecharts_kline.html")

# 登出Baostock
bs.logout()