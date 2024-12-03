#  _____            ___             ____     __
# /\___ \          /\_ \           /\  _`\  /\ \__
# \/__/\ \   __  __\//\ \    __  __\ \,\L\_\\ \ ,_\    ___     ___       __
#    _\ \ \ /\ \/\ \ \ \ \  /\ \/\ \\/_\__ \ \ \ \/   / __`\ /' _ `\   /'__`\
#   /\ \_\ \\ \ \_\ \ \_\ \_\ \ \_\ \ /\ \L\ \\ \ \_ /\ \L\ \/\ \/\ \ /\  __/
#   \ \____/ \ \____/ /\____\\/`____ \\ `\____\\ \__\\ \____/\ \_\ \_\\ \____\
#    \/___/   \/___/  \/____/ `/___/> \\/_____/ \/__/ \/___/  \/_/\/_/ \/____/
#                                /\___/
#                                \/__/
# encoding: utf-8
import pandas as pd


def words_get(path):
    origin_df = pd.read_excel(path, sheet_name='all_json')
    mapping_df = pd.read_excel(path, sheet_name='id_mapping')

    mapping_df = mapping_df[['CommodityId', 'CommodityChsName_x']]

    return mapping_df, origin_df

def rename(mapping_df, origin_df):
    mapping_df.fillna('', inplace=True)
    mapping = dict(zip(mapping_df['CommodityId'], mapping_df['CommodityChsName_x']))

    for key,value in mapping.items():
        origin_df['SixMap'] = origin_df['SixMap'].str.replace('"'+key+'"', value)
    return origin_df

def format_excel(df, path):
    from Utils.Excelize import ReadExcel, width_auto_fit, use_style_header

    df.to_excel(path, sheet_name='all_json', index=False)
    excel = ReadExcel(path)
    width_auto_fit(excel.selected_sheet,  {'C': 15, 'G': 60})
    use_style_header(excel.selected_sheet, style_dict=None)
    excel.save()

def main():
    source_path = '../ExcelFiles/source.xlsx'
    target_path = '../ExcelFiles/target.xlsx'

    mapping_df, origin_df = words_get(source_path)
    df_renamed = rename(mapping_df, origin_df)
    format_excel(df_renamed, target_path)

if __name__ == '__main__':
    main()
