# -*- coding:utf-8 -*-
import pymongo
import pandas as pd
import matplotlib.pyplot as plt

label_mapping = {
    'fast_trade_bp': '闪电下单',
    'draw_order_bp': '画线下单',
    'draw_analy_bp': '画线分析',
    'quote_alert_bp': '行情预警',
    'contract_search_bp': '合约搜索',
    'condition_order_bp': '添加云条件单',
    'draw_warning_bp': '画线预警',
    'add_favorite_bp': '添加自选',
}

def get_mongo_data():
    """
    获取MongoDB数据
    """
    from db_setting import mongoDB
    try:
        client = pymongo.MongoClient(f"mongodb://{mongoDB['username']}:{mongoDB['password']}@{mongoDB['host']}:{mongoDB['port']}/")
        uzi = client['uzi']
        user_tracking = uzi["user_tracking"]
        return list(user_tracking.find())
    except Exception as e:
        print(f"获取MongoDB数据时出错: {e}")
        return []


def clean_near_duplicate_data(df):
    """
    清洗掉时间很近数据接近的重复数据
    """
    df = df.sort_values(by='time')
    df['time_diff'] = df['time'].diff().fillna(pd.Timedelta(seconds=0))

    # 10秒内认为是重复数据
    threshold = pd.Timedelta(seconds=10)

    # 数据与上一条完全相同的，标记为重复记录
    key_list = label_mapping.keys()
    df['is_duplicate'] = (df['time_diff'] <= threshold) & (df[key_list].shift(1) == df[key_list]).all(axis=1)

    # 删除标记为重复的记录
    df_cleaned = df[~df['is_duplicate']].drop(columns=['time_diff', 'is_duplicate'])

    return df_cleaned


def convert_to_df(docs):
    """
    转换为DataFrame
    """
    df = pd.DataFrame(docs).fillna(0)

    if df.empty:
        print("没有有效数据")
        return pd.DataFrame()

    df = clean_near_duplicate_data(df)

    # 选择数值型列，用以计算每日总和
    df['date'] = df['time'].dt.normalize()
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

    # 筛选掉2024-10-16之前的数据
    df_daily_sum = df.groupby('date')[numerical_columns].sum().query('date > "2024-10-16"')
    return df_daily_sum


def func_bp_count(df_daily_sum):
    """
    绘制功能使用次数折线图
    """
    if df_daily_sum.empty:
        print("没有数据可绘制折线图")
        return

    plt.subplot(2, 1, 1)
    for column in df_daily_sum.columns:
        df_daily_sum[column].plot(kind='line', label=label_mapping.get(column))

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 修改绘图字体，用来正常显示中文标签
    plt.title('随日期变化的功能使用次数')
    plt.ylabel('次数')
    plt.legend()
    plt.grid(True)


def func_bp_total(df_daily_sum):
    """
    绘制功能使用总次数柱状图
    """
    if df_daily_sum.empty:
        print("没有数据可绘制柱状图")
        return

    plt.subplot(2, 1, 2)
    amounts = df_daily_sum.sum()
    new_labels = [label_mapping.get(label) for label in amounts.index]
    ax = amounts.plot(kind='bar', figsize=(10, 10))
    ax.set_xticklabels(new_labels)
    plt.title('累计使用总次数')
    plt.ylabel('次数')
    plt.xticks(rotation=45)


def main():
    docs = get_mongo_data()
    df_daily_sum = convert_to_df(docs)
    func_bp_count(df_daily_sum)
    func_bp_total(df_daily_sum)
    plt.show()


if __name__ == '__main__':
    main()
