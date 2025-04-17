# encoding: utf-8
import pandas as pd


class KeyMapping:
    def __init__(self, file_path="../ExcelFiles/key_map.xlsx"):
        self.file_path = file_path
        self.mapping_df = self.words_get()
        self.mapping = self.get_mapping()

    def words_get(self):
        mapping_df = pd.read_excel(self.file_path, sheet_name='id_mapping')
        mapping_df = mapping_df[['Contract_Code', 'Contract_Abbr']]
        return mapping_df

    def get_mapping(self) -> dict:
        self.mapping_df.fillna('', inplace=True)
        mapping = dict(zip(self.mapping_df['Contract_Abbr'], self.mapping_df['Contract_Code']))

        return mapping


def app():
    res = KeyMapping().mapping
    print(res)


GLOBAL_KEY_MAPPING = KeyMapping().mapping


def mapping_handler(abbr, if_option=False):
    temp = GLOBAL_KEY_MAPPING.get(abbr, "")
    if temp == "":
        return abbr
    if if_option:
        temp = temp.replace("|F|", "|O|")
    return temp


if __name__ == '__main__':
    app()
    strTest = "FU"
    for key, value in GLOBAL_KEY_MAPPING.items():
        temp1 = str.replace(key, value)
        print(temp1)
