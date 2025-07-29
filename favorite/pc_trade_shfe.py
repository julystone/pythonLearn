import pandas as pd


def read_blocks(filename):
    # 步骤1：读取整个sheet（不跳过任何行）
    df_raw = pd.read_excel(filename, header=None, skiprows=2)

    # 步骤2：遍历行，识别每个数据块的开始和结束
    blocks = []  # 存储每个数据块的(start_index, end_index, 商品名称)
    current_start = None
    commodity_name = None

    for idx, row in df_raw.iterrows():
        # 检查第一列是否以“商品名称:”开头
        if row[0].startswith('商品名称:'):
            commodity_name = row[0].split(':')[1]  # 提取商品名称
            current_start = idx - 1  # 数据块从下一行开始（假设数据块紧接着商品名称行）
        elif row[0] == '小计':
            # 遇到小计行，表示当前数据块结束
            if current_start is not None:
                blocks.append((current_start, idx - 1, commodity_name))  # 结束行为小计的前一行
                current_start = None
                commodity_name = None

    return blocks, df_raw


# 预处理函数：提取期权类型(C/P)
def extract_option_type(contract_code):
    if not isinstance(contract_code, str):
        return None
    # 识别合约代码中的C/P标识（位置通常在日期代码之后）
    import re
    matches = re.findall(r'\d+([CP]).+', contract_code)
    return matches[0] if matches else None


def data_prepare(blocks, df_raw):
    block_list = []
    block_df = None  # 存储所有数据块的DataFrame
    for start, end, name in blocks:
        block_df = df_raw.loc[start:end].copy()
        # 设置列标题：取第一行作为列名，然后删除该行
        block_df.columns = block_df.iloc[0]  # 第一行作为列名
        block_df = block_df[2:]  # 去掉第一、第二行（列名行）
        # 添加期权类型列
        block_df['期权类型'] = block_df['合约代码'].apply(extract_option_type)
        # 添加商品名称列
        block_df['商品名称'] = name
        # 将“持仓量”列转换为数值
        block_df['持仓量'] = block_df['持仓量'].str.replace(',', '').astype(float)
        block_list.append(block_df)
    return block_list


def max_ccl_record(block_list):
    dfs = []
    # 分别处理看涨(C)和看跌(P)
    for block_df in block_list:
        for option_type in ['C', 'P']:
            # 筛选特定期权类型
            option_df = block_df[block_df['期权类型'] == option_type]

            if len(option_df) > 0:
                # 按持仓量降序排序
                sorted_df = option_df.sort_values('持仓量', ascending=False)

                # 获取持仓量最大的合约
                max_holding_row = sorted_df.iloc[0]

                # 添加到结果
                dfs.append(max_holding_row)
            else:
                # 添加空行占位
                placeholder = {
                    '商品类型': 1,
                    '期权类型': option_type,
                    '合约代码': None,
                    '持仓量': 0,
                    '收盘价': None
                }
                dfs.append(placeholder)

    final_df = pd.DataFrame(dfs)
    # print(final_df)

    return final_df
    # final_df.to_excel("./Excel_shfe.xlsx")


def compare_df(df1, df2):
    # 合并两个DataFrame, 比较持仓量与国君持仓量差异
    merged_df = pd.merge(df1, df2, on=['商品名称', '期权类型'], how='inner')
    merged_df['diff'] = merged_df['持仓量'] - merged_df['国君持仓量'].astype(float)
    # merged_df['diff'] = merged_df['diff'].map({0: '一致'})
    print(merged_df)
    merged_df.to_excel("./Excel_shfe_diff.xlsx")


def app():
    filename = "../ExcelFiles/shfe期权all.xlsx"
    blocks, df_raw = read_blocks(filename)
    block_list = data_prepare(blocks, df_raw)
    final_df = max_ccl_record(block_list)
    expected_df = pd.read_excel("../ExcelFiles/Excel_shfe_expected.xlsx")
    compare_df(final_df, expected_df)



if __name__ == '__main__':
    app()
